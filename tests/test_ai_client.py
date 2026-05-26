"""Tests for utils/ai_client.py — prompt building and allergy/toxic filtering."""
import pytest
from utils.ai_client import _build_prompt, _parse_response, _TOXIC
from utils.nutrition import get_portion_guidance


def _make_profile(**overrides):
    base = {
        "species": "Dog",
        "breed": "Labrador",
        "age_value": 3.0,
        "age_unit": "years",
        "weight_value": 15.0,
        "weight_unit": "kg",
        "allergies": [],
        "health_goal": "Maintenance",
    }
    base.update(overrides)
    return base


def _portions(profile):
    return get_portion_guidance(profile["species"], profile["weight_value"], profile["health_goal"])


class TestBuildPrompt:
    def test_contains_species(self):
        profile = _make_profile()
        prompt = _build_prompt(profile, _portions(profile))
        assert "Dog" in prompt

    def test_contains_breed(self):
        profile = _make_profile(breed="Labrador")
        prompt = _build_prompt(profile, _portions(profile))
        assert "Labrador" in prompt

    def test_user_allergy_in_forbidden_list(self):
        profile = _make_profile(allergies=["chicken"])
        prompt = _build_prompt(profile, _portions(profile))
        assert "chicken" in prompt

    def test_species_toxic_foods_in_forbidden_list(self):
        profile = _make_profile(species="Dog")
        prompt = _build_prompt(profile, _portions(profile))
        for toxic in _TOXIC["Dog"]:
            assert toxic in prompt

    def test_health_goal_included(self):
        profile = _make_profile(health_goal="Weight Loss")
        prompt = _build_prompt(profile, _portions(profile))
        assert "Weight Loss" in prompt

    def test_json_structure_requested(self):
        profile = _make_profile()
        prompt = _build_prompt(profile, _portions(profile))
        assert '"days"' in prompt


class TestParseResponse:
    def _make_plan_json(self, days=7, meals_per_day=2):
        days_data = []
        for d in range(1, days + 1):
            meals = [
                {
                    "name": f"Meal {m}",
                    "ingredients": ["chicken 100g"],
                    "portion_g": 200,
                    "portion_oz": 7.1,
                    "notes": "",
                }
                for m in range(1, meals_per_day + 1)
            ]
            days_data.append({"day": d, "meals": meals, "daily_notes": ""})
        import json
        return json.dumps({"days": days_data})

    def test_valid_json_parsed(self):
        result = _parse_response(self._make_plan_json())
        assert "days" in result
        assert len(result["days"]) == 7

    def test_strips_markdown_fences(self):
        raw = "```json\n" + self._make_plan_json() + "\n```"
        result = _parse_response(raw)
        assert len(result["days"]) == 7

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError, match="invalid JSON"):
            _parse_response("not json at all")

    def test_wrong_day_count_raises(self):
        import json
        bad = json.dumps({"days": [{"day": 1, "meals": []}]})
        with pytest.raises(ValueError, match="7 days"):
            _parse_response(bad)
