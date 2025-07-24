class Character:
    def __init__(self, name, char_class, stats, level=1):
        self.name = name
        self.char_class = char_class
        self.stats = stats
        self.level = level

    def validate(self):
        for key, val in self.stats.items():
            if not (4 <= val <= 8):
                raise ValueError(f"{key} must be 4 between and 8")
    
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.char_class,
            "level": self.level,
            "stats": self.stats,            
        }