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

    word = "Word"

    # Motor
    head          = "Head.mean"
    mouth         = "Mouth.mean"
    hand          = "Hand_arm.mean"
    foot          = "Foot_leg.mean"
    torso         = "Torso.mean"

    # Sensory
    touch         = "Haptic.mean"
    hearing       = "Auditory.mean"
    seeing        = "Visual.mean"
    smelling      = "Olfactory.mean"
    tasting       = "Gustatory.mean"
    interoception = "Interoceptive.mean"

    # Other stats
    n_known_perceptual = "N_known.perceptual"
    n_list_perceptual  = "List_N.perceptual"
    n_known_action     = "N_known.action"
    n_list_action      = "List_N.action"


class SensorimotorNorms(object):

    VectorColNames = [
        # Sensory
        ColNames.touch, ColNames.hearing, ColNames.seeing, ColNames.smelling, ColNames.tasting, ColNames.interoception,
        # Motor
        ColNames.head, ColNames.mouth, ColNames.hand, ColNames.foot, ColNames.torso,
    ]

    def __init__(self):
        self.data: DataFrame = read_csv(Preferences.sensorimotor_norms_path, index_col=None, header=0,
                                        # Prevent the "nan" item from being interpreted as a NaN
                                        dtype={ColNames.word: str}, keep_default_na=False)

        # Trim whitespace and convert words to lower case
        self.data[ColNames.word] = self.data[ColNames.word].str.strip()
        self.data[ColNames.word] = self.data[ColNames.word].str.lower()

        self._words: set = set(self.data[ColNames.word])

    def iter_words(self) -> Iterable[str]:
        for word in self.data[ColNames.word]:
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
        row = self.data[self.data[ColNames.word] == word]

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
            for col_name in SensorimotorNorms.VectorColNames
        ]

    def fraction_known(self, word: str) -> float:
        """
        Returns the fraction of participants who knew a word.
        :param word:
        :return:
            Prevalence of the word
        :raises: WordNotInNormsError
            When the requested word is not in the norms
        """
        row = self.data[self.data[ColNames.word] == word]

        # Make sure we only got one row
        n_rows = row.shape[0]
        if n_rows is 0:
            # No rows: word wasn't found
            raise WordNotInNormsError(word)
        elif n_rows > 1:
            # More than one row: word wasn't a unique row identifier
            # Something has gone wrong!
            raise Exception()

        n_known_perceptual = row.iloc[0][ColNames.n_known_perceptual]
        n_list_perceptual  = row.iloc[0][ColNames.n_list_perceptual]
        n_known_action     = row.iloc[0][ColNames.n_known_action]
        n_list_action      = row.iloc[0][ColNames.n_list_action]

        return (n_known_perceptual + n_known_action) / (n_list_perceptual + n_list_action)

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
        data_for_words = self.data[self.data[ColNames.word].isin(words)]
        return data_for_words[SensorimotorNorms.VectorColNames].values
