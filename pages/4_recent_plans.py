from datetime import datetime

import streamlit as st

from lib.ui import inject_css, eyebrow, display, lede, h2

st.set_page_config(page_title="Recent Plans — PawChef", page_icon="📋", layout="centered")
inject_css()

st.markdown("""
<style>
.plans-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin: 20px 0 32px;
}
@media (max-width: 600px) { .plans-grid { grid-template-columns: 1fr; } }

.plan-thumb {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  display: flex; flex-direction: column; gap: 10px;
}
.pt-head {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
}
.pt-type {
  font-family: var(--mono);
  font-size: 10px; letter-spacing: .10em; text-transform: uppercase;
  background: var(--primary-soft); color: var(--primary);
  border-radius: var(--r-pill); padding: 3px 9px;
}
.pt-pet {
  font-size: 13px; color: var(--ink-2);
  font-family: var(--mono); letter-spacing: .04em;
}
.pt-title {
  font-family: var(--serif); font-size: 20px; color: var(--ink); line-height: 1.15;
  margin: 0;
}
.pt-title em { font-style: italic; color: var(--accent); }
.pt-stats {
  display: flex; gap: 16px; flex-wrap: wrap;
}
.ps-box {
  display: flex; flex-direction: column; gap: 1px;
}
.ps-box .k {
  font-family: var(--mono); font-size: 9px; letter-spacing: .10em;
  text-transform: uppercase; color: var(--muted);
}
.ps-box .v {
  font-family: var(--serif); font-size: 20px; color: var(--ink); line-height: 1;
}
.ps-box .v small { font-size: 12px; color: var(--ink-2); }
.ps-box .delta { font-size: 11px; color: var(--muted); margin-top: 1px; }
.pt-meta {
  display: flex; justify-content: space-between;
  font-family: var(--mono); font-size: 11px; color: var(--muted);
  border-top: 1px solid var(--line); padding-top: 10px; margin-top: 2px;
  letter-spacing: .04em;
}
.allergy-banner {
  display: flex; align-items: flex-start; gap: 12px;
  background: var(--accent-soft); border: 1px solid var(--accent);
  border-radius: var(--r); padding: 12px 14px; margin: 0 0 20px;
  font-size: 13px; color: var(--ink-2);
}
.allergy-banner .icon {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--accent); color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px; flex-shrink: 0;
}
.day-card {
  background: var(--paper); border: 1px solid var(--line);
  border-radius: var(--r-lg); overflow: hidden; margin-bottom: 10px;
}
.day-header {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px; cursor: pointer; user-select: none;
}
.day-header:hover { background: var(--bg-2); }
.dnum {
  font-family: var(--mono); font-size: 11px; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted); min-width: 32px;
}
.dnum strong { display: block; font-family: var(--serif); font-size: 22px;
  color: var(--ink); letter-spacing: 0; }
.meal-chips { display: flex; gap: 6px; flex-wrap: wrap; flex: 1; }
.meal-chip {
  background: var(--bg-2); border-radius: var(--r-pill);
  padding: 3px 9px; font-size: 12px; color: var(--ink-2);
}
.day-kcal {
  font-family: var(--mono); font-size: 12px; color: var(--muted);
  white-space: nowrap;
}
.footer-tip {
  display: flex; align-items: flex-start; gap: 14px;
  background: var(--primary-soft); border: 1px solid var(--line);
  border-radius: var(--r-lg); padding: 16px 18px; margin: 24px 0;
  font-size: 13px; color: var(--ink-2); line-height: 1.6;
}
.footer-tip .badge {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--primary); color: var(--primary-ink);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

_SPECIES_GLYPH = {"Dog": "🐕", "Cat": "🐈", "Rabbit": "🐇", "Bird": "🐦", "Other": "🐾"}
_MEAL_GLYPH = {"breakfast": "🥣", "lunch": "🍽", "dinner": "🌙"}
_DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _rel_time(ts: float) -> str:
    if not ts:
        return "just now"
    diff = (datetime.now().timestamp() - ts / 1000) / 86400
    if diff < 1:
        return "today"
    if diff < 2:
        return "yesterday"
    if diff < 7:
        return f"{int(diff)}d ago"
    if diff < 30:
        return f"{int(diff/7)}w ago"
    return f"{int(diff/30)}mo ago"


# ── Back + header ─────────────────────────────────────────────────────────────
if st.button("← Home"):
    st.switch_page("app.py")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
eyebrow("your saved plans")

pets: list        = st.session_state.get("pets", [])
meal_plans: dict  = st.session_state.get("meal_plans", {})

# Build list of (pet, plan) pairs
saved = [(p, meal_plans[p["id"]]) for p in pets if p["id"] in meal_plans]

display(f"Recent <em>plans.</em>")
if saved:
    lede(f"{len(saved)} plan{'s' if len(saved) > 1 else ''} saved across your pets.")
else:
    lede("No plans yet — generate one from the Meal Plan page.")

# ── Empty state ───────────────────────────────────────────────────────────────
if not saved:
    if st.button("🍽️ Go to Meal Plan", use_container_width=True):
        st.switch_page("pages/2_meal_plan.py")
    st.stop()

# ── Plan thumbnails grid ──────────────────────────────────────────────────────
h2("All <em>plans</em>")

rows = [saved[i:i+2] for i in range(0, len(saved), 2)]
for row in rows:
    cols = st.columns(len(row) if len(row) < 2 else 2)
    for col, (pet, plan) in zip(cols, row):
        with col:
            name       = pet.get("name") or pet.get("breed", "—")
            glyph      = _SPECIES_GLYPH.get(pet.get("species", ""), "🐾")
            portions   = plan.get("_portions", {})
            daily_kcal = portions.get("daily_kcal", plan.get("summary", {}).get("dailyKcal", "—"))
            protein    = plan.get("summary", {}).get("proteinPct", "—")
            variety    = plan.get("summary", {}).get("uniqueIngredients", "—")
            created_ts = plan.get("_created_at", 0)
            rel        = _rel_time(created_ts)
            goal       = pet.get("health_goal", "")

            st.markdown(f"""
<div class="plan-thumb">
  <div class="pt-head">
    <span class="pt-type">7-day homemade</span>
    <span class="pt-pet">{glyph} {name}</span>
  </div>
  <h4 class="pt-title">{goal} plan for <em>{name}</em></h4>
  <div class="pt-stats">
    <div class="ps-box">
      <div class="k">Daily energy</div>
      <div class="v">{daily_kcal}<small> kcal</small></div>
      <div class="delta">per day</div>
    </div>
    <div class="ps-box">
      <div class="k">Protein</div>
      <div class="v">{protein}<small>%</small></div>
      <div class="delta">of diet</div>
    </div>
    <div class="ps-box">
      <div class="k">Variety</div>
      <div class="v">{variety}<small> ing.</small></div>
      <div class="delta">across 7 days</div>
    </div>
  </div>
  <div class="pt-meta">
    <span>Generated {rel}</span>
    <span>{len(plan.get("days", []))} days · 3 meals/day</span>
  </div>
</div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("View plan", key=f"view_{pet['id']}", use_container_width=True):
                    st.session_state["active_pet_id"] = pet["id"]
                    st.session_state["pet_profile"]   = pet
                    st.session_state["meal_plan"]     = plan
                    st.switch_page("pages/2_meal_plan.py")
            with c2:
                if st.button("Regenerate", key=f"regen_{pet['id']}", use_container_width=True):
                    st.session_state["active_pet_id"] = pet["id"]
                    st.session_state["pet_profile"]   = pet
                    st.session_state["meal_plans"].pop(pet["id"], None)
                    st.session_state["meal_plan"] = None
                    st.switch_page("pages/2_meal_plan.py")

# ── Full plan viewer (expand selected pet's plan) ─────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
h2("Browse <em>day by day</em>")

pet_names = [
    (pet.get("name") or pet.get("breed", "—")) + f" ({pet.get('species','')})"
    for pet, _ in saved
]
sel_idx = st.selectbox("Choose a pet's plan to browse", range(len(saved)),
                       format_func=lambda i: pet_names[i])

sel_pet, sel_plan = saved[sel_idx]
sel_name    = sel_pet.get("name") or sel_pet.get("breed", "—")
sel_glyph   = _SPECIES_GLYPH.get(sel_pet.get("species", ""), "🐾")
sel_allergy = sel_pet.get("allergies", [])
sel_goal    = sel_pet.get("health_goal", "")

# Unit toggle
unit = st.radio("Units", ["grams", "ounces"], horizontal=True, label_visibility="collapsed")


def _fmt(g):
    if g is None:
        return "—"
    return f"{round(g / 28.35, 1)} oz" if unit == "ounces" else f"{g} g"


# Allergy banner
if sel_allergy:
    al_list = ", ".join(f"**{a}**" for a in sel_allergy)
    st.markdown(f"""
<div class="allergy-banner">
  <div class="icon">!</div>
  <div><strong>Allergen-safe plan.</strong> Excluded: {", ".join(sel_allergy)}. Every meal below is verified clean.</div>
</div>""", unsafe_allow_html=True)

# Day-by-day expanders
days = sel_plan.get("days", [])
for i, day in enumerate(days):
    meals   = day.get("meals", [])
    day_num = day.get("day", i + 1)
    day_kcal = sum(m.get("kcal", 0) or m.get("portion_g", 0) for m in meals)
    meal_chips = "".join(
        f'<span class="meal-chip">{_MEAL_GLYPH.get(m.get("slot",""),"🍴")} {m.get("name","")}</span>'
        for m in meals
    )
    day_name = _DAY_NAMES[i] if i < 7 else f"Day {day_num}"

    with st.expander(f"**D{day_num} — {day_name}**   · {day_kcal} kcal", expanded=(i == 0)):
        for meal in meals:
            slot  = meal.get("slot", "")
            mtime = meal.get("time", "")
            mname = meal.get("name", "")
            ings  = meal.get("ingredients", [])
            total_g = meal.get("totalGrams") or meal.get("portion_g")
            m_kcal  = meal.get("kcal") or meal.get("portion_kcal", "")
            is_swap = meal.get("swap", False)

            st.markdown(f"""
**{_MEAL_GLYPH.get(slot,'🍴')} {slot.capitalize()}**{"  `swap-friendly`" if is_swap else ""}
*{mname}* {'· ' + mtime if mtime else ''}
""")
            if isinstance(ings, list):
                for ing in ings:
                    if isinstance(ing, dict):
                        st.markdown(f"- {ing.get('name','')} &nbsp; `{_fmt(ing.get('grams'))}`")
                    else:
                        st.markdown(f"- {ing}")
            if total_g:
                st.caption(f"Total portion: {_fmt(total_g)}{' · ' + str(m_kcal) + ' kcal' if m_kcal else ''}")
            st.markdown("---")

        if day.get("daily_notes"):
            st.info(day["daily_notes"])

# ── Footer tip ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-tip">
  <div class="badge">💡</div>
  <div>
    <strong>Heads up:</strong> this plan is a starting point, not vet advice.
    Introduce new ingredients gradually over 5–7 days and always have fresh water available.
    If {sel_name} has chronic conditions, run this past your vet first.
  </div>
</div>""", unsafe_allow_html=True)
