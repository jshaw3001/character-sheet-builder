import random
import re
from logic.ability_modifier import score_to_modifier

class Skill:
    def __init__(self, name, description, dice_formula):
        self.name = name
        self.description = description
        self.dice_formula = dice_formula

    def name(self):
        return f"{self.name}"
    
    def description(self):
        return f"{self.description}"
    
    def dice_formula(self):
        return f"{self.dice_formula}"

    def roll(self, stats):
        """
        stats:dict, e.g {"Athletics": 3, "Bravery": 2, ...}
        Returns the result of the Skill roll based on the dice formula and stats.
        """

        # Formula of the form "2d6+Athletics"
        match = re.match(r'(\d+)d(\d+)([+-]\w+)?', self.dice_formula)
        if not match:
            raise ValueError(f"Invalid dice formula: {self.dice_formula}")
        num_dice = int(match.group(1))
        die_sides = int(match.group(2))
        stat_name = match.group(3)
        # Roll the dice
        die_roll = sum(random.randint(1, die_sides) for _ in range(num_dice))
        # Add the stat bonus if applicable
        modifier = score_to_modifier(stats.get(stat_name[1:], 0)) if stat_name else 0
        # Calculate the total
        total = die_roll + modifier
        # Return the die roll, modifier, and total
        return die_roll, modifier, total

        

skills = {
    "Punch": Skill("Punch", "A rush of quick melee attacks.", "2d4+Athletics"),
    "Block": Skill("Dodge", "Increase movement speed and avoid opportunity attacks", "1d8+Athletics"),
    "Slash": Skill("Slash", "A quick cutting attack.", "1d8+Athletics"),
    "Parry": Skill("Parry", "Deflect an incoming attack.", "1d6+Bravery"),
    "Steal": Skill("Mug", "Attack and steal from an enemy", "1d6+Athletics"),
    "Hide": Skill("Hide", "Become unseen by enemies.", "1d4+Wit"),
    "Snipe": Skill("Snipe", "A long-range attack with a bow.", "1d8+Athletics"),
    "Friendship": Skill("Friendship", "Charm an enemy into becoming an ally.", "1d6+Charm"),
    "Shield Bash": Skill("Shield Bash", "Stun an enemy with a shield.", "1d6+Bravery"),
    "Guard": Skill("Guard", "Protect an ally from harm.", "1d6+Bravery"),
    "Heal": Skill("Heal", "Restore health to an ally.", "1d8+Wit"),
    "Smite": Skill("Smite", "Deal holy damage to an enemy.", "1d6+Wit"),
    "Inspire": Skill("Inspire", "Boost an ally's morale.", "1d4+Bravery"),
    "Command": Skill("Command", "Force an enemy to obey.", "1d6+Charm"),
    "Arcane Bolt": Skill("Arcane Bolt", "A basic magical attack.", "1d10+Wit"),
    "Arcane Shield": Skill("Arcane Shield", "Create a magical barrier.", "1d4+Wit"),
    "Illusion": Skill("Illusion", "Create a false image to deceive enemies.", "1d6+Wit"),
    "Disguise": Skill("Disguise", "Change appearance to blend in.", "1d4+Charm"),
    "Sing": Skill("Sing", "Perform a song to inspire or harm.", "1d6+Charm"),
    "Dance": Skill("Dance", "Perform a dance to charm or distract.", "1d4+Charm"),
}

class_skills = {
    "Brawler": ["Punch", "Block"],
    "Knight": ["Slash", "Parry"],
    "Thief": ["Steal", "Hide"],
    "Ranger": ["Snipe", "Friendship"],
    "Warden": ["Shield Bash", "Guard"],
    "Divine": ["Heal", "Smite"],
    "Tactician": ["Inspire", "Command"],
    "Wizard": ["Arcane Bolt", "Arcane Shield"],
    "Phantom": ["Illusion", "Disguise"],
    "Performer": ["Sing", "Dance"]
}

def get_starting_skills_for_class(char_class):
    skill_names = class_skills.get(char_class, [])
    return [skills[name] for name in skill_names if name in skills]
