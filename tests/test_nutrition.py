"""Tests for utils/nutrition.py — portion size and caloric calculations."""
import pytest
from utils.nutrition import convert_weight_to_kg, get_daily_calories, get_portion_guidance


class TestConvertWeightToKg:
    def test_kg_unchanged(self):
        assert convert_weight_to_kg(10.0, "kg") == 10.0

    def test_lbs_conversion(self):
        result = convert_weight_to_kg(22.0, "lbs")
        assert abs(result - 9.979) < 0.01

    def test_zero_weight(self):
        assert convert_weight_to_kg(0.0, "kg") == 0.0


class TestGetDailyCalories:
    def test_dog_maintenance_positive(self):
        kcal = get_daily_calories("Dog", 10.0, "Maintenance")
        assert kcal > 0

    def test_weight_loss_less_than_maintenance(self):
        maintenance = get_daily_calories("Dog", 10.0, "Maintenance")
        loss = get_daily_calories("Dog", 10.0, "Weight Loss")
        assert loss < maintenance

    def test_weight_gain_more_than_maintenance(self):
        maintenance = get_daily_calories("Dog", 10.0, "Maintenance")
        gain = get_daily_calories("Dog", 10.0, "Weight Gain")
        assert gain > maintenance

    def test_heavier_pet_needs_more_calories(self):
        light = get_daily_calories("Dog", 5.0, "Maintenance")
        heavy = get_daily_calories("Dog", 20.0, "Maintenance")
        assert heavy > light

    def test_minimum_one_kcal(self):
        # Even with weight=0 guard in nutrition, result must be >= 1
        assert get_daily_calories("Dog", 0.001, "Maintenance") >= 1

    def test_cat_reasonable_range(self):
        kcal = get_daily_calories("Cat", 4.0, "Maintenance")
        assert 150 < kcal < 500

    def test_unknown_species_falls_back(self):
        kcal = get_daily_calories("Other", 5.0, "Maintenance")
        assert kcal > 0


class TestGetPortionGuidance:
    def test_returns_required_keys(self):
        result = get_portion_guidance("Dog", 10.0, "Maintenance")
        for key in ("daily_kcal", "per_meal_kcal", "wet_food_daily_g",
                    "dry_food_daily_g", "meals_per_day"):
            assert key in result

    def test_dry_food_less_than_wet(self):
        result = get_portion_guidance("Dog", 10.0, "Maintenance")
        assert result["dry_food_daily_g"] < result["wet_food_daily_g"]

    def test_dog_two_meals_per_day(self):
        result = get_portion_guidance("Dog", 10.0, "Maintenance")
        assert result["meals_per_day"] == 2

    def test_rabbit_three_meals_per_day(self):
        result = get_portion_guidance("Rabbit", 2.0, "Maintenance")
        assert result["meals_per_day"] == 3
