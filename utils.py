import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def get_code_topics():
    from topics import TOPICS_CODE

    TOPICS = TOPICS_CODE  # You can add topic lists here and return one list

    return TOPICS


def get_general_topics():
    from topics import TOPICS_GENERAL

    TOPICS = TOPICS_GENERAL  # You can add topic lists here and return one list

    return TOPICS
