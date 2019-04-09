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


class LabelNotInNormsError(LookupError):
    """
    An error raised when a label is not found in the norms.
    """

    """ Label not found. """
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    def __str__(self, *args, **kwargs):  # real signature unknown
        """ Return str(self). """
        pass

    @property
    def message(self) -> str:
        return self.args[0]
