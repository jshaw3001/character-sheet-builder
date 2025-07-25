def score_to_modifier(score: int) -> int:
    """Convert a score to a modifier. Scores range from 1 to 10, where 5 is the baseline (0 modifier). Each point above or below 5 increases or decreases the modifier by 1."""
    if not (1 <= score <= 10):
        raise ValueError("Ability scores must be between 1 and 10. Got: {}".format(score))
    return score - 5