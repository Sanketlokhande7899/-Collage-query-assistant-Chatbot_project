from difflib import SequenceMatcher


def calculate_similarity(text1, text2):
    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()