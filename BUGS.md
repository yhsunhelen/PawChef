# Bug Report — PawChef

## Bug 1 — Weight = 0 Bypasses Form Validation ✅ Fixed

**File:** `Final/pages/1_profile.py`
**Severity:** Medium
**Status:** Fixed in current code

**Description:**
The weight field accepted `0` as a valid value, allowing submission and producing a nonsensical 1 kcal/day plan.

**Fix:**
`pages/1_profile.py` validation block contains:
```python
elif weight_value <= 0:
    errors.append("Weight must be greater than 0.")
```
This check catches both `0` and negative values before saving. The `st.number_input` uses `min_value=0.0` so the widget prevents negatives at the UI level; the backend guard catches the exact-zero edge case.

---

## Bug 2 — Age = 0 Bypasses Form Validation ✅ Fixed

**File:** `Final/pages/1_profile.py`
**Severity:** Low
**Status:** Fixed in current code

**Description:**
Same issue as Bug 1 for the Age field.

**Fix:**
`pages/1_profile.py` validation block contains:
```python
elif age_value <= 0:
    errors.append("Age must be greater than 0.")
```

---

## Bug 3 — Stale Meal Plan Shown After Profile Update ✅ Fixed

**File:** `Final/pages/1_profile.py`, `Final/pages/2_meal_plan.py`
**Severity:** Medium
**Status:** Fixed

**Description:**
If a meal plan was generated and the user later edited the pet's profile (e.g., changed species Dog → Cat, or updated health goal/weight), the Meal Plan page continued to display the old plan with no indication it was stale.

**Fix (two-layer):**

1. **Auto-clear on save** (`pages/1_profile.py`): When an edit saves with any change to `species`, `health_goal`, `weight_value`, `weight_unit`, `age_value`, or `age_unit`, the stored plan for that pet is immediately deleted from `meal_plans` and the user sees an info message: *"Profile changed — the previous meal plan was cleared."*

2. **Staleness banner** (`pages/2_meal_plan.py`): Every newly generated plan stores a `_profile_snapshot` dict. On load, `_is_plan_stale()` compares the snapshot against the current profile. If they differ, a yellow warning is shown: *"This plan was generated before the profile was updated. Click Regenerate below."*

---

## Bug 4 — Invalid DeepSeek Key Blocks Valid Anthropic Key ✅ Fixed

**File:** `Final/utils/ai_client.py`
**Severity:** High
**Status:** Fixed in current code

**Description:**
When `DEEPSEEK_API_KEY` was set but invalid, a 401 error was raised and the Anthropic key was never tried.

**Fix:**
`utils/ai_client.py` wraps the DeepSeek call in a `try/except` that falls back to Anthropic on any exception:
```python
if deepseek_key:
    try:
        raw = _call_deepseek(prompt, deepseek_key)
    except Exception as deepseek_err:
        if not anthropic_key:
            raise ValueError(f"DeepSeek failed and no Anthropic key is set: {deepseek_err}")
        raw = _call_anthropic(prompt, anthropic_key)
else:
    raw = _call_anthropic(prompt, anthropic_key)
```
