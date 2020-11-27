from collections import defaultdict
from typing import Iterable, Dict
from logging import getLogger

from .dictionary.dialect_dictionary import ameng_to_breng
from .dictionary.vocabulary import ameng_counter, breng_counter

logger = getLogger(__name__)


def select_best_translations(words: Iterable[str], verbose: bool = False) -> Dict[str, str]:
    """

    :param words:
    :return:
    :raises: ValueError
    """

    # The final translations
    translations: Dict[str, str] = dict()

    # Select best translations
    for word in words:
        # Where the norm is untranslatable, we leave as-is
        if word not in ameng_to_breng.source_vocab:
            translations[word] = word
            continue

        # Otherwise we go with the best translation
        available_translations = ameng_to_breng.translations_for(word)
        translations_were_available = len(available_translations) > 0
        # Disallow translations to a word which are already in the norms
        available_translations = [
            t
            for t in available_translations
            if t not in words
        ]

        # If the word is untranslatable, we leave as-is
        if len(available_translations) == 0:
            if translations_were_available and verbose:
                logger.info(f"Tried to translate {word} but all translations already supplied: {', '.join(ameng_to_breng.translations_for(word))}")
            translations[word] = word
            continue

        # Pick the best translation
        for t in available_translations:
            # Disallow translations to a word which is already in the norms
            if t in words:
                continue
            translations[word] = t
            break

        # If we exhausted translations, just don't translate
        if word not in translations:
            if verbose:
                logger.info(f"Exhausted translation options for {word}")
            translations[word] = word

    collisions = find_collisions(translations)

    collision_avoidance = dict()
    for target, sources in collisions.items():
        if verbose:
            logger.info(f"Collision wit {', '.join(sources)} all pointing to {target}. Trying to avoid...")
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
    collisions = find_collisions(translations)
    assert len(collisions) == 0

    return translations


def find_collisions(translations):
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
