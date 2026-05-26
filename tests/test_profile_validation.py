"""
Tests for profile validation logic and Bug 3 (stale plan detection).

These tests cover the rules enforced in pages/1_profile.py (validation) and
the _is_plan_stale helper logic introduced in pages/2_meal_plan.py.
Because both live in Streamlit pages we extract the pure logic and test it
without importing Streamlit.
"""
import pytest


# ── Reusable helpers (mirrors the logic in the pages) ─────────────────────────

def _validate_profile(species, breed, age_value, weight_value, health_goal):
    """Returns list of error strings, empty means valid."""
    errors = []
    if not species:
        errors.append("Species is required.")
    if not breed or not breed.strip():
        errors.append("Breed is required.")
    if age_value is None:
        errors.append("Age is required.")
    elif age_value <= 0:
        errors.append("Age must be greater than 0.")
    if weight_value is None:
        errors.append("Weight is required.")
    elif weight_value <= 0:
        errors.append("Weight must be greater than 0.")
    if not health_goal:
        errors.append("Health Goal is required.")
    return errors


def _is_plan_stale(plan: dict, profile: dict) -> bool:
    """Mirrors _is_plan_stale from pages/2_meal_plan.py."""
    snap = plan.get("_profile_snapshot")
    if not snap:
        return False
    fields = ("species", "health_goal", "weight_value", "weight_unit", "age_value", "age_unit")
    return any(str(snap.get(f)) != str(profile.get(f)) for f in fields)


# ── Bug 1 & 2: zero weight and age rejected ────────────────────────────────────

class TestProfileValidation:
    def test_valid_profile_passes(self):
        errs = _validate_profile("Dog", "Labrador", 3.0, 10.0, "Maintenance")
        assert errs == []

    def test_zero_weight_rejected(self):
        errs = _validate_profile("Dog", "Labrador", 3.0, 0.0, "Maintenance")
        assert any("Weight" in e for e in errs)

    def test_negative_weight_rejected(self):
        errs = _validate_profile("Dog", "Labrador", 3.0, -1.0, "Maintenance")
        assert any("Weight" in e for e in errs)

    def test_zero_age_rejected(self):
        errs = _validate_profile("Dog", "Labrador", 0.0, 10.0, "Maintenance")
        assert any("Age" in e for e in errs)

    def test_negative_age_rejected(self):
        errs = _validate_profile("Dog", "Labrador", -1.0, 10.0, "Maintenance")
        assert any("Age" in e for e in errs)

    def test_missing_species_rejected(self):
        errs = _validate_profile("", "Labrador", 3.0, 10.0, "Maintenance")
        assert any("Species" in e for e in errs)

    def test_missing_breed_rejected(self):
        errs = _validate_profile("Dog", "  ", 3.0, 10.0, "Maintenance")
        assert any("Breed" in e for e in errs)

    def test_missing_health_goal_rejected(self):
        errs = _validate_profile("Dog", "Labrador", 3.0, 10.0, "")
        assert any("Health Goal" in e for e in errs)

    def test_multiple_errors_all_reported(self):
        errs = _validate_profile("", "", None, None, "")
        assert len(errs) >= 3


# ── Bug 3: stale plan detection ───────────────────────────────────────────────

class TestStalePlanDetection:
    def _make_plan(self, **snap_overrides):
        snap = {
            "species": "Dog",
            "health_goal": "Maintenance",
            "weight_value": 10.0,
            "weight_unit": "kg",
            "age_value": 3.0,
            "age_unit": "years",
        }
        snap.update(snap_overrides)
        return {"days": [], "_profile_snapshot": snap}

    def _make_profile(self, **overrides):
        base = {
            "species": "Dog",
            "health_goal": "Maintenance",
            "weight_value": 10.0,
            "weight_unit": "kg",
            "age_value": 3.0,
            "age_unit": "years",
        }
        base.update(overrides)
        return base

    def test_matching_snapshot_not_stale(self):
        plan = self._make_plan()
        profile = self._make_profile()
        assert not _is_plan_stale(plan, profile)

    def test_species_change_is_stale(self):
        plan = self._make_plan(species="Dog")
        profile = self._make_profile(species="Cat")
        assert _is_plan_stale(plan, profile)

    def test_health_goal_change_is_stale(self):
        plan = self._make_plan(health_goal="Maintenance")
        profile = self._make_profile(health_goal="Weight Loss")
        assert _is_plan_stale(plan, profile)

    def test_weight_change_is_stale(self):
        plan = self._make_plan(weight_value=10.0)
        profile = self._make_profile(weight_value=15.0)
        assert _is_plan_stale(plan, profile)

    def test_weight_unit_change_is_stale(self):
        plan = self._make_plan(weight_unit="kg")
        profile = self._make_profile(weight_unit="lbs")
        assert _is_plan_stale(plan, profile)

    def test_name_only_change_not_stale(self):
        """Changing only name/breed doesn't affect nutrition — plan stays valid."""
        plan = self._make_plan()
        profile = self._make_profile()
        profile["name"] = "NewName"
        profile["breed"] = "Poodle"
        assert not _is_plan_stale(plan, profile)

    def test_plan_without_snapshot_not_stale(self):
        """Older plans with no snapshot are treated as non-stale (no false positives)."""
        plan = {"days": []}  # no _profile_snapshot key
        profile = self._make_profile()
        assert not _is_plan_stale(plan, profile)
