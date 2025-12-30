# Pais Effect Demonstrator - Python Analysis Tools
# See docs/06-phase5-analysis.md for detailed documentation

from .data_loader import load_experiment, validate_data
from .calibration import apply_calibration, apply_accel_calibration
from .signal_processing import extract_baseline, subtract_baseline, compute_spectrum
from .statistics import detection_statistics, calculate_upper_bound, test_pais_scaling

__version__ = "0.1.0"
__all__ = [
    'load_experiment',
    'validate_data', 
    'apply_calibration',
    'apply_accel_calibration',
    'extract_baseline',
    'subtract_baseline',
    'compute_spectrum',
    'detection_statistics',
    'calculate_upper_bound',
    'test_pais_scaling'
]
