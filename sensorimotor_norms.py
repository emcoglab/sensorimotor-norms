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

    # Derived stats
    fraction_known = "Fraction.known"


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

        # Convert word column to index
        self.data.set_index(ColNames.word, inplace=True, drop=False)

        # Add computed columns

        self.data[ColNames.fraction_known] = (self.data[ColNames.n_known_perceptual] + self.data[ColNames.n_known_action]) / (self.data[ColNames.n_list_perceptual] + self.data[ColNames.n_list_action])

    def iter_words(self) -> Iterable[str]:
        for word in self.data.index:
            yield word

    def has_word(self, word: str) -> bool:
        """True if a word is in the norms, else False."""
        return word in self.data.index

    def vector_for_word(self, word: str) -> List[float]:
        """
        A vector of sensorimotor data associated with each word.
        :param word:
        :return:
        :raises: WordNotInNormsError
        """
        try:
            data_for_word = self.data.loc[word]
        except KeyError:
            raise WordNotInNormsError(word)

        return list(data_for_word[SensorimotorNorms.VectorColNames])

    def fraction_known(self, word: str) -> float:
        """
        Returns the fraction of participants who knew a word.
        :param word:
        :return:
            Fraction of participants who knew the word.
            This is guaranteed to be in the range [0, 1].
        :raises: WordNotInNormsError
            When the requested word is not in the norms
        """
        try:
            data_for_word = self.data.loc[word]
        except KeyError:
            raise WordNotInNormsError(word)

        return data_for_word[ColNames.fraction_known]

    def matrix_for_words(self, words: List[str]):
        """
        Returns a data matrix of words-x-dims.
        :param words:
        :return:
        :raises: WordNotInNormsError
        """
        try:
            data_for_words = self.data.loc[words]
        except KeyError as er:
            raise WordNotInNormsError(er.args[0])
        return data_for_words[SensorimotorNorms.VectorColNames].values
