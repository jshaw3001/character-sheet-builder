from data.classes import CharClass
from logic.skills import get_starting_skills_for_class

class Character:
    def __init__(self, name, char_class: CharClass, stats, level=1):
        self.name = name
        self.char_class = char_class
        self.stats = stats
        self.level = level
        self.skills = get_starting_skills_for_class(char_class)

    def validate(self):
        for key, val in self.stats.items():
            if not (1 <= val <= 10):
                raise ValueError(f"{key} must be 1 between and 10, got {val}")
    
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.char_class,
            "level": self.level,
            "stats": self.stats           
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            char_class=data["class"],
            stats=data["stats"],
            level=data.get("level", 1),
        )

