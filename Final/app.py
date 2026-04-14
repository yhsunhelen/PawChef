import streamlit as st

st.set_page_config(
    page_title="PawChef",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 PawChef")
st.subheader("Personalized Weekly Meal Plans for Your Pet")

st.markdown(
    """
    Welcome to **PawChef** — an AI-powered meal planner tailored to your pet's unique needs.

    ### How it works
    1. **Build your pet's profile** — species, breed, age, weight, allergies, and health goals
    2. **Generate a meal plan** — get a safe, balanced 7-day feeding schedule
    3. **Review the results** — day-by-day breakdown with portion sizes

    ### Get started
    Use the **sidebar** to navigate to the Pet Profile page and enter your pet's information.
    """
)

st.info("Navigate to **Pet Profile** in the sidebar to begin.", icon="👈")
