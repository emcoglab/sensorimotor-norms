"""
===========================
Sensorimotor norms interface.
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


from pandas import DataFrame, read_csv

from .exceptions import LabelNotInNormsError
from .preferences import Preferences


class ColNames(object):
    """Column names used in sensorimotor data"""

    Word = "word"

    # Motor
    Head          = "head.mean"
    Mouth         = "mouth.mean"
    Hand          = "hand.mean"
    Foot          = "foot.mean"
    Torso         = "torso.mean"

    # Sensory
    Touch         = "haptic.mean"
    Hearing       = "auditory.mean"
    Seeing        = "visual.mean"
    Smelling      = "olfactory.mean"
    Tasting       = "gustatory.mean"
    Interoception = "interoception.mean"


class SensorimotorNorms(object):

    DataColNames = [
        # Sensory
        ColNames.Touch, ColNames.Hearing, ColNames.Seeing, ColNames.Smelling, ColNames.Tasting, ColNames.Interoception,
        # Motor
        ColNames.Head, ColNames.Mouth, ColNames.Hand, ColNames.Foot, ColNames.Torso,
    ]

    def __init__(self):
        self.data: DataFrame = read_csv(Preferences.sensorimotor_norms_path, index_col=None, header=0,
                                        usecols=[ColNames.Word] + SensorimotorNorms.DataColNames)

        # Trim whitespace and convert words to lower case
        self.data[ColNames.Word] = self.data[ColNames.Word].str.strip()
        self.data[ColNames.Word] = self.data[ColNames.Word].str.lower()

    def vector_for_word(self, word):
        row = self.data[self.data[ColNames.Word] == word]

        # Make sure we only got one row
        n_rows = row.shape[0]
        if n_rows is 0:
            # No rows: word wasn't found
            raise LabelNotInNormsError(word)
        elif n_rows > 1:
            # More than one row: word wasn't a unique row identifier
            # Something has gone wrong!
            raise Exception()

        return [
            row.iloc[0][col_name]
            for col_name in SensorimotorNorms.DataColNames
        ]
