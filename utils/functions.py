from difflib import SequenceMatcher


def similarity_ratio(original, found):
    return round(SequenceMatcher(None, original, found).ratio() * 100)
