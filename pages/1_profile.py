import base64
import random
import time
from pathlib import Path

import streamlit as st

from lib.ui import inject_css

st.set_page_config(page_title="Pet Profile — PawChef", page_icon="🐾", layout="centered")
inject_css()

ASSETS = Path(__file__).parent.parent / "assets"
_AV_DIR = ASSETS / "avatars"

# (avatar_id, display_label, filename)
_SPECIES_AVATARS: dict[str, list[tuple[str, str, str]]] = {
    "Cat": [
        ("cat-orange-sit",       "Orange tabby",    "cat-orange-sit.png"),
        ("cat-siamese-sit",      "Siamese",         "cat-siamese-sit.png"),
        ("cat-black-sit",        "Black shorthair", "cat-black-sit.png"),
        ("cat-british-grey-sit", "British Grey",    "cat-british-grey-sit.png"),
        ("cat-grey-lie",         "Grey longhair",   "cat-grey-lie.png"),
    ],
    "Dog": [
        ("dog-corgi-stand",     "Corgi",       "dog-corgi-stand.png"),
        ("dog-shiba-sit",       "Shiba Inu",   "dog-shiba-sit.png"),
        ("dog-poodle-sit",      "Toy Poodle",  "dog-poodle-sit.png"),
        ("dog-dachshund-stand", "Dachshund",   "dog-dachshund-stand.png"),
        ("dog-spaniel-lie",     "Spaniel",     "dog-spaniel-lie.png"),
    ],
    "Rabbit": [
        ("rabbit-brown-stand",  "Brown bunny", "rabbit-brown-stand.png"),
    ],
    "Bird": [
        ("bird-budgie-stand",     "Budgie",     "bird-budgie-stand.png"),
        ("bird-cockatiel-stand",  "Cockatiel",  "bird-cockatiel-stand.png"),
        ("bird-canary-stand",     "Canary",     "bird-canary-stand.png"),
    ],
    "Hamster": [
        ("hamster-golden-stand",  "Golden hamster", "hamster-golden-stand.png"),
    ],
    "Guinea Pig": [
        ("guineapig-tricolor-sit", "Tricolor", "guineapig-tricolor-sit.png"),
    ],
}

_SPECIES_DEFAULT_AVATAR = {s: avs[0][0] for s, avs in _SPECIES_AVATARS.items()}
_SPECIES_DEFAULT_AVATAR["Other"] = "cat-orange-sit"


def _uid() -> str:
    return hex(int(time.time() * 1000) % 0xFFFFFFFF + random.randint(0, 9999))[2:]


def _img_b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


# ── Determine add vs edit mode ────────────────────────────────────────────────
if "pets" not in st.session_state:
    st.session_state["pets"] = []

editing_id = st.session_state.get("editing_pet_id")  # None = new pet, str = edit existing
pets: list = st.session_state["pets"]

if editing_id is not None:
    existing = next((p for p in pets if p["id"] == editing_id), {})
    is_new = False
else:
    existing = {}
    is_new = True

# ── Page header ───────────────────────────────────────────────────────────────
if st.button("← Back"):
    st.switch_page("app.py")

st.title("✏️ Edit Pet" if not is_new else "🐾 Add a Pet")
st.markdown("Fill in your pet's details so we can generate the right meal plan.")
st.markdown("---")

# ── Step 1: Species (outside form so avatar picker reacts) ────────────────────
st.markdown("**Step 1 — Species**")

species_options = ["", "Dog", "Cat", "Rabbit", "Bird", "Hamster", "Guinea Pig", "Other"]
default_species = existing.get("species", "")

# Only reset when switching to a different editing context, not on every rerun
_ctx = editing_id or "__new__"
if st.session_state.get("_profile_ctx") != _ctx:
    st.session_state["profile_species"] = default_species
    st.session_state["_profile_ctx"] = _ctx

species = st.selectbox(
    "Species *", options=species_options,
    key="profile_species",
    help="Select your pet's species.",
)

# ── Step 2: Avatar picker (species-aware, outside form) ───────────────────────
st.markdown("**Step 2 — Choose an avatar**")
st.caption("Pick a character for the living room scene.")

# Initialize selected avatar (once per editing context)
_av_key = f"sel_av_{_ctx}"
if _av_key not in st.session_state:
    st.session_state[_av_key] = existing.get("avatarId", _SPECIES_DEFAULT_AVATAR.get(species or "Cat", "cat-orange-sit"))

av_list = _SPECIES_AVATARS.get(species, []) if species else []

if av_list:
    # Show picker grid — up to 5 per row
    cols = st.columns(min(len(av_list), 5))
    for i, (av_id, av_label, av_file) in enumerate(av_list):
        with cols[i]:
            selected = st.session_state[_av_key] == av_id
            b64 = _img_b64(_AV_DIR / av_file)
            bc = "var(--primary)" if selected else "var(--line)"
            sh = "0 0 0 3px rgba(79,107,58,.2)" if selected else "none"
            st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
  <img src="data:image/png;base64,{b64}"
       style="width:88px;height:88px;object-fit:contain;background:var(--paper);
              border:2px solid {bc};border-radius:var(--r);padding:6px;box-shadow:{sh};">
  <span style="font-family:var(--mono);font-size:10px;color:var(--muted);
               text-transform:uppercase;letter-spacing:.08em">{av_label}</span>
</div>""", unsafe_allow_html=True)
            # For single-avatar species, just show as pre-selected
            if len(av_list) == 1:
                st.session_state[_av_key] = av_id
            else:
                btn_lbl = "✓ Selected" if selected else "Select"
                if st.button(btn_lbl, key=f"av_{av_id}_{_ctx}", use_container_width=True):
                    st.session_state[_av_key] = av_id
                    st.rerun()
elif species == "Other":
    st.info("🐾 Custom species — your pet will appear with a default avatar in the living room.", icon="ℹ️")
    st.session_state[_av_key] = "cat-orange-sit"
elif not species:
    st.caption("Select a species above to choose an avatar.")

st.markdown("---")

# ── Step 3: Profile details form ──────────────────────────────────────────────
st.markdown("**Step 3 — Pet details**")

with st.form("pet_profile_form"):
    pet_name = st.text_input(
        "Pet Name",
        placeholder="e.g. Mochi, Luna, Pepper",
        value=existing.get("name", ""),
    )

    breed = st.text_input(
        "Breed *",
        placeholder="e.g. Golden Retriever, Persian, Holland Lop",
        value=existing.get("breed", ""),
    )

    age_col, unit_col = st.columns([2, 1])
    with age_col:
        age_value = st.number_input(
            "Age *", min_value=0.0, max_value=300.0,
            value=float(existing["age_value"]) if existing.get("age_value") else None,
            step=1.0, placeholder="Enter age",
        )
    with unit_col:
        age_units = ["years", "months"]
        age_unit_default = existing.get("age_unit", "years")
        age_unit = st.selectbox("Unit", options=age_units,
                                index=age_units.index(age_unit_default) if age_unit_default in age_units else 0)

    weight_col, wunit_col = st.columns([2, 1])
    with weight_col:
        weight_value = st.number_input(
            "Weight *", min_value=0.0, max_value=1000.0,
            value=float(existing["weight_value"]) if existing.get("weight_value") else None,
            step=0.1, placeholder="Enter weight",
        )
    with wunit_col:
        w_units = ["kg", "lbs"]
        wunit_default = existing.get("weight_unit", "kg")
        weight_unit = st.selectbox("Unit ", options=w_units,
                                   index=w_units.index(wunit_default) if wunit_default in w_units else 0)

    allergies_str = ", ".join(existing.get("allergies", []))
    allergies = st.text_input(
        "Allergies / Forbidden Ingredients",
        placeholder="e.g. chicken, dairy, wheat (leave blank if none)",
        value=allergies_str,
        help="Separate multiple items with commas.",
    )

    goal_options = ["", "Maintenance", "Weight Loss", "Weight Gain", "Senior Care"]
    goal_default = existing.get("health_goal", "")
    health_goal = st.selectbox(
        "Health Goal *", options=goal_options,
        index=goal_options.index(goal_default) if goal_default in goal_options else 0,
        help="Select the primary health goal.",
    )

    btn_label = "Save Changes" if not is_new else "Save & Continue"
    submitted = st.form_submit_button(btn_label, use_container_width=True)

# ── Validation & save ─────────────────────────────────────────────────────────
if submitted:
    errors = []
    if not species:
        errors.append("Species is required (Step 1 above).")
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
            "id":           existing.get("id") or _uid(),
            "name":         pet_name.strip(),
            "species":      species,
            "breed":        breed.strip(),
            "age_value":    age_value,
            "age_unit":     age_unit,
            "weight_value": weight_value,
            "weight_unit":  weight_unit,
            "allergies":    [a.strip() for a in allergies.split(",") if a.strip()],
            "health_goal":  health_goal,
            "avatarId":     st.session_state.get(_av_key, "cat-orange-sit"),
        }

        # Detect if nutrition-relevant fields changed on edit → stale plan
        _plan_invalidated = False
        if not is_new:
            _old = existing
            _nutrition_fields = ("species", "health_goal", "weight_value", "weight_unit",
                                 "age_value", "age_unit")
            if any(str(_old.get(f)) != str(profile.get(f)) for f in _nutrition_fields):
                _plans = st.session_state.get("meal_plans", {})
                if profile["id"] in _plans:
                    del _plans[profile["id"]]
                    st.session_state["meal_plans"] = _plans
                    _plan_invalidated = True

        if is_new:
            pets.append(profile)
        else:
            for i, p in enumerate(pets):
                if p["id"] == profile["id"]:
                    pets[i] = profile
                    break

        st.session_state["pets"]           = pets
        st.session_state["pet_profile"]    = profile   # backward compat
        st.session_state["active_pet_id"]  = profile["id"]
        st.session_state["editing_pet_id"] = profile["id"]  # now in edit mode
        st.session_state.pop("meal_plan", None)

        _label = 'Added' if is_new else 'Updated'
        st.success(f"{_label}: **{profile['name'] or profile['breed']}**")
        if _plan_invalidated:
            st.info("Profile changed — the previous meal plan was cleared. Generate a new one below.")
        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.switch_page("app.py")
        with c2:
            if st.button("🍽️ Generate Meal Plan →", use_container_width=True):
                st.session_state["meal_plan"] = None
                st.switch_page("pages/2_meal_plan.py")
