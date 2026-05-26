import streamlit as st

st.set_page_config(
    page_title="Pet Profile — PawChef",
    page_icon="🐾",
    layout="centered",
)

st.title("🐶 Pet Profile")
st.markdown("Fill in your pet's details so we can generate the right meal plan.")

with st.form("pet_profile_form"):
    # --- Species ---
    species = st.selectbox(
        "Species *",
        options=["", "Dog", "Cat", "Rabbit", "Bird", "Other"],
        help="Select your pet's species.",
    )

    # --- Breed ---
    breed = st.text_input("Breed *", placeholder="e.g. Golden Retriever, Persian, Holland Lop")

    # --- Age ---
    age_col, unit_col = st.columns([2, 1])
    with age_col:
        age_value = st.number_input(
            "Age *",
            min_value=0.0,
            max_value=300.0,
            value=None,
            step=1.0,
            placeholder="Enter age",
        )
    with unit_col:
        age_unit = st.selectbox("Unit", options=["years", "months"], label_visibility="visible")

    # --- Weight ---
    weight_col, wunit_col = st.columns([2, 1])
    with weight_col:
        weight_value = st.number_input(
            "Weight *",
            min_value=0.0,
            max_value=1000.0,
            value=None,
            step=0.1,
            placeholder="Enter weight",
        )
    with wunit_col:
        weight_unit = st.selectbox("Unit ", options=["kg", "lbs"], label_visibility="visible")

    # --- Allergies / Forbidden Ingredients ---
    allergies = st.text_input(
        "Allergies / Forbidden Ingredients",
        placeholder="e.g. chicken, dairy, wheat (leave blank if none)",
        help="Separate multiple items with commas.",
    )

    # --- Health Goals ---
    health_goal = st.selectbox(
        "Health Goal *",
        options=["", "Maintenance", "Weight Loss", "Weight Gain", "Senior Care"],
        help="Select the primary health goal for your pet's diet.",
    )

    submitted = st.form_submit_button("Generate Meal Plan", use_container_width=True)

# --- Validation & save ---
if submitted:
    errors = []

    if not species:
        errors.append("Species is required.")
    if not breed.strip():
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

    if errors:
        for err in errors:
            st.error(err)
    else:
        profile = {
            "species": species,
            "breed": breed.strip(),
            "age_value": age_value,
            "age_unit": age_unit,
            "weight_value": weight_value,
            "weight_unit": weight_unit,
            "allergies": [a.strip() for a in allergies.split(",") if a.strip()],
            "health_goal": health_goal,
        }
        st.session_state["pet_profile"] = profile
        st.session_state.pop("meal_plan", None)  # clear stale plan when profile changes

        st.success("Profile saved! Here's a summary:")
        st.markdown("---")

        st.subheader("Profile Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Species:** {profile['species']}")
            st.markdown(f"**Breed:** {profile['breed']}")
            st.markdown(f"**Age:** {profile['age_value']} {profile['age_unit']}")
        with col2:
            st.markdown(f"**Weight:** {profile['weight_value']} {profile['weight_unit']}")
            st.markdown(f"**Health Goal:** {profile['health_goal']}")
            allergy_display = ", ".join(profile["allergies"]) if profile["allergies"] else "None"
            st.markdown(f"**Allergies:** {allergy_display}")

        st.info("Navigate to **Meal Plan** in the sidebar to view your pet's 7-day schedule.", icon="👈")
