#!/usr/bin/env python3
"""
quick_analysis.py - One-click analysis for a single experiment

Usage:
    python quick_analysis.py <data_file.csv> [output_dir]

Example:
    python quick_analysis.py data/CV_007_20240115_1520.csv results/
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import signal, stats
from dataclasses import dataclass
from typing import Tuple, Optional

# ==================== DATA LOADING ====================

@dataclass
class ExperimentMetadata:
    """Metadata for an experiment"""
    test_id: str
    protocol: str
    date: str
    filepath: str

def load_experiment(filepath: str) -> Tuple[pd.DataFrame, ExperimentMetadata]:
    """Load experiment data and extract metadata from filename."""
    path = Path(filepath)
    
    parts = path.stem.split('_')
    protocol = parts[0] if len(parts) > 0 else "UNKNOWN"
    test_id = parts[1] if len(parts) > 1 else "000"
    date = parts[2] if len(parts) > 2 else "00000000"
    
    metadata = ExperimentMetadata(
        test_id=f"{protocol}_{test_id}",
        protocol=protocol,
        date=date,
        filepath=str(path)
    )
    
    df = pd.read_csv(filepath)
    
    # Add derived columns
    df['time_s'] = (df['timestamp_us'] - df['timestamp_us'].iloc[0]) / 1e6
    
    # Calculate magnitude for each sensor
    for sensor in ['m1', 'm2', 'm3']:
        cols = [f'{sensor}{ax}' for ax in 'xyz']
        if all(c in df.columns for c in cols):
            df[f'{sensor}_mag'] = np.sqrt(sum(df[c]**2 for c in cols))
    
    # Acceleration magnitude
    if all(f'a{ax}' in df.columns for ax in 'xyz'):
        df['acc_mag'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)
    
    return df, metadata

def validate_data(df: pd.DataFrame) -> dict:
    """Perform data quality checks."""
    quality = {}
    
    dt = np.diff(df['timestamp_us'])
    expected_dt = np.median(dt)
    quality['sample_rate_hz'] = 1e6 / expected_dt
    quality['duration_s'] = df['time_s'].iloc[-1]
    quality['sample_count'] = len(df)
    quality['timestamp_gaps'] = np.sum(dt > 2 * expected_dt)
    quality['nan_count'] = df.isna().sum().sum()
    
    return quality

# ==================== CALIBRATION ====================

def apply_calibration(df: pd.DataFrame) -> pd.DataFrame:
    """Convert magnetometer LSB to microtesla."""
    df_cal = df.copy()
    
    # HMC5883L at gain 1: 1090 LSB/Gauss = 10900 LSB/mT
    # 1 Gauss = 100 μT
    sensitivity = 10900 / 100  # LSB per μT
    
    for sensor in ['m1', 'm2', 'm3']:
        for axis in 'xyz':
            col = f'{sensor}{axis}'
            if col in df.columns:
                df_cal[f'{col}_uT'] = df[col] / sensitivity
        
        # Recalculate magnitude in physical units
        cols_uT = [f'{sensor}{ax}_uT' for ax in 'xyz']
        if all(c in df_cal.columns for c in cols_uT):
            df_cal[f'{sensor}_mag_uT'] = np.sqrt(sum(df_cal[c]**2 for c in cols_uT))
    
    return df_cal

def apply_accel_calibration(df: pd.DataFrame) -> pd.DataFrame:
    """Convert accelerometer LSB to m/s²."""
    df_cal = df.copy()
    
    # ADXL345 at ±16g, full resolution: 3.9 mg/LSB
    sensitivity = 3.9  # mg per LSB
    
    for axis in 'xyz':
        col = f'a{axis}'
        if col in df.columns:
            df_cal[f'{col}_ms2'] = df[col] * sensitivity * 9.81 / 1000
    
    if all(f'a{ax}_ms2' in df_cal.columns for ax in 'xyz'):
        df_cal['acc_mag_ms2'] = np.sqrt(sum(df_cal[f'a{ax}_ms2']**2 for ax in 'xyz'))
    
    return df_cal

# ==================== SIGNAL PROCESSING ====================

def extract_baseline(df: pd.DataFrame, 
                     pre_window: Tuple[float, float] = (0, 10),
                     post_window: Optional[Tuple[float, float]] = None) -> dict:
    """Extract baseline statistics from pre/post stimulus periods."""
    baseline = {}
    
    mask_pre = (df['time_s'] >= pre_window[0]) & (df['time_s'] < pre_window[1])
    
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

# ==================== STATISTICS ====================

def detection_statistics(signal_period: np.ndarray, 
                         baseline_period: np.ndarray) -> dict:
    """Calculate detection statistics comparing signal to baseline."""
    mean_signal = np.mean(signal_period)
    mean_baseline = np.mean(baseline_period)
    std_baseline = np.std(baseline_period)
    
    mean_diff = mean_signal - mean_baseline
    snr = mean_diff / std_baseline if std_baseline > 0 else 0
    
    t_stat, p_value = stats.ttest_ind(signal_period, baseline_period)
    sigma_level = np.abs(stats.norm.ppf(p_value / 2)) if p_value > 0 else np.inf
    
    return {
        'mean_signal': mean_signal,
        'mean_baseline': mean_baseline,
        'mean_diff': mean_diff,
        'std_baseline': std_baseline,
        'std_signal': np.std(signal_period),
        'snr': snr,
        't_stat': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'sigma_level': sigma_level
    }

# ==================== VISUALIZATION ====================

def plot_experiment_overview(df: pd.DataFrame, 
                              baseline: dict,
                              title: str = "Experiment Overview") -> plt.Figure:
    """Create standard 4-panel experiment overview plot."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel 1: Magnetometer time series
    ax1 = axes[0, 0]
    for sensor in ['m1', 'm2', 'm3']:
        col = f'{sensor}_mag_uT'
        if col in df.columns:
            ax1.plot(df['time_s'], df[col], label=sensor.upper(), alpha=0.7)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Field Magnitude (μT)')
    ax1.legend()
    ax1.set_title('Magnetometer Signals')
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Acceleration
    ax2 = axes[0, 1]
    if 'acc_mag_ms2' in df.columns:
        ax2.plot(df['time_s'], df['acc_mag_ms2'], color='red', alpha=0.7)
    elif 'acc_mag' in df.columns:
        ax2.plot(df['time_s'], df['acc_mag'], color='red', alpha=0.7)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Acceleration')
    ax2.set_title('Plate Acceleration')
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: PSD
    ax3 = axes[1, 0]
    for sensor in ['m1', 'm2', 'm3']:
        col = f'{sensor}_mag_uT'
        if col in df.columns:
            f, psd = signal.welch(df[col].values, 100, nperseg=min(1024, len(df)//4))
            ax3.semilogy(f, psd, label=sensor.upper(), alpha=0.7)
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('PSD (μT²/Hz)')
    ax3.legend()
    ax3.set_title('Power Spectral Density')
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: Statistics text
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    stats_text = "Baseline Statistics:\n\n"
    for col, stat in list(baseline.items())[:3]:
        stats_text += f"{col}:\n"
        stats_text += f"  Mean: {stat['combined_mean']:.2f} μT\n"
        stats_text += f"  Std:  {stat['combined_std']:.2f} μT\n\n"
    
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes,
             fontfamily='monospace', fontsize=10, verticalalignment='top')
    ax4.set_title('Statistics')
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig

# ==================== MAIN ====================

def analyze_experiment(filepath: str, output_dir: str = 'results'):
    """Run complete analysis on a single experiment file."""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load data
    print(f"Loading {filepath}...")
    df, metadata = load_experiment(filepath)
    
    # Validate
    quality = validate_data(df)
    print(f"Samples: {quality['sample_count']}, Duration: {quality['duration_s']:.1f}s")
    print(f"Sample rate: {quality['sample_rate_hz']:.1f} Hz")
    
    if quality['timestamp_gaps'] > 0:
        print(f"Warning: {quality['timestamp_gaps']} timestamp gaps detected")
    
    # Calibrate
    df = apply_calibration(df)
    df = apply_accel_calibration(df)
    
    # Extract baseline
    baseline = extract_baseline(df)
    
    # Calculate detection statistics
    signal_mask = (df['time_s'] >= 15) & (df['time_s'] <= df['time_s'].max() - 15)
    baseline_mask = (df['time_s'] < 10) | (df['time_s'] > df['time_s'].max() - 10)
    
    print("\n" + "="*50)
    print("Detection Statistics:")
    print("="*50)
    
    for col in ['m1_mag_uT', 'm2_mag_uT', 'm3_mag_uT']:
        if col in df.columns:
            sig_data = df.loc[signal_mask, col].values
            base_data = df.loc[baseline_mask, col].values
            
            if len(sig_data) > 0 and len(base_data) > 0:
                stat = detection_statistics(sig_data, base_data)
                status = "⚠️  SIGNIFICANT" if stat['significant'] else "✓ Not significant"
                print(f"  {col}: SNR={stat['snr']:.2f}, p={stat['p_value']:.4f}, "
                      f"σ={stat['sigma_level']:.1f} {status}")
    
    print("="*50 + "\n")
    
    # Generate plots
    fig = plot_experiment_overview(df, baseline, title=metadata.test_id)
    output_file = output_path / f"{metadata.test_id}_overview.png"
    fig.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot saved to {output_file}")
    
    return df, metadata, baseline

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'results'
    
    analyze_experiment(filepath, output_dir)
