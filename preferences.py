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

    box_root = "/Users/caiwingfield/Box Sync/LANGBOOT Project/"
    data_dir_root = path.join(box_root, "Experiments/Phase 1 - Categorisation/Experiment 1.4 - Category production/Data & Analysis/Data for proximity measures/")

    sensorimotor_wordlist_csv_path = path.join(data_dir_root, "Data for sensorimotor proximity measures (some compound words).csv")
    sensorimotor_norms_path        = path.join(data_dir_root, "sensorimotor_norms_for_38982_words_low_N_known_removed.csv")
    sensorimotor_results_path      = path.join(data_dir_root, "sensorimotor proximity results.csv")
