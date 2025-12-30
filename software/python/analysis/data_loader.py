#!/usr/bin/env python3
"""
data_loader.py - Load and validate experimental data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ExperimentMetadata:
    """Metadata for an experiment"""
    test_id: str
    protocol: str
    date: str
    filepath: str
    frequency_hz: Optional[float] = None
    voltage_kv: Optional[float] = None
    amplitude_pct: Optional[float] = None
    duration_s: Optional[float] = None
    notes: str = ""


def load_experiment(filepath: str) -> Tuple[pd.DataFrame, ExperimentMetadata]:
    """
    Load experiment data and extract metadata from filename.

    Filename format: {Protocol}_{TestID}_{Date}_{Time}.csv
    Example: CV_007_20240115_1520.csv

    Parameters:
        filepath: Path to CSV data file

    Returns:
        Tuple of (DataFrame, ExperimentMetadata)
    """
    path = Path(filepath)

    # Parse filename
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

    # Load data
    df = pd.read_csv(filepath)

    # Validate columns
    required_cols = ['timestamp_us']
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Add derived columns
    df['time_s'] = (df['timestamp_us'] - df['timestamp_us'].iloc[0]) / 1e6

    # Calculate magnitude for each sensor
    for sensor in ['m1', 'm2', 'm3']:
        cols = [f'{sensor}{ax}' for ax in 'xyz']
        if all(c in df.columns for c in cols):
            df[f'{sensor}_mag'] = np.sqrt(sum(df[c]**2 for c in cols))

    # Calculate acceleration magnitude
    if all(f'a{ax}' in df.columns for ax in 'xyz'):
        df['acc_mag'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)

    return df, metadata


def validate_data(df: pd.DataFrame) -> dict:
    """
    Perform data quality checks.

    Parameters:
        df: DataFrame with sensor data

    Returns:
        Dict of quality metrics including:
        - sample_rate_hz: Measured sample rate
        - duration_s: Total duration
        - sample_count: Number of samples
        - timestamp_gaps: Number of timing gaps detected
        - nan_count: Total NaN values
    """
    quality = {}

    # Check for gaps in timestamps
    dt = np.diff(df['timestamp_us'])
    expected_dt = np.median(dt)
    gaps = np.sum(dt > 2 * expected_dt)
    quality['timestamp_gaps'] = int(gaps)
    quality['sample_rate_hz'] = 1e6 / expected_dt

    # Check for saturated values (HMC5883L saturates at ±2048)
    for col in ['m1x', 'm1y', 'm1z', 'm2x', 'm2y', 'm2z', 'm3x', 'm3y', 'm3z']:
        if col in df.columns:
            saturated = np.sum(np.abs(df[col]) >= 2047)
            quality[f'{col}_saturated'] = int(saturated)

    # Check for NaN values
    quality['nan_count'] = int(df.isna().sum().sum())

    # Duration
    quality['duration_s'] = float(df['time_s'].iloc[-1])
    quality['sample_count'] = len(df)

    return quality


def load_multiple_experiments(filepaths: list) -> Tuple[list, list]:
    """
    Load multiple experiment files.

    Parameters:
        filepaths: List of file paths

    Returns:
        Tuple of (list of DataFrames, list of ExperimentMetadata)
    """
    dataframes = []
    metadata_list = []

    for filepath in filepaths:
        try:
            df, metadata = load_experiment(filepath)
            dataframes.append(df)
            metadata_list.append(metadata)
        except Exception as e:
            print(f"Warning: Failed to load {filepath}: {e}")

    return dataframes, metadata_list
