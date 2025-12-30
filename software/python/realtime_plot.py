#!/usr/bin/env python3
"""
realtime_plot.py - Real-time plotting of magnetometer data from Arduino

Displays live data stream from the DAQ system with rolling windows
for time series and FFT spectrum.

Usage:
    python realtime_plot.py [--port /dev/ttyACM0] [--baud 115200]

Requirements:
    pip install pyserial matplotlib numpy

Press Ctrl+C to exit.
"""

import argparse
import sys
import time
from collections import deque
from threading import Thread, Event

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Error: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


# Configuration
WINDOW_SECONDS = 10  # Rolling window size
SAMPLE_RATE = 100    # Expected sample rate (Hz)
BUFFER_SIZE = WINDOW_SECONDS * SAMPLE_RATE


class DataBuffer:
    """Thread-safe circular buffer for sensor data."""

    def __init__(self, maxlen: int):
        self.maxlen = maxlen
        self.time = deque(maxlen=maxlen)
        self.m1_mag = deque(maxlen=maxlen)
        self.m2_mag = deque(maxlen=maxlen)
        self.m3_mag = deque(maxlen=maxlen)
        self.acc_mag = deque(maxlen=maxlen)
        self.start_time = None

    def add_sample(self, timestamp_us: int, m1x, m1y, m1z,
                   m2x, m2y, m2z, m3x, m3y, m3z, ax, ay, az):
        """Add a sample to the buffer."""
        if self.start_time is None:
            self.start_time = timestamp_us

        t = (timestamp_us - self.start_time) / 1e6

        # Calculate magnitudes
        m1_mag = np.sqrt(m1x**2 + m1y**2 + m1z**2)
        m2_mag = np.sqrt(m2x**2 + m2y**2 + m2z**2)
        m3_mag = np.sqrt(m3x**2 + m3y**2 + m3z**2)
        acc_mag = np.sqrt(ax**2 + ay**2 + az**2)

        self.time.append(t)
        self.m1_mag.append(m1_mag)
        self.m2_mag.append(m2_mag)
        self.m3_mag.append(m3_mag)
        self.acc_mag.append(acc_mag)

    def get_arrays(self):
        """Get numpy arrays of current buffer contents."""
        return (
            np.array(self.time),
            np.array(self.m1_mag),
            np.array(self.m2_mag),
            np.array(self.m3_mag),
            np.array(self.acc_mag)
        )

    def __len__(self):
        return len(self.time)


def find_arduino_port():
    """Auto-detect Arduino serial port."""
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Common Arduino identifiers
        if 'Arduino' in port.description or 'ttyACM' in port.device or 'ttyUSB' in port.device:
            return port.device

    # Return first available if no Arduino found
    if ports:
        return ports[0].device

    return None


def serial_reader(port: str, baud: int, buffer: DataBuffer, stop_event: Event):
    """Background thread to read serial data."""
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print(f"Connected to {port} at {baud} baud")

        # Skip header line
        ser.readline()

        while not stop_event.is_set():
            try:
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    continue

                parts = line.split(',')
                if len(parts) != 13:
                    continue

                values = [int(p) for p in parts]
                buffer.add_sample(*values)

            except (ValueError, UnicodeDecodeError):
                continue

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        if 'ser' in locals():
            ser.close()


def compute_fft(data: np.ndarray, fs: float = SAMPLE_RATE):
    """Compute FFT magnitude spectrum."""
    if len(data) < 16:
        return np.array([]), np.array([])

    n = len(data)
    # Remove DC offset
    data = data - np.mean(data)
    # Apply window
    window = np.hanning(n)
    data = data * window
    # FFT
    fft_vals = np.fft.rfft(data)
    fft_mag = np.abs(fft_vals) * 2 / n
    freqs = np.fft.rfftfreq(n, 1/fs)

    return freqs, fft_mag


def create_realtime_plot(buffer: DataBuffer, stop_event: Event):
    """Create and run the real-time plot."""
    # Set up figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Pais Effect Demonstrator - Real-time Monitor', fontsize=14)

    # Time series - Magnetometers
    ax1 = axes[0, 0]
    line_m1, = ax1.plot([], [], 'b-', label='M1', alpha=0.8)
    line_m2, = ax1.plot([], [], 'g-', label='M2', alpha=0.8)
    line_m3, = ax1.plot([], [], 'r-', label='M3', alpha=0.8)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Field Magnitude (LSB)')
    ax1.set_title('Magnetometer Readings')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Time series - Accelerometer
    ax2 = axes[0, 1]
    line_acc, = ax2.plot([], [], 'purple', alpha=0.8)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Acceleration (LSB)')
    ax2.set_title('Accelerometer')
    ax2.grid(True, alpha=0.3)

    # FFT - Magnetometer
    ax3 = axes[1, 0]
    line_fft, = ax3.plot([], [], 'b-', alpha=0.8)
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Magnitude')
    ax3.set_title('FFT - Magnetometer 1')
    ax3.set_xlim(0, SAMPLE_RATE / 2)
    ax3.grid(True, alpha=0.3)

    # Statistics
    ax4 = axes[1, 1]
    ax4.axis('off')
    stats_text = ax4.text(0.1, 0.9, '', transform=ax4.transAxes,
                          fontfamily='monospace', fontsize=10,
                          verticalalignment='top')

    plt.tight_layout()

    def update(frame):
        """Update function for animation."""
        if len(buffer) < 10:
            return line_m1, line_m2, line_m3, line_acc, line_fft, stats_text

        t, m1, m2, m3, acc = buffer.get_arrays()

        # Update time series
        if len(t) > 0:
            t_offset = t - t[0]  # Start from 0

            line_m1.set_data(t_offset, m1)
            line_m2.set_data(t_offset, m2)
            line_m3.set_data(t_offset, m3)
            line_acc.set_data(t_offset, acc)

            # Adjust axes
            ax1.set_xlim(0, max(t_offset[-1], WINDOW_SECONDS))
            ax1.set_ylim(min(m1.min(), m2.min(), m3.min()) * 0.95,
                         max(m1.max(), m2.max(), m3.max()) * 1.05)

            ax2.set_xlim(0, max(t_offset[-1], WINDOW_SECONDS))
            if len(acc) > 0:
                ax2.set_ylim(acc.min() * 0.95, acc.max() * 1.05)

        # Update FFT
        if len(m1) >= 64:
            freqs, fft_mag = compute_fft(m1)
            if len(freqs) > 0:
                line_fft.set_data(freqs, fft_mag)
                ax3.set_ylim(0, max(fft_mag.max() * 1.1, 1))

        # Update statistics
        if len(m1) > 10:
            stats = f"Buffer: {len(buffer)} samples\n"
            stats += f"Time: {t[-1]:.1f} s\n\n"
            stats += f"M1: mean={m1.mean():.0f}, std={m1.std():.1f}\n"
            stats += f"M2: mean={m2.mean():.0f}, std={m2.std():.1f}\n"
            stats += f"M3: mean={m3.mean():.0f}, std={m3.std():.1f}\n"
            stats += f"Acc: mean={acc.mean():.0f}, std={acc.std():.1f}\n"

            # Detect vibration frequency from FFT
            if len(m1) >= 64:
                freqs, fft_mag = compute_fft(acc)
                if len(freqs) > 1:
                    peak_idx = np.argmax(fft_mag[1:]) + 1  # Skip DC
                    peak_freq = freqs[peak_idx]
                    stats += f"\nPeak vibration: {peak_freq:.1f} Hz"

            stats_text.set_text(stats)

        return line_m1, line_m2, line_m3, line_acc, line_fft, stats_text

    # Create animation
    ani = FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()


def main():
    parser = argparse.ArgumentParser(description='Real-time magnetometer plotter')
    parser.add_argument('--port', '-p', type=str, default=None,
                        help='Serial port (auto-detect if not specified)')
    parser.add_argument('--baud', '-b', type=int, default=115200,
                        help='Baud rate (default: 115200)')
    parser.add_argument('--demo', action='store_true',
                        help='Run in demo mode with simulated data')
    args = parser.parse_args()

    buffer = DataBuffer(BUFFER_SIZE)
    stop_event = Event()

    if args.demo:
        # Demo mode with simulated data
        print("Running in demo mode with simulated data...")

        def demo_generator():
            t = 0
            while not stop_event.is_set():
                # Simulate magnetometer readings with some noise
                base = 2000
                noise = 50
                vibration = 100 * np.sin(2 * np.pi * 5 * t)  # 5 Hz vibration

                m1x = base + np.random.randn() * noise + vibration
                m1y = np.random.randn() * noise
                m1z = base + np.random.randn() * noise
                m2x = base + np.random.randn() * noise + vibration * 0.8
                m2y = np.random.randn() * noise
                m2z = base + np.random.randn() * noise
                m3x = base + np.random.randn() * noise + vibration * 0.5
                m3y = np.random.randn() * noise
                m3z = base + np.random.randn() * noise
                ax = np.random.randn() * 10 + vibration * 0.1
                ay = np.random.randn() * 10
                az = 256 + np.random.randn() * 10

                buffer.add_sample(int(t * 1e6), int(m1x), int(m1y), int(m1z),
                                  int(m2x), int(m2y), int(m2z),
                                  int(m3x), int(m3y), int(m3z),
                                  int(ax), int(ay), int(az))

                t += 1 / SAMPLE_RATE
                time.sleep(1 / SAMPLE_RATE)

        reader_thread = Thread(target=demo_generator)

    else:
        # Real serial mode
        port = args.port
        if port is None:
            port = find_arduino_port()
            if port is None:
                print("Error: No serial port found. Specify with --port or connect Arduino.")
                print("Available ports:")
                for p in serial.tools.list_ports.comports():
                    print(f"  {p.device}: {p.description}")
                sys.exit(1)

        reader_thread = Thread(target=serial_reader,
                               args=(port, args.baud, buffer, stop_event))

    reader_thread.daemon = True
    reader_thread.start()

    # Give serial time to start
    time.sleep(0.5)

    # Run plot
    create_realtime_plot(buffer, stop_event)

    print("\nExiting...")
    stop_event.set()
    reader_thread.join(timeout=1)


if __name__ == '__main__':
    main()
