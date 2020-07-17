from collections import defaultdict
from typing import Iterable, Dict, List, DefaultDict

from .dictionary.dialect_dictionary import ameng_to_breng


def select_best_translations(words: Iterable[str]) -> Dict[str, str]:
    # Best option for each case
    candidates: Dict[str, List[str]] = {
        word: ameng_to_breng.translations_for(word)
        for word in words
    }

    preferred: Dict[str, str] = {
        word: translations[0]
        for word, translations in candidates.items()
        # Drop those without translations
        if len(translations) > 0
    }

    # Check for collisions
    def check_for_collisions(_preferred: Dict[str, str]) -> DefaultDict[str, List[str]]:
        """Returns translation -> [words]."""
        # target -> source
        checked: Dict[str, str] = dict()
        collisions_: DefaultDict[str, List[str]] = defaultdict(list)
        for word, translation in _preferred.items():
            if translation in checked:
                if checked[translation] not in collisions_[translation]:
                    collisions_[translation].append(checked[translation])
                collisions_[translation].append(word)
            checked[translation] = word
        return collisions_

    collisions = check_for_collisions(preferred)
    # while collisions:
    #     ...

    # TODO: check for preferred examples already being in the norms

    # Select preferred source for each target
    # for word, translations in collisions:
    #     ...

    return preferred



def translate_to_breng(word: str) -> str:
    """Logic for applying BrEng translation to norms."""
    word = word.lower().strip()
    return ameng_to_breng.best_translation_for(word, allow_identical=True)
