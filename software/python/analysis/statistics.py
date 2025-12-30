#!/usr/bin/env python3
"""
statistics.py - Statistical analysis for signal detection
"""

import numpy as np
from scipy import stats
from typing import Tuple


def detection_statistics(signal_period: np.ndarray,
                         baseline_period: np.ndarray) -> dict:
    """
    Calculate detection statistics comparing signal to baseline.

    Parameters:
        signal_period: Array of measurements during stimulus
        baseline_period: Array of measurements during baseline

    Returns:
        Dict with:
        - mean_signal: Mean of signal period
        - mean_baseline: Mean of baseline period
        - mean_diff: Difference in means
        - std_baseline: Standard deviation of baseline
        - std_signal: Standard deviation of signal
        - snr: Signal-to-noise ratio
        - t_stat: Student's t statistic
        - p_value: p-value for difference
        - significant: Whether p < 0.05
        - sigma_level: Detection significance in sigma
    """
    mean_signal = np.mean(signal_period)
    mean_baseline = np.mean(baseline_period)
    std_baseline = np.std(baseline_period)
    std_signal = np.std(signal_period)

    mean_diff = mean_signal - mean_baseline
    snr = mean_diff / std_baseline if std_baseline > 0 else 0

    # Two-sample t-test
    t_stat, p_value = stats.ttest_ind(signal_period, baseline_period)

    # Convert to sigma level
    if p_value > 0 and p_value < 1:
        sigma_level = np.abs(stats.norm.ppf(p_value / 2))
    else:
        sigma_level = 0 if p_value >= 1 else np.inf

    return {
        'mean_signal': float(mean_signal),
        'mean_baseline': float(mean_baseline),
        'mean_diff': float(mean_diff),
        'std_baseline': float(std_baseline),
        'std_signal': float(std_signal),
        'snr': float(snr),
        't_stat': float(t_stat),
        'p_value': float(p_value),
        'significant': bool(p_value < 0.05),
        'sigma_level': float(sigma_level)
    }


def calculate_upper_bound(baseline_std: float,
                           confidence: float = 0.95,
                           n_samples: int = 1000) -> float:
    """
    Calculate upper bound on signal if nothing detected.

    Uses one-sided confidence interval.

    Parameters:
        baseline_std: Standard deviation of baseline measurements
        confidence: Confidence level (default 0.95 = 95%)
        n_samples: Number of samples in measurement

    Returns:
        Upper bound in same units as baseline_std
    """
    # Critical value for one-sided test
    z = stats.norm.ppf(confidence)

    # Standard error of mean
    sem = baseline_std / np.sqrt(n_samples)

    # Upper bound
    return float(z * sem)


def fit_power_law(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    """
    Fit y = A * x^n power law using log-log regression.

    Parameters:
        x: Independent variable (e.g., frequency)
        y: Dependent variable (e.g., signal amplitude)

    Returns:
        Tuple of (n exponent, A coefficient, r_squared)
    """
    # Remove zeros and negatives
    mask = (x > 0) & (y > 0)
    x_clean = x[mask]
    y_clean = y[mask]

    if len(x_clean) < 2:
        return np.nan, np.nan, np.nan

    # Log-log regression
    log_x = np.log(x_clean)
    log_y = np.log(y_clean)

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)

    n = slope
    A = np.exp(intercept)
    r_squared = r_value**2

    return float(n), float(A), float(r_squared)


def test_pais_scaling(frequencies: np.ndarray, signals: np.ndarray) -> dict:
    """
    Test if signal follows Pais prediction (v³) vs classical (v²).

    The Pais patents suggest effects scale with frequency cubed,
    while classical electromagnetic effects typically scale with
    frequency squared.

    Parameters:
        frequencies: Array of test frequencies
        signals: Array of measured signal amplitudes

    Returns:
        Dict with comparison of fits
    """
    # Fit power law
    n_fit, A_fit, r2_fit = fit_power_law(frequencies, signals)

    # Calculate residuals for v² (classical)
    classical_pred = frequencies**2
    classical_pred = classical_pred * np.mean(signals) / np.mean(classical_pred)
    classical_residuals = np.sum((signals - classical_pred)**2)

    # Calculate residuals for v³ (Pais)
    pais_pred = frequencies**3
    pais_pred = pais_pred * np.mean(signals) / np.mean(pais_pred)
    pais_residuals = np.sum((signals - pais_pred)**2)

    return {
        'fitted_exponent': n_fit,
        'fitted_coefficient': A_fit,
        'fit_r_squared': r2_fit,
        'classical_exponent': 2,
        'pais_exponent': 3,
        'classical_residuals': float(classical_residuals),
        'pais_residuals': float(pais_residuals),
        'favors_pais': bool(pais_residuals < classical_residuals),
        'residual_ratio': float(classical_residuals / pais_residuals) if pais_residuals > 0 else np.inf
    }


def multiple_comparison_correction(p_values: np.ndarray,
                                    method: str = 'bonferroni') -> np.ndarray:
    """
    Apply multiple comparison correction to p-values.

    Parameters:
        p_values: Array of p-values
        method: Correction method ('bonferroni', 'fdr')

    Returns:
        Corrected p-values
    """
    n = len(p_values)

    if method == 'bonferroni':
        return np.minimum(p_values * n, 1.0)

    elif method == 'fdr':
        # Benjamini-Hochberg procedure
        sorted_idx = np.argsort(p_values)
        sorted_p = p_values[sorted_idx]

        corrected = np.zeros_like(sorted_p)
        for i, p in enumerate(sorted_p):
            corrected[i] = p * n / (i + 1)

        # Ensure monotonicity
        for i in range(n - 2, -1, -1):
            corrected[i] = min(corrected[i], corrected[i + 1])

        # Restore original order
        result = np.zeros_like(p_values)
        result[sorted_idx] = corrected
        return np.minimum(result, 1.0)

    else:
        raise ValueError(f"Unknown method: {method}")


def effect_size(signal_period: np.ndarray, baseline_period: np.ndarray) -> dict:
    """
    Calculate effect size metrics.

    Parameters:
        signal_period: Measurements during stimulus
        baseline_period: Measurements during baseline

    Returns:
        Dict with Cohen's d and other effect size measures
    """
    mean_diff = np.mean(signal_period) - np.mean(baseline_period)

    # Pooled standard deviation
    n1, n2 = len(signal_period), len(baseline_period)
    s1, s2 = np.std(signal_period, ddof=1), np.std(baseline_period, ddof=1)
    pooled_std = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))

    # Cohen's d
    cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0

    # Glass's delta (using baseline std)
    glass_delta = mean_diff / s2 if s2 > 0 else 0

    return {
        'cohens_d': float(cohens_d),
        'glass_delta': float(glass_delta),
        'mean_difference': float(mean_diff),
        'pooled_std': float(pooled_std)
    }
