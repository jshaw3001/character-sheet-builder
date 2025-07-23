class Character:
    def __init__(self, name, char_class, stats):
        self.name = name
        self.char_class = char_class
        self.stats = stats

    def validate(self):
        for key, val in self.stats.items():
            if not (1 <= val <= 20):
                raise ValueError(f"{key} must be between 1 and 20")
    
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.char_class,
            "stats": self.stats
        }