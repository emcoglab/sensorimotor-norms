"""
===========================
Sensorimotor norms preferences.
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
from os import path


class Preferences:

    _data_dir = path.join("/Users",
                          "caiwingfield",
                          "Box Sync",
                          "LANGBOOT Project",
                          "Experiments",
                          "Phase 1 - Categorisation",
                          "Experiment 1.4 - Category production",
                          "Data & Analysis",
                          "Data for proximity measures")

    sensorimotor_norms_path = path.join(_data_dir, "sensorimotor_norms_for_39731_words_low_N_known_removed.csv")
