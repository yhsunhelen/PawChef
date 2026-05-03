# Bug Report — PawChef

## Bug 1 — Weight = 0 Bypasses Form Validation

**File:** `Final/pages/1_profile.py`, line 77  
**Severity:** Medium

**Description:**  
The weight field accepts `0` as a valid value. The validation only checks for `None` (empty field), so a user can submit a weight of zero without any error.

**Steps to Reproduce:**
1. Open the Pet Profile page
2. Fill in all required fields normally
3. Set Weight to `0`
4. Click "Generate Meal Plan"

**Expected:** Error message — "Weight must be greater than 0."  
**Actual:** Form submits successfully. The calorie calculation (`70 × 0^0.75 = 0`) is forced to 1 kcal/day by a `max(1, ...)` guard in `nutrition.py`, producing a nonsensical meal plan.

---

## Bug 2 — Age = 0 Bypasses Form Validation

**File:** `Final/pages/1_profile.py`, line 75  
**Severity:** Low

**Description:**  
Same issue as Bug 1. Age `0` is accepted without error. A newborn animal has very different nutritional needs, but the app treats it identically to any other age.

**Steps to Reproduce:**
1. Open the Pet Profile page
2. Fill in all required fields normally
3. Set Age to `0`
4. Click "Generate Meal Plan"

**Expected:** Error message — "Age must be greater than 0."  
**Actual:** Form submits and generates a plan with no age-appropriate adjustment.

---

## Bug 3 — Stale Meal Plan Shown After Profile Update

**File:** `Final/pages/2_meal_plan.py`, line 122–128  
**Severity:** Medium

**Description:**  
If a meal plan has already been generated and the user goes back to update the pet profile, the Meal Plan page still shows the old plan. The profile summary at the top reflects the new profile, but the meal content belongs to the previous one.

**Steps to Reproduce:**
1. Complete the Pet Profile form and navigate to Meal Plan
2. Click "Generate Meal Plan" — wait for it to finish
3. Go back to Pet Profile, change the species (e.g., Dog → Cat), and submit
4. Navigate back to Meal Plan

**Expected:** Either a prompt to regenerate, or the old plan is cleared automatically.  
**Actual:** Old meal plan is displayed under the new pet's profile header — a Dog plan shown for a Cat.

---

## Bug 4 — Invalid DeepSeek Key Blocks Valid Anthropic Key

**File:** `Final/utils/ai_client.py`, lines 132–148  
**Severity:** High

**Description:**  
The code always tries DeepSeek first if `DEEPSEEK_API_KEY` is set. If that key is present but invalid, the call raises an exception and the app shows an error — it never attempts the Anthropic key, even if `ANTHROPIC_API_KEY` is valid.

**Steps to Reproduce:**
1. Set `DEEPSEEK_API_KEY=invalid_key` and `ANTHROPIC_API_KEY=<valid key>` in `.env`
2. Complete the pet profile and click "Generate Meal Plan"

**Expected:** Falls back to Anthropic and generates a plan successfully.  
**Actual:** DeepSeek call fails with a 401 error; Anthropic is never tried.
