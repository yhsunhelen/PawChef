import time

import streamlit as st
from lib.ui import inject_css

from utils.ai_client import generate_meal_plan

st.set_page_config(page_title="Meal Plan — PawChef", page_icon="🐾", layout="centered")
inject_css()

if st.button("← Home"):
    st.switch_page("app.py")

st.title("🍽️ Meal Plan")

# ── Pet selector ──────────────────────────────────────────────────────────────
pets: list = st.session_state.get("pets", [])

# Fall back: if old single-pet format exists but pets list doesn't
if not pets and "pet_profile" in st.session_state:
    old = st.session_state["pet_profile"]
    if "id" not in old:
        import time, random
        old["id"] = hex(int(time.time() * 1000) % 0xFFFFFFFF + random.randint(0,9999))[2:]
    pets = [old]
    st.session_state["pets"] = pets

if not pets:
    st.warning("No pet profile found. Please add a pet first.")
    if st.button("🐾 Add a pet", use_container_width=True):
        st.session_state["editing_pet_id"] = None
        st.switch_page("pages/1_profile.py")
    st.stop()

# Pick which pet
def _pet_label(p):
    name = p.get("name") or p.get("breed", "Unknown")
    return f"{name} ({p.get('species','')})"

active_id = st.session_state.get("active_pet_id")
pet_ids   = [p["id"] for p in pets]

# Default to active_pet_id if valid, else first pet
if active_id and active_id in pet_ids:
    default_idx = pet_ids.index(active_id)
else:
    default_idx = 0

if len(pets) > 1:
    selected_idx = st.selectbox(
        "Select a pet",
        range(len(pets)),
        index=default_idx,
        format_func=lambda i: _pet_label(pets[i]),
    )
else:
    selected_idx = 0

profile = pets[selected_idx]
st.session_state["active_pet_id"] = profile["id"]
st.session_state["pet_profile"]   = profile  # backward compat

allergy_display = ", ".join(profile["allergies"]) if profile["allergies"] else "None"
name_display = profile.get("name") or profile.get("breed", "—")

st.markdown(
    f"**{name_display}** · {profile['breed']} ({profile['species']}) · "
    f"{profile['age_value']} {profile['age_unit']} · "
    f"{profile['weight_value']} {profile['weight_unit']} · "
    f"Goal: **{profile['health_goal']}** · "
    f"Allergies: *{allergy_display}*"
)
st.divider()

# ── Plan storage per pet ──────────────────────────────────────────────────────
if "meal_plans" not in st.session_state:
    st.session_state["meal_plans"] = {}

_plans: dict = st.session_state["meal_plans"]


def _display_plan(plan: dict) -> None:
    portions = plan.get("_portions", {})
    if portions:
        st.markdown(
            f"**Daily target:** ~{portions['daily_kcal']} kcal &nbsp;|&nbsp; "
            f"~{portions['wet_food_daily_g']} g ({portions['wet_food_daily_oz']} oz) wet food "
            f"or ~{portions['dry_food_daily_g']} g ({portions['dry_food_daily_oz']} oz) dry kibble"
        )
        st.markdown("")

    st.subheader("🍳 Homemade Meal Plan")
    for day_data in plan["days"]:
        with st.expander(f"**Day {day_data['day']}**", expanded=(day_data["day"] == 1)):
            for meal in day_data["meals"]:
                st.markdown(f"##### {meal['name']}")
                for ingredient in meal["ingredients"]:
                    st.markdown(f"- {ingredient}")
                st.caption(f"Portion: {meal['portion_g']} g / {meal['portion_oz']} oz")
                if meal.get("notes"):
                    st.info(meal["notes"], icon="💡")
            if day_data.get("daily_notes"):
                st.markdown(f"*{day_data['daily_notes']}*")

    recs = plan.get("commercial_recommendations", [])
    if recs:
        st.markdown("")
        st.subheader("🛒 Recommended Commercial Foods")
        st.caption("Products suited to your pet's profile — an alternative or supplement to homemade meals.")
        for rec in recs:
            with st.expander(f"**{rec['brand']}** — {rec['product']}"):
                st.markdown(f"**Type:** {rec['type']}")
                st.markdown(f"**Why it fits:** {rec['why']}")


def _plan_to_text(plan: dict) -> str:
    portions = plan.get("_portions", {})
    name_display_txt = profile.get("name") or profile.get("breed", "—")
    lines = [
        "PawChef — 7-Day Personalized Meal Plan",
        f"Pet: {name_display_txt} · {profile['breed']} ({profile['species']}) · "
        f"{profile['age_value']} {profile['age_unit']} · "
        f"{profile['weight_value']} {profile['weight_unit']}",
        f"Health Goal: {profile['health_goal']}",
        f"Allergies: {allergy_display}",
    ]
    if portions:
        lines.append(
            f"Daily target: ~{portions['daily_kcal']} kcal | "
            f"~{portions['wet_food_daily_g']}g wet food or ~{portions['dry_food_daily_g']}g dry kibble"
        )
    lines.append("")
    for day_data in plan["days"]:
        lines.append(f"=== Day {day_data['day']} ===")
        for meal in day_data["meals"]:
            lines.append(f"  {meal['name']}")
            for ingredient in meal["ingredients"]:
                lines.append(f"    - {ingredient}")
            lines.append(f"  Portion: {meal['portion_g']} g / {meal['portion_oz']} oz")
            if meal.get("notes"):
                lines.append(f"  Note: {meal['notes']}")
        if day_data.get("daily_notes"):
            lines.append(f"  {day_data['daily_notes']}")
        lines.append("")
    recs = plan.get("commercial_recommendations", [])
    if recs:
        lines.append("=== Recommended Commercial Foods ===")
        for rec in recs:
            lines.append(f"  {rec['brand']} — {rec['product']} ({rec['type']})")
            lines.append(f"    {rec['why']}")
        lines.append("")
    lines.append(
        "Disclaimer: PawChef is for general nutrition guidance only and is not a substitute "
        "for professional veterinary advice."
    )
    return "\n".join(lines)


def _run_generation() -> None:
    with st.spinner("Generating your pet's personalized 7-day meal plan..."):
        try:
            plan = generate_meal_plan(profile)
            plan["_created_at"] = int(time.time() * 1000)
            plan["_profile_snapshot"] = {
                "species":      profile.get("species"),
                "health_goal":  profile.get("health_goal"),
                "weight_value": profile.get("weight_value"),
                "weight_unit":  profile.get("weight_unit"),
                "age_value":    profile.get("age_value"),
                "age_unit":     profile.get("age_unit"),
            }
            _plans[profile["id"]] = plan
            st.session_state["meal_plans"] = _plans
            st.session_state["meal_plan"]  = plan  # backward compat
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"An unexpected error occurred: {exc}")


# ── Main flow ─────────────────────────────────────────────────────────────────
current_plan = _plans.get(profile["id"])


def _is_plan_stale(plan: dict, pet: dict) -> bool:
    snap = plan.get("_profile_snapshot")
    if not snap:
        return False
    fields = ("species", "health_goal", "weight_value", "weight_unit", "age_value", "age_unit")
    return any(str(snap.get(f)) != str(pet.get(f)) for f in fields)


if current_plan is None:
    st.markdown("Click below to generate a 7-day meal plan tailored to your pet.")
    if st.button("Generate Meal Plan", type="primary", use_container_width=True):
        _run_generation()
else:
    if _is_plan_stale(current_plan, profile):
        st.warning(
            "⚠️ This plan was generated before the profile was updated. "
            "Click **Regenerate** below to get a fresh plan.",
            icon="⚠️",
        )
    _display_plan(current_plan)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate", use_container_width=True):
            _run_generation()
    with col2:
        st.download_button(
            "Export as Text",
            data=_plan_to_text(current_plan),
            file_name="pawchef_meal_plan.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.divider()
st.caption(
    "PawChef is designed for general nutrition guidance only. "
    "It is **not** a substitute for professional veterinary advice. "
    "Always consult a licensed veterinarian for medical concerns or special dietary conditions."
)
