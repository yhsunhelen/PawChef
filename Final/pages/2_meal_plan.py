import streamlit as st

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
st.markdown(
    f"Meal plan for **{profile['breed']} ({profile['species']})** — "
    f"{profile['age_value']} {profile['age_unit']}, "
    f"{profile['weight_value']} {profile['weight_unit']}, "
    f"Goal: {profile['health_goal']}"
)

st.info("AI meal plan generation will be available once the AI integration is complete (Issue #3).")
