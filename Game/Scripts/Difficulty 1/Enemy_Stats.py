enemies = {
    "Enemy Dumm": {
        "hp": 100,
        "attack": 10,
        "defense": 8,
        "resistance": 4,
        "special_attack": 15,
        # Add more stats as needed
    },
    "Goblin": {
        "hp": 60,
        "attack": 12,
        "defense": 5,
        "resistance": 2,
        "special_attack": 8,
    },
    "Orc": {
        "hp": 150,
        "attack": 18,
        "defense": 12,
        "resistance": 6,
        "special_attack": 20,
    },
    # Add more enemy types as needed
}

def get_enemy_stats(enemy_name):
    """Retrieve the stats for a given enemy."""
    return enemies.get(enemy_name, {"hp": 1, "attack": 1, "defense": 0, "resistance": 0, "special_attack": 0})
