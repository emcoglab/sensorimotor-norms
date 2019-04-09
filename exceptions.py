"""
===========================
Sensorimotor norms exceptions.
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


class WordNotInNormsError(LookupError):
    """
    An error raised when a word is not found in the norms.
    """
    pass
