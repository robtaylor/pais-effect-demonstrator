#!/usr/bin/env python3
"""
calibration.py - Apply sensor calibrations
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class MagnetometerCalibration:
    """
    Calibration parameters for a magnetometer.

    Attributes:
        offset_x/y/z: Hard iron offset for each axis
        scale_x/y/z: Soft iron scale factor for each axis
        sensitivity: LSB per Tesla (HMC5883L at gain 1 = 1090 LSB/Gauss = 10900 LSB/mT)
    """
    offset_x: float = 0.0
    offset_y: float = 0.0
    offset_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    sensitivity: float = 10900.0  # LSB per mT


@dataclass
class AccelerometerCalibration:
    """
    Calibration for ADXL345 accelerometer.

    Attributes:
        offset_x/y/z: Offset for each axis
        sensitivity: mg per LSB (ADXL345 at ±16g, full resolution: 3.9 mg/LSB)
    """
    offset_x: float = 0.0
    offset_y: float = 0.0
    offset_z: float = 0.0
    sensitivity: float = 3.9  # mg per LSB


# Default calibrations (replace with measured values)
DEFAULT_MAG_CAL = {
    'm1': MagnetometerCalibration(),
    'm2': MagnetometerCalibration(),
    'm3': MagnetometerCalibration(),
}

DEFAULT_ACCEL_CAL = AccelerometerCalibration()


def apply_calibration(df: pd.DataFrame, calibrations: dict = None) -> pd.DataFrame:
    """
    Apply calibration to magnetometer data.
    Converts LSB to microtesla (μT).

    Parameters:
        df: DataFrame with magnetometer columns (m1x, m1y, m1z, etc.)
        calibrations: Dict mapping sensor names to MagnetometerCalibration objects

    Returns:
        DataFrame with additional calibrated columns (*_uT)
    """
    if calibrations is None:
        calibrations = DEFAULT_MAG_CAL

    df_cal = df.copy()

    for sensor, cal in calibrations.items():
        for axis in ['x', 'y', 'z']:
            col = f'{sensor}{axis}'
            if col not in df.columns:
                continue

            offset = getattr(cal, f'offset_{axis}')
            scale = getattr(cal, f'scale_{axis}')

            # Apply offset and scale
            df_cal[f'{col}_cal'] = (df[col] - offset) * scale

            # Convert to microtesla
            # 1 Gauss = 100 μT, sensitivity is in LSB/Gauss
            df_cal[f'{col}_uT'] = df_cal[f'{col}_cal'] / (cal.sensitivity / 100)

    # Recalculate magnitudes in physical units
    for sensor in ['m1', 'm2', 'm3']:
        cols_uT = [f'{sensor}{ax}_uT' for ax in 'xyz']
        if all(c in df_cal.columns for c in cols_uT):
            df_cal[f'{sensor}_mag_uT'] = np.sqrt(sum(df_cal[c]**2 for c in cols_uT))

    return df_cal


def apply_accel_calibration(df: pd.DataFrame, cal: AccelerometerCalibration = None) -> pd.DataFrame:
    """
    Convert accelerometer readings to m/s².

    Parameters:
        df: DataFrame with accelerometer columns (ax, ay, az)
        cal: AccelerometerCalibration object

    Returns:
        DataFrame with additional calibrated columns (*_ms2)
    """
    if cal is None:
        cal = DEFAULT_ACCEL_CAL

    df_cal = df.copy()

    for axis in ['x', 'y', 'z']:
        col = f'a{axis}'
        if col not in df.columns:
            continue

        offset = getattr(cal, f'offset_{axis}')

        # Apply offset and convert to m/s²
        # 1g = 9.81 m/s², sensitivity in mg/LSB
        df_cal[f'{col}_ms2'] = (df[col] - offset) * cal.sensitivity * 9.81 / 1000

    # Calculate magnitude
    if all(f'a{ax}_ms2' in df_cal.columns for ax in 'xyz'):
        df_cal['acc_mag_ms2'] = np.sqrt(
            df_cal['ax_ms2']**2 +
            df_cal['ay_ms2']**2 +
            df_cal['az_ms2']**2
        )

    return df_cal


def calibrate_from_tumble(data: pd.DataFrame, sensor: str) -> MagnetometerCalibration:
    """
    Calculate calibration from tumble test data.

    During tumble test, sensor is rotated through all orientations.
    Min/max values give offset and scale.

    Parameters:
        data: DataFrame containing tumble test data
        sensor: Sensor prefix (e.g., 'm1')

    Returns:
        MagnetometerCalibration with calculated parameters
    """
    offsets = {}
    scales = {}

    for axis in ['x', 'y', 'z']:
        col = f'{sensor}{axis}'
        min_val = data[col].min()
        max_val = data[col].max()

        offsets[axis] = (max_val + min_val) / 2
        scales[axis] = (max_val - min_val) / 2

    # Normalize scales to average
    avg_scale = np.mean(list(scales.values()))
    norm_scales = {ax: avg_scale / scales[ax] if scales[ax] != 0 else 1.0 for ax in 'xyz'}

    return MagnetometerCalibration(
        offset_x=offsets['x'],
        offset_y=offsets['y'],
        offset_z=offsets['z'],
        scale_x=norm_scales['x'],
        scale_y=norm_scales['y'],
        scale_z=norm_scales['z']
    )


def save_calibration(cal: MagnetometerCalibration, filepath: str):
    """Save calibration to JSON file."""
    import json

    data = {
        'offset_x': cal.offset_x,
        'offset_y': cal.offset_y,
        'offset_z': cal.offset_z,
        'scale_x': cal.scale_x,
        'scale_y': cal.scale_y,
        'scale_z': cal.scale_z,
        'sensitivity': cal.sensitivity
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_calibration(filepath: str) -> MagnetometerCalibration:
    """Load calibration from JSON file."""
    import json

    with open(filepath, 'r') as f:
        data = json.load(f)

    return MagnetometerCalibration(**data)
