ABILITY_NAMES = ["Athletics", "Bravery", "Wit", "Charm"]
POINT_POOL = 8

def point_cost(score):
    if score < 4:
        return 0
    elif 4 <= score <= 6:
        return score -4
    elif 7 <= score <= 8:
        return 2 * (score - 6) + 2
    else:
        return float('inf')

def total_points_spent(scores):
    return sum(point_cost(val) for val in scores.values())

def remaining_points(scores):
    return POINT_POOL - total_points_spent(scores)