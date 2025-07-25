from enum import Enum

class CharClass(Enum):
    BRAWLER = "Brawler"
    KNIGHT = "Knight"
    THIEF = "Thief"
    RANGER = "Ranger"
    WARDEN = "Warden"
    DIVINE = "Divine"
    TACTICIAN = "Tactician"
    WIZARD = "Wizard"
    PHANTOM = "Phantom"
    PERFORMER = "Performer"

classes = {
    CharClass.BRAWLER: {
        "abilities": ["Athletics"],
        "description": "A fierce melee combatant who's body is their weapon."
    },
    CharClass.KNIGHT: {
        "abilities": ["Athletics", "Bravery"],
        "description": "A mighty warrior striving for perfection in armed combat."
    },
    CharClass.THIEF: {
        "abilities": ["Athletics", "Wit"],
        "description": "A cloaked dagger in the dark, expert of stealth."
    },
    CharClass.RANGER: {
        "abilities": ["Athletics", "Charm"],
        "description": "A versatile hunter who's charms are irresistible to even the wildest of beasts."
    },
    CharClass.WARDEN: {
        "abilities": ["Bravery"],
        "description": "A stoic wall of steel, guarding allies with unshakable resolve."
    },
    CharClass.DIVINE: {
        "abilities": ["Bravery", "Wit"],
        "description": "A vessel of sacred power, wielding divine judgment and healing."
    },
    CharClass.TACTICIAN: {
        "abilities": ["Bravery", "Charm"],
        "description": "A dominating presence who drives allies to victory through sheer force of will."
    },
    CharClass.WIZARD: {
        "abilities": ["Wit"],
        "description": "A scholar of arcane mysteries, master of raw magical power."
    },
    CharClass.PHANTOM: {
        "abilities": ["Wit", "Charm"],
        "description": "A mysterious illusionist who blends charm with deception."
    },
    CharClass.PERFORMER: {
        "abilities": ["Charm"],
        "description": "A bard who's magnetic presence keeps them center stage."
    }
}

