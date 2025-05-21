def get_player_stats(level):
    level = max(1, min(100, level))
    return {
        "hp": 8 + (level * 2), 
        "attack": 1 + (level // 15), 
        "special_attack": 5 + (level // 10) 
    }
player_stats = get_player_stats(1)

