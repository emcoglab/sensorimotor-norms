from collections import defaultdict
from typing import Iterable, Dict, Set
from logging import getLogger

from .dictionary.dialect_dictionary import ameng_to_breng
from .dictionary.vocabulary import ameng_counter, breng_counter

logger = getLogger(__name__)


def _select_best_translation(word: str, other_words: Set[str], verbose: bool = False) -> str:

    available_translations = ameng_to_breng.translations_for(word)
    translations_were_available = len(available_translations) > 0
    available_translations = [
        t
        for t in available_translations
        # Disallow translations to a word which are already in the norms
        if t not in other_words
    ]

    # If the word is untranslatable, we leave as-is
    if len(available_translations) == 0:
        if translations_were_available and verbose:
            logger.info(f"Tried to translate {word} but all translations already supplied: "
                        f"{', '.join(ameng_to_breng.translations_for(word))}")
        return word

    # Pick the best translation
    for t in available_translations:
        # Disallow translations to a word which is already in the norms
        if t in other_words:
            continue
        return t

    # If we exhausted translations, just don't translate
    if verbose:
        logger.info(f"Exhausted translation options for {word}")
    return word


def select_best_translations(words: Iterable[str], verbose: bool = False) -> Dict[str, str]:
    """
    Selects the single best translation for each of the words in the input
    :param words:
    :return:
    :raises: ValueError
    """

    words = set(words)

    # The final translations
    translations: Dict[str, str] = dict()

    # Select best translations
    for word in words:

        # Translate directly where we can use the dictionary to do so
        if word in ameng_to_breng.source_vocab:
            translations[word] = _select_best_translation(word, other_words=words-{word}, verbose=verbose)

        # If we can't use the dictionary directly, we try and break the word up into tokens and use the dictionary on
        # those
        elif " " in word:
            # It's a multi-word term
            tokens = word.split(" ")
            translated_tokens = []
            for token in tokens:
                translated_tokens.append(_select_best_translation(token, set()))
            translated_multiword = " ".join(translated_tokens)
            # Make sure we don't generate a collision
            translations[word] = translated_multiword if translated_multiword not in words else word

        # Otherwise it's an untranslatable single word, there's nothing further we can do
        else:
            translations[word] = word

    collisions = _find_collisions(translations)

    collision_avoidance = dict()
    for target, sources in collisions.items():
        if verbose:
            logger.info(f"Collision found: {', '.join(sources)} all point to {target}. Trying to avoid...")
        # Order source words by AmEng dominance
        sources = sorted(sources, key=lambda w: ameng_counter[w], reverse=True)
        for source in sources:
            # By default, the dictionary won't offer "anesthetise" as a translation for "anaesthetise".
            # So we have to pool translations of the collision sources.
            available_translations = {
                t
                for s in sources
                for t in ameng_to_breng.translations_for(s)
            }
            # Don't accidentally cause another collision
            available_translations = [
                t
                for t in available_translations
                if (t not in words) and (t not in collision_avoidance.values())
            ]
            # Pick the best one available
            available_translations = sorted(available_translations, key=lambda w: breng_counter[w], reverse=True)

            for t in available_translations:
                collision_avoidance[source] = t
                break
            # If we didn't avoid collisions, just bail on translating it
            if source not in collision_avoidance:
                if verbose:
                    logger.info(f"Ran out of collision avoidance options for {source}")
                collision_avoidance[source] = source

    # Apply collision avoidance
    for s, t in collision_avoidance.items():
        translations[s] = t

    # Make sure we're done
    collisions = _find_collisions(translations)
    assert len(collisions) == 0

    return translations


def _find_collisions(translations):
    """Finds examples where multiple sources end in the same target."""
    # target -> source
    collisions = defaultdict(list)
    for k, v in translations.items():
        collisions[v].append(k)
    # Forget the cases where there aren't any collisions
    forget = []
    for target, sources in collisions.items():
        if len(sources) == 1:
            forget.append(target)
    for target in forget:
        del collisions[target]
    return collisions
