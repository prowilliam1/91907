def get_player1_stats(level):
    level = max(1, min(100, level))
    return {
        "hp": 18 + (level * 2),
        "attack": 9 + (level),
        "special_attack": 14 + (level),
        "defense": 4 + (level),
        "resistance": 4 + (level),
    }

def get_player2_stats(level):
    level = max(1, min(100, level))
    return {
        "hp": 22 + (level * 2),
        "attack": 7 + (level),
        "special_attack": 10 + (level),
        "defense": 7 + (level),
        "resistance": 6 + (level),
    }

def get_player3_stats(level):
    level = max(1, min(100, level))
    return {
        "hp": 15 + (level * 2),
        "attack": 13 + (level),
        "special_attack": 8 + (level),
        "defense": 3 + (level),
        "resistance": 5 + (level),
    }

def get_player4_stats(level):
    level = max(1, min(100, level))
    return {
        "hp": 17 + (level * 2),
        "attack": 8 + (level),
        "special_attack": 18 + (level),
        "defense": 5 + (level),
        "resistance": 8 + (level),
    }

