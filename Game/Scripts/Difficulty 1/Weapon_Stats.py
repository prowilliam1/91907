import random

weapons = {
    "Sword": {"attack": 1, "special_attack": 1, "special_equation": lambda x, y: x + y},
    "Axe": {"attack": 15, "special_attack": 2, "special_equation": lambda x, y: x * y},
    "Bow": {"attack": 8, "special_attack": 10, "special_equation": lambda x, y: x - y},
    "Dagger": {"attack": 5, "special_attack": 15, "special_equation": lambda x, y: x // y if y != 0 else 0},
}

def get_weapon_stats(weapon_name):
    """Retrieve the stats for a given weapon."""
    return weapons.get(weapon_name, {"attack": 0, "special_attack": 0, "special_equation": lambda x, y: 0})

special_questions = {
    "Sword": [
        {
            "question": lambda x, y, v, w, z: f"{x}x + {y} + {w}^{v} = {z}",
            "answer": lambda x, y, v, w, z: (z - y - w**v) // x,
            "adjust_z": lambda x, y, v, w: x * random.randint(1, 10) + y + w**v,
        },
        {
            "question": lambda x, y, v, w, z: f"{x}x + {y} + {w}^{v} = {z}",
            "answer": lambda x, y, v, w, z: (z - y - w**v) // x,
            "adjust_z": lambda x, y, v, w: x * random.randint(1, 10) + y + w**v, 
        },
    ],
    "Axe": [
        {"question": lambda x, y, w: f"{x} * {y} + {w}", "answer": lambda x, y, w: x * y + w},
        {"question": lambda x, y, z: f"{x} + {y} - {z}", "answer": lambda x, y, z: x + y - z},
    ],
    "Bow": [
        {"question": lambda x, y, v: f"{x} - {y} + {v}", "answer": lambda x, y, v: x - y + v},
        {"question": lambda x, y, w: f"{x} // {y} + {w} (integer division)", "answer": lambda x, y, w: x // y + w if y != 0 else 0},
    ],
    "Dagger": [
        {"question": lambda x, y, z: f"{x} // {y} - {z} (integer division)", "answer": lambda x, y, z: x // y - z if y != 0 else 0},
        {"question": lambda x, y, v: f"{x} * {y} + {v}", "answer": lambda x, y, v: x * y + v},
    ],
}

def get_special_question(weapon_name):
    """Retrieve a random special question logic for a given weapon."""
    questions = special_questions.get(weapon_name, [])
    return random.choice(questions) if questions else {"question": lambda x, y, v, w, z: "", "answer": lambda x, y, v, w, z: 0, "adjust_z": lambda x, y, v, w: 0}
