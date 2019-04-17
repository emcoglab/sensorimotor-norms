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
from typing import List, Iterable

from pandas import DataFrame, read_csv

from .exceptions import WordNotInNormsError
from .preferences import Preferences


class ColNames(object):
    """Column names used in sensorimotor data."""

    Word = "Word"

    # Motor
    Head          = "Head.mean"
    Mouth         = "Mouth.mean"
    Hand          = "Hand_arm.mean"
    Foot          = "Foot_leg.mean"
    Torso         = "Torso.mean"

    # Sensory
    Touch         = "Haptic.mean"
    Hearing       = "Auditory.mean"
    Seeing        = "Visual.mean"
    Smelling      = "Olfactory.mean"
    Tasting       = "Gustatory.mean"
    Interoception = "Interoceptive.mean"


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

        self._words: set = set(self.data[ColNames.Word])

    def iter_words(self) -> Iterable[str]:
        for word in self.data[ColNames.Word]:
            yield word

    def has_word(self, word: str) -> bool:
        """True if a word is in the norms, else False."""
        return word in self._words

    def vector_for_word(self, word: str) -> List[float]:
        """
        A vector of sensorimotor data associated with each word.
        :param word:
        :return:
        :raises: WordNotInNormsError
        """
        row = self.data[self.data[ColNames.Word] == word]

        # Make sure we only got one row
        n_rows = row.shape[0]
        if n_rows is 0:
            # No rows: word wasn't found
            raise WordNotInNormsError(word)
        elif n_rows > 1:
            # More than one row: word wasn't a unique row identifier
            # Something has gone wrong!
            raise Exception()

        return [
            row.iloc[0][col_name]
            for col_name in SensorimotorNorms.DataColNames
        ]

    def matrix_for_words(self, words: List[str]):
        """
        Returns a data matrix of words-x-dims.
        :param words:
        :return:
        :raises: WordNotInNormsError
        """
        for word in words:
            if not self.has_word(word):
                raise WordNotInNormsError(word)
        data_for_words = self.data[self.data[ColNames.Word].isin(words)]
        return data_for_words[SensorimotorNorms.DataColNames].values
