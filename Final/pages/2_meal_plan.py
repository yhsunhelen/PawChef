import streamlit as st

from utils.ai_client import generate_meal_plan

st.set_page_config(
    page_title="Meal Plan — PawChef",
    page_icon="🐾",
    layout="centered",
)

st.title("🍽️ Meal Plan")

if "pet_profile" not in st.session_state:
    st.warning("No pet profile found. Please complete the **Pet Profile** page first.")
    st.stop()

profile = st.session_state["pet_profile"]
allergy_display = ", ".join(profile["allergies"]) if profile["allergies"] else "None"

st.markdown(
    f"**{profile['breed']} ({profile['species']})** · "
    f"{profile['age_value']} {profile['age_unit']} · "
    f"{profile['weight_value']} {profile['weight_unit']} · "
    f"Goal: **{profile['health_goal']}** · "
    f"Allergies: *{allergy_display}*"
)
st.divider()


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
        st.caption("Real products suited to your pet's profile — a convenient alternative or supplement to homemade meals.")
        for rec in recs:
            with st.expander(f"**{rec['brand']}** — {rec['product']}"):
                st.markdown(f"**Type:** {rec['type']}")
                st.markdown(f"**Why it fits:** {rec['why']}")


def _plan_to_text(plan: dict) -> str:
    portions = plan.get("_portions", {})
    lines = [
        "PawChef — 7-Day Personalized Meal Plan",
        f"Pet: {profile['breed']} ({profile['species']}), "
        f"{profile['age_value']} {profile['age_unit']}, "
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
            st.session_state["meal_plan"] = plan
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"An unexpected error occurred: {exc}")


# --- Main flow ---
if "meal_plan" not in st.session_state:
    st.markdown("Click below to generate a 7-day meal plan tailored to your pet.")
    if st.button("Generate Meal Plan", type="primary", use_container_width=True):
        _run_generation()
else:
    plan = st.session_state["meal_plan"]
    _display_plan(plan)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate", use_container_width=True):
            _run_generation()
    with col2:
        st.download_button(
            "Export as Text",
            data=_plan_to_text(plan),
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
