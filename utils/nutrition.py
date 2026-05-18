from __future__ import annotations

# Resting Energy Requirement multipliers per species and health goal.
# Base RER = 70 * weight_kg^0.75 (standard veterinary formula).
_RER_FACTORS: dict[str, dict[str, float]] = {
    "Dog":    {"Maintenance": 1.6, "Weight Loss": 1.0, "Weight Gain": 1.8, "Senior Care": 1.4},
    "Cat":    {"Maintenance": 1.4, "Weight Loss": 0.8, "Weight Gain": 1.6, "Senior Care": 1.2},
    "Rabbit": {"Maintenance": 1.0, "Weight Loss": 0.85, "Weight Gain": 1.2, "Senior Care": 0.9},
    "Bird":   {"Maintenance": 1.0, "Weight Loss": 0.9,  "Weight Gain": 1.1, "Senior Care": 0.9},
    "Other":  {"Maintenance": 1.0, "Weight Loss": 0.85, "Weight Gain": 1.2, "Senior Care": 0.9},
}

_MEALS_PER_DAY: dict[str, int] = {
    "Dog": 2, "Cat": 2, "Rabbit": 3, "Bird": 3, "Other": 2,
}


def convert_weight_to_kg(weight_value: float, weight_unit: str) -> float:
    return weight_value * 0.453592 if weight_unit == "lbs" else float(weight_value)


def get_daily_calories(species: str, weight_kg: float, health_goal: str) -> int:
    rer = 70.0 * (weight_kg ** 0.75)
    factors = _RER_FACTORS.get(species, _RER_FACTORS["Other"])
    factor = factors.get(health_goal, 1.0)
    return max(1, round(rer * factor))


def get_portion_guidance(species: str, weight_kg: float, health_goal: str) -> dict:
    kcal = get_daily_calories(species, weight_kg, health_goal)
    meals = _MEALS_PER_DAY.get(species, 2)
    wet_g = round(kcal)           # ~1 kcal/g for wet/fresh food
    dry_g = round(kcal / 3.5)    # ~3.5 kcal/g for dry kibble
    return {
        "daily_kcal": kcal,
        "per_meal_kcal": round(kcal / meals),
        "wet_food_daily_g": wet_g,
        "wet_food_daily_oz": round(wet_g / 28.35, 1),
        "dry_food_daily_g": dry_g,
        "dry_food_daily_oz": round(dry_g / 28.35, 1),
        "meals_per_day": meals,
    }
