#!/usr/bin/env python3
"""
signal_processing.py - Signal extraction and processing
"""

import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Tuple, Optional


def extract_baseline(df: pd.DataFrame,
                     pre_window: Tuple[float, float] = (0, 10),
                     post_window: Optional[Tuple[float, float]] = None) -> dict:
    """
    Extract baseline statistics from pre/post stimulus periods.

    Parameters:
        df: DataFrame with 'time_s' column
        pre_window: (start, end) in seconds for pre-stimulus baseline
        post_window: (start, end) in seconds for post-stimulus baseline
                     If None, uses last 10 seconds

    Returns:
        Dict with mean and std for each sensor channel
    """
    baseline = {}

    # Pre-stimulus baseline
    mask_pre = (df['time_s'] >= pre_window[0]) & (df['time_s'] < pre_window[1])

    # Post-stimulus baseline
    if post_window is None:
        max_t = df['time_s'].max()
        post_window = (max_t - 10, max_t)
    mask_post = (df['time_s'] >= post_window[0]) & (df['time_s'] < post_window[1])

    for col in df.columns:
        if col.endswith('_uT') or col.endswith('_mag_uT'):
            pre_mean = df.loc[mask_pre, col].mean()
            pre_std = df.loc[mask_pre, col].std()
            post_mean = df.loc[mask_post, col].mean()
            post_std = df.loc[mask_post, col].std()

            baseline[col] = {
                'pre_mean': pre_mean,
                'pre_std': pre_std,
                'post_mean': post_mean,
                'post_std': post_std,
                'combined_mean': (pre_mean + post_mean) / 2,
                'combined_std': np.sqrt(pre_std**2 + post_std**2) / 2
            }

    return baseline


def subtract_baseline(df: pd.DataFrame, baseline: dict) -> pd.DataFrame:
    """
    Subtract baseline mean from each channel.

    Parameters:
        df: DataFrame with calibrated data
        baseline: Dict from extract_baseline()

    Returns:
        DataFrame with additional baseline-subtracted columns (*_sub)
    """
    df_sub = df.copy()

    for col, stats in baseline.items():
        if col in df.columns:
            df_sub[f'{col}_sub'] = df[col] - stats['combined_mean']

    return df_sub


def compute_spectrum(df: pd.DataFrame, column: str, fs: float = 100) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute power spectral density using Welch's method.

    Parameters:
        df: DataFrame with data
        column: Column name to analyze
        fs: Sample rate in Hz

    Returns:
        Tuple of (frequencies, psd)
    """
    data = df[column].values
    nperseg = min(1024, len(data) // 4)
    if nperseg < 16:
        nperseg = len(data)
    f, psd = signal.welch(data, fs, nperseg=nperseg)
    return f, psd


def compute_spectrogram(df: pd.DataFrame, column: str,
                        fs: float = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute spectrogram for time-frequency analysis.

    Parameters:
        df: DataFrame with data
        column: Column name to analyze
        fs: Sample rate in Hz

    Returns:
        Tuple of (frequencies, times, Sxx power matrix)
    """
    data = df[column].values
    f, t, Sxx = signal.spectrogram(data, fs, nperseg=256, noverlap=128)
    return f, t, Sxx


def extract_frequency_component(df: pd.DataFrame, column: str,
                                 target_freq: float, fs: float = 100,
                                 bandwidth: float = 5) -> pd.DataFrame:
    """
    Extract component at specific frequency using bandpass filter.

    Parameters:
        df: DataFrame with data
        column: Column name to filter
        target_freq: Center frequency in Hz
        fs: Sample rate in Hz
        bandwidth: Total bandwidth in Hz

    Returns:
        DataFrame with filtered signal and envelope columns
    """
    data = df[column].values

    # Design bandpass filter
    low = (target_freq - bandwidth/2) / (fs/2)
    high = (target_freq + bandwidth/2) / (fs/2)

    # Ensure valid filter frequencies
    low = max(0.01, min(low, 0.99))
    high = max(low + 0.01, min(high, 0.99))

    b, a = signal.butter(4, [low, high], btype='band')

    # Apply filter
    filtered = signal.filtfilt(b, a, data)

    # Compute envelope using Hilbert transform
    analytic = signal.hilbert(filtered)
    envelope = np.abs(analytic)

    result = df[['time_s']].copy()
    result[f'{column}_filt_{target_freq}Hz'] = filtered
    result[f'{column}_env_{target_freq}Hz'] = envelope

    return result


def remove_mains_noise(df: pd.DataFrame, column: str,
                       mains_freq: float = 50, fs: float = 100,
                       harmonics: int = 3) -> pd.DataFrame:
    """
    Remove mains frequency and harmonics using notch filters.

    Parameters:
        df: DataFrame with data
        column: Column to filter
        mains_freq: Mains frequency (50 or 60 Hz)
        fs: Sample rate in Hz
        harmonics: Number of harmonics to remove

    Returns:
        DataFrame with notch-filtered column
    """
    data = df[column].values.copy()

    for h in range(1, harmonics + 1):
        freq = mains_freq * h
        if freq < fs / 2:  # Only filter if below Nyquist
            Q = 30.0  # Quality factor
            w0 = freq / (fs / 2)
            b, a = signal.iirnotch(w0, Q)
            data = signal.filtfilt(b, a, data)

    result = df.copy()
    result[f'{column}_notch'] = data

    return result


def compute_correlation(df: pd.DataFrame, col1: str, col2: str,
                        max_lag: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute cross-correlation between two channels.

    Parameters:
        df: DataFrame with data
        col1, col2: Column names to correlate
        max_lag: Maximum lag in samples

    Returns:
        Tuple of (lags, correlation)
    """
    x = df[col1].values - np.mean(df[col1])
    y = df[col2].values - np.mean(df[col2])

    correlation = np.correlate(x, y, mode='full')
    correlation = correlation / (np.std(x) * np.std(y) * len(x))

    mid = len(correlation) // 2
    lags = np.arange(-max_lag, max_lag + 1)
    correlation = correlation[mid - max_lag:mid + max_lag + 1]

    return lags, correlation
