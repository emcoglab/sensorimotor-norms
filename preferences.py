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
                          "Model")

    sensorimotor_norms_path = path.join(_data_dir, "FINAL_sensorimotor_norms_for_39707_words.csv")
