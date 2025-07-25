import random
from logic.ability_modifier import score_to_modifier


def ability_roll(stat_value):
        """
        Rolls 1d20 + ability modifier for a given stat.
        stat_name: e.g. "Athletics"
        stat_value: integer value of the stat
        Returns the total roll result.
        """

        die_roll = random.randint(1, 20)
        modifier = score_to_modifier(stat_value)
        total = die_roll + modifier
        return die_roll, modifier, total
        # Returns (die_roll, modifier, total)