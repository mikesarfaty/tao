WHITESPACE_CHARS = set([" ", "\t", "\n", "\v", "\r", "\f"])


def split_leading_whitespace(line):
    """
    Splits a string into two parts: the part before non-whitespace characters begin, and the part after

    Returns: (str, str) or (WhitespaceString, AfterWhitespaceString)
    """
    leading_whitespace = ""
    idx = 0
    while line[idx] in WHITESPACE_CHARS and idx <= len(line):
        leading_whitespace += line[idx]
        idx += 1

    return leading_whitespace, line[idx:]
