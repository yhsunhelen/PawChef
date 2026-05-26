import base64
import random
import time
from pathlib import Path

import streamlit as st

from lib.ui import inject_css, display, eyebrow, h2, lede

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(page_title="PawChef", page_icon="🐾", layout="centered")
inject_css()

st.markdown("""
<style>
.chef-home-hero { padding: 32px 0 20px; }
.chef-pet-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0 32px; }
@media (max-width: 600px) { .chef-pet-grid { grid-template-columns: 1fr; } }
.chef-pet-card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  display: flex; flex-direction: column; gap: 10px;
}
.chef-pet-card .top { display: flex; gap: 12px; align-items: flex-start; }
.chef-pet-card .avatar-thumb {
  width: 64px; height: 64px;
  object-fit: contain;
  background: var(--bg-2);
  border-radius: var(--r);
  padding: 4px;
  flex-shrink: 0;
}
.chef-pet-card .avatar-placeholder {
  width: 64px; height: 64px;
  background: var(--bg-2);
  border-radius: var(--r);
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; flex-shrink: 0;
}
.chef-pet-card .info h3 {
  font-family: var(--serif); font-size: 18px; color: var(--ink); margin: 0 0 2px;
}
.chef-pet-card .info .sub { font-size: 12px; color: var(--ink-2); line-height: 1.5; }
.chef-pet-card .tags { display: flex; flex-wrap: wrap; gap: 4px; }
.chef-add-card {
  background: var(--paper);
  border: 2px dashed var(--line-strong);
  border-radius: var(--r-lg);
  padding: 18px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; min-height: 140px; cursor: pointer; color: var(--muted);
  transition: border-color 160ms, background 160ms;
}
.chef-add-card:hover { border-color: var(--primary); background: var(--primary-soft); }
.chef-add-card .plus { font-size: 28px; color: var(--primary); }
.chef-add-card .lbl { font-family: var(--sans); font-size: 14px; font-weight: 500; color: var(--ink-2); }
.chef-scene-cta {
  display: flex; align-items: center; gap: 16px;
  background: var(--paper); border: 1px solid var(--line);
  border-radius: var(--r-lg); padding: 16px 20px; margin: 0 0 4px;
}
.chef-scene-cta .thumb {
  width: 72px; height: 72px; border-radius: 14px;
  background-size: cover; background-position: center; flex-shrink: 0;
}
.chef-scene-cta .copy .lbl {
  font-family: var(--mono); font-size: 10px;
  letter-spacing: .12em; text-transform: uppercase; color: var(--accent);
}
.chef-scene-cta .copy .ttl {
  font-family: var(--serif); font-size: 22px; color: var(--ink); margin-top: 2px;
}
.chef-scene-cta .copy .ttl em { font-style: italic; color: var(--accent); }
.chef-scene-cta .copy .sub { font-size: 13px; color: var(--muted); margin-top: 2px; }
.chef-scene-cta .arrow { font-family: var(--serif); font-style: italic; font-size: 22px; color: var(--muted); }
.chef-steps {
  display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 20px 0 40px;
}
.chef-step {
  background: var(--paper); border: 1px solid var(--line);
  border-radius: var(--r-lg); padding: 20px; box-shadow: var(--shadow-sm);
}
.chef-step .num {
  font-family: var(--mono); font-size: 10px; letter-spacing: .12em;
  color: var(--muted); text-transform: uppercase; margin-bottom: 10px;
}
.chef-step .glyph { font-size: 26px; margin-bottom: 8px; }
.chef-step h3 { font-family: var(--serif); font-size: 17px; color: var(--ink); margin: 0 0 5px; }
.chef-step p   { font-size: 13px; color: var(--ink-2); margin: 0; line-height: 1.5; }
@media (max-width: 620px) { .chef-steps { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

_SPECIES_GLYPH = {"Dog": "🐕", "Cat": "🐈", "Rabbit": "🐇", "Bird": "🐦", "Other": "🐾"}
_AV_B64_CACHE: dict = {}


def _uid() -> str:
    return hex(int(time.time() * 1000) % 0xFFFFFFFF + random.randint(0, 9999))[2:]


def _av_b64(av_id: str) -> str:
    if av_id not in _AV_B64_CACHE:
        p = ASSETS / "avatars" / f"{av_id}.png"
        _AV_B64_CACHE[av_id] = base64.b64encode(p.read_bytes()).decode() if p.exists() else ""
    return _AV_B64_CACHE[av_id]


# ── Migrate old single-pet format ─────────────────────────────────────────────
if "pets" not in st.session_state:
    old = st.session_state.get("pet_profile")
    if old:
        if "id" not in old:
            old["id"] = _uid()
        st.session_state["pets"] = [old]
    else:
        st.session_state["pets"] = []

if "meal_plans" not in st.session_state:
    st.session_state["meal_plans"] = {}
    old_plan = st.session_state.get("meal_plan")
    pets = st.session_state["pets"]
    if old_plan and pets:
        st.session_state["meal_plans"][pets[0]["id"]] = old_plan

pets: list = st.session_state["pets"]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="chef-home-hero">', unsafe_allow_html=True)
eyebrow("your household")
display("Good morning,<br><em>chef.</em>")
n = len(pets)
if n == 0:
    lede("Let's start by adding your first pet.")
else:
    lede(f"{n} pet{'s' if n > 1 else ''} in the kitchen · use the sidebar to navigate.")
st.markdown("</div>", unsafe_allow_html=True)

# ── Pet grid ──────────────────────────────────────────────────────────────────
st.markdown('<div class="chef-pet-grid">', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# render cards (can't nest st widgets inside raw html, so iterate outside)
if pets:
    rows = [pets[i:i+2] for i in range(0, len(pets), 2)]
    for row in rows:
        cols = st.columns(len(row) if len(row) < 2 else 2)
        for col, pet in zip(cols, row):
            with col:
                av_id   = pet.get("avatarId", "cat-orange-sit")
                av_b64  = _av_b64(av_id)
                glyph   = _SPECIES_GLYPH.get(pet.get("species", ""), "🐾")
                name    = pet.get("name") or pet.get("breed", "—")
                sub     = f"{pet.get('breed','')} · {pet.get('age_value','')} {pet.get('age_unit','')} · {pet.get('weight_value','')} {pet.get('weight_unit','')}"
                al_tags = " ".join(
                    f'<span class="chef-tag chef-tag-allergy">no {a.lower()}</span>'
                    for a in pet.get("allergies", [])[:3]
                )
                goal_tag = f'<span class="chef-tag">{pet.get("health_goal","")}</span>'
                if av_b64:
                    av_html = f'<img class="avatar-thumb" src="data:image/png;base64,{av_b64}" alt="{name}">'
                else:
                    av_html = f'<div class="avatar-placeholder">{glyph}</div>'

                st.markdown(f"""
<div class="chef-pet-card">
  <div class="top">
    {av_html}
    <div class="info">
      <h3>{name}</h3>
      <div class="sub">{sub}</div>
    </div>
  </div>
  <div class="tags">{goal_tag}{al_tags}</div>
</div>""", unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✏️ Edit", key=f"edit_{pet['id']}", use_container_width=True):
                        st.session_state["editing_pet_id"] = pet["id"]
                        st.switch_page("pages/1_profile.py")
                with c2:
                    has_plan = pet["id"] in st.session_state["meal_plans"]
                    btn_label = "🍽️ New Plan" if not has_plan else "🍽️ Plan"
                    if st.button(btn_label, key=f"plan_{pet['id']}", use_container_width=True):
                        st.session_state["active_pet_id"]  = pet["id"]
                        st.session_state["pet_profile"]    = pet
                        st.session_state["meal_plan"]      = st.session_state["meal_plans"].get(pet["id"])
                        st.switch_page("pages/2_meal_plan.py")

# Add-pet card (max 10 pets stored, living room shows ≤5)
if len(pets) < 10:
    if st.button("＋ Add a pet", use_container_width=True, key="add_pet_btn"):
        st.session_state["editing_pet_id"] = None  # new pet
        st.switch_page("pages/1_profile.py")

# ── Living Room CTA ───────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

try:
    thumb_path = Path(__file__).parent / "assets" / "scenes" / "living-room.png"
    thumb_b64  = base64.b64encode(thumb_path.read_bytes()).decode()
    thumb_style = f"background-image: url('data:image/png;base64,{thumb_b64}')"
except Exception:
    thumb_style = "background: var(--bg-2)"

st.markdown(f"""
<div class="chef-scene-cta">
  <div class="thumb" style="{thumb_style}"></div>
  <div class="copy">
    <div class="lbl">interactive</div>
    <div class="ttl">Visit the <em>living room</em></div>
    <div class="sub">See all your pets at home — tap any of them to check in.</div>
  </div>
  <div class="arrow">→</div>
</div>""", unsafe_allow_html=True)

if st.button("🏠 Open Living Room", use_container_width=True, key="open_lr"):
    st.switch_page("pages/3_living_room.py")

_saved_count = sum(1 for p in pets if p["id"] in st.session_state.get("meal_plans", {}))
_plans_label = f"📋 Recent Plans ({_saved_count} saved)" if _saved_count > 0 else "📋 Recent Plans"
if st.button(_plans_label, use_container_width=True, key="open_plans"):
    st.switch_page("pages/4_recent_plans.py")

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
h2("How it <em>works</em>")
st.markdown("""
<div class="chef-steps">
  <div class="chef-step">
    <div class="num">step 01</div><div class="glyph">🐾</div>
    <h3>Build a pet profile</h3>
    <p>Species, breed, age, weight, allergies, goals. Add up to 10 pets.</p>
  </div>
  <div class="chef-step">
    <div class="num">step 02</div><div class="glyph">✨</div>
    <h3>Generate a meal plan</h3>
    <p>AI builds a safe, balanced 7-day homemade plan or picks commercial products.</p>
  </div>
  <div class="chef-step">
    <div class="num">step 03</div><div class="glyph">🏠</div>
    <h3>Visit the living room</h3>
    <p>All your pets hang out together. Tap any pet to check their profile and plans.</p>
  </div>
</div>""", unsafe_allow_html=True)
