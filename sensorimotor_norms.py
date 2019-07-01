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
from random import randint
from typing import List, Iterable

from pandas import DataFrame, read_csv

from .exceptions import WordNotInNormsError
from .config.preferences import Preferences


class DataColNames(object):
    """Column names used in sensorimotor data file."""

    word = "Word"

    # region Mean

    # Sensory
    hearing       = "Auditory.mean"
    tasting       = "Gustatory.mean"
    touch         = "Haptic.mean"
    interoception = "Interoceptive.mean"
    smelling      = "Olfactory.mean"
    seeing        = "Visual.mean"

    # Motor
    foot          = "Foot_leg.mean"
    hand          = "Hand_arm.mean"
    head          = "Head.mean"
    mouth         = "Mouth.mean"
    torso         = "Torso.mean"

    # endregion

    # region SD

    # Sensory
    hearing_sd       = "Auditory.SD"
    tasting_sd       = "Gustatory.SD"
    touch_sd         = "Haptic.SD"
    interoception_sd = "Interoceptive.SD"
    smelling_sd      = "Olfactory.SD"
    seeing_sd        = "Visual.SD"

    # Motor
    foot_sd          = "Foot_leg.SD"
    hand_sd          = "Hand_arm.SD"
    head_sd          = "Head.SD"
    mouth_sd         = "Mouth.SD"
    torso_sd         = "Torso.SD"

    # endregion

    # region Other stats

    max_strength_perceptual   = "Max_strength.perceptual"
    minkowski3_perceptual     = "Minkowski3.perceptual"
    exclusivity_perceptual    = "Exclusivity.perceptual"
    dominant_perceptual       = "Dominant.perceptual"
    max_strength_action       = "Max_strength.action"
    minkowski3_action         = "Minkowski3.action"
    exclusivity_action        = "Exclusivity.action"
    dominant_action           = "Dominant.action"
    max_strength_sensorimotor = "Max_strength.sensorimotor"
    minkowski3_sensorimotor   = "Minkowski3.sensorimotor"
    exclusivity_sensorimotor  = "Exclusivity.sensorimotor"
    dominant_sensorimotor     = "Dominant.sensorimotor"

    n_known_perceptual = "N_known.perceptual"
    n_list_perceptual  = "List_N.perceptual"
    n_known_action     = "N_known.action"
    n_list_action      = "List_N.action"

    percentage_known_perceptual = "Percent_known.perceptual"
    percentage_known_action     = "Percentage_known.action"
    mean_age_perceptual         = "Mean_age.perceptual"
    mean_age_action             = "Mean_age.action"
    list_no_perceptual          = "List#.perceptual"
    list_no_action              = "List#.action"

    # endregion


class ComputedColNames(object):
    """Additional queryable columns which are computed on load"""

    fraction_known = "Percentage_known.sensorimotor"


class SensorimotorNorms(object):

    SensoryColNames = [
        DataColNames.hearing,
        DataColNames.tasting,
        DataColNames.touch,
        DataColNames.interoception,
        DataColNames.smelling,
        DataColNames.seeing,
    ]

    SensorySDColNames = [
        DataColNames.hearing_sd,
        DataColNames.tasting_sd,
        DataColNames.touch_sd,
        DataColNames.interoception_sd,
        DataColNames.smelling_sd,
        DataColNames.seeing_sd,
    ]

    MotorColNames = [
        DataColNames.foot,
        DataColNames.hand,
        DataColNames.head,
        DataColNames.mouth,
        DataColNames.torso,
    ]

    MotorSDColNames = [
        DataColNames.foot_sd,
        DataColNames.hand_sd,
        DataColNames.head_sd,
        DataColNames.mouth_sd,
        DataColNames.torso_sd,
    ]

    VectorColNames = SensoryColNames + MotorColNames

    def __init__(self):
        self.data: DataFrame = read_csv(Preferences.sensorimotor_norms_path,
                                        index_col=None, header=0,
                                        dtype={
                                            # Prevent the "nan" item from being interpreted as a NaN
                                            DataColNames.word: str,
                                            DataColNames.n_known_action: int,
                                            DataColNames.n_known_perceptual: int,
                                            DataColNames.n_list_action: int,
                                            DataColNames.n_list_perceptual: int,
                                        },
                                        keep_default_na=False)

        # Trim whitespace and convert words to lower case
        self.data[DataColNames.word] = self.data[DataColNames.word].str.strip()
        self.data[DataColNames.word] = self.data[DataColNames.word].str.lower()

        # Convert word column to index
        self.data.set_index(DataColNames.word, inplace=True, drop=False)

        # region Add computed columns

        self.data[ComputedColNames.fraction_known] = (self.data[DataColNames.n_known_perceptual] + self.data[DataColNames.n_known_action]) / (self.data[DataColNames.n_list_perceptual] + self.data[DataColNames.n_list_action])

        # endregion

        self.n_items = len(list(self.iter_words()))
        self.n_dims = len(self.VectorColNames)

    def iter_words(self) -> Iterable[str]:
        for word in self.data.index:
            yield word

    def random_word(self) -> str:
        return self.data[DataColNames.word].iloc[randint(0, self.n_items-1)]

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

        return data_for_word[ComputedColNames.fraction_known]

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
