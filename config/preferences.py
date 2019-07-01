"""
===========================
Global preferences.
===========================

Dr. Cai Wingfield
---------------------------
Embodied Cognition Lab
Department of Psychology
University of Lancaster
c.wingfield@lancaster.ac.uk
caiwingfield.net
---------------------------
2019
---------------------------
"""

from .config import Config


class Preferences:
    """
    Preferences for models.
    """
    
    # Static config
    _config: Config = Config()

    sensorimotor_norms_path = _config.value_by_key_path("sensorimotor-norms-location")
