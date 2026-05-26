import base64
import json
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from lib.ui import inject_css, display, eyebrow, lede

st.set_page_config(page_title="Living Room — PawChef", page_icon="🏠", layout="centered")
inject_css()

if st.button("← Home"):
    st.switch_page("app.py")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
eyebrow("the living room")
display("Welcome <em>home.</em>")

# ── Gather pets ───────────────────────────────────────────────────────────────
pets: list = st.session_state.get("pets", [])

if not pets and "pet_profile" in st.session_state:
    old = st.session_state["pet_profile"]
    if "id" not in old:
        import time
        old["id"] = hex(int(time.time() * 1000) % 0xFFFFFFFF)[2:]
    pets = [old]

# Up to 5 pets; if more, random sample (stable per session with a seed)
MAX_DISPLAY = 5
if len(pets) > MAX_DISPLAY:
    rng = random.Random(sum(ord(c) for c in "".join(p["id"] for p in pets)))
    displayed = rng.sample(pets, MAX_DISPLAY)
else:
    displayed = list(pets)

if displayed:
    n = len(pets)
    shown = len(displayed)
    msg = f"{n} pet{'s' if n > 1 else ''} in the household"
    if n > MAX_DISPLAY:
        msg += f" — showing {shown} of {n} (refresh to reshuffle)"
    lede(msg + ". Tap any of them to check in.")
else:
    lede("No pets yet — add one first and they'll move in.")
    st.page_link("pages/1_profile.py", label="Add a pet →", icon="🐾")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Asset paths ───────────────────────────────────────────────────────────────
ASSETS = Path(__file__).parent.parent / "assets"

_AV_DIR = ASSETS / "avatars"
_AV_FILES = {
    "cat-orange-sit":         _AV_DIR / "cat-orange-sit.png",
    "cat-siamese-sit":        _AV_DIR / "cat-siamese-sit.png",
    "cat-black-sit":          _AV_DIR / "cat-black-sit.png",
    "cat-british-grey-sit":   _AV_DIR / "cat-british-grey-sit.png",
    "cat-grey-lie":           _AV_DIR / "cat-grey-lie.png",
    "dog-corgi-stand":        _AV_DIR / "dog-corgi-stand.png",
    "dog-shiba-sit":          _AV_DIR / "dog-shiba-sit.png",
    "dog-poodle-sit":         _AV_DIR / "dog-poodle-sit.png",
    "dog-dachshund-stand":    _AV_DIR / "dog-dachshund-stand.png",
    "dog-spaniel-lie":        _AV_DIR / "dog-spaniel-lie.png",
    "rabbit-brown-stand":     _AV_DIR / "rabbit-brown-stand.png",
    "bird-budgie-stand":      _AV_DIR / "bird-budgie-stand.png",
    "bird-cockatiel-stand":   _AV_DIR / "bird-cockatiel-stand.png",
    "bird-canary-stand":      _AV_DIR / "bird-canary-stand.png",
    "hamster-golden-stand":   _AV_DIR / "hamster-golden-stand.png",
    "guineapig-tricolor-sit": _AV_DIR / "guineapig-tricolor-sit.png",
}


def _b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()


bg_b64 = _b64(ASSETS / "scenes" / "living-room.png")

# Preload all avatar images needed
_av_cache: dict = {}
for p in displayed:
    av_id = p.get("avatarId", "cat-orange-sit")
    if av_id not in _av_cache:
        path = _AV_FILES.get(av_id, _AV_FILES["cat-orange-sit"])
        _av_cache[av_id] = _b64(path)

# ── Slot definitions (positions as % of scene width/height) ──────────────────
_SLOTS = [
    {"id": "sofa-cushion", "x": 78, "feet_y": 67, "label": "on the sofa",         "prefer": ["lie", "sit", "stand"], "w": 17, "pop": "left"},
    {"id": "sofa-arm",     "x": 58, "feet_y": 58, "label": "on the armrest",      "prefer": ["sit", "stand"],        "w": 12, "pop": "left"},
    {"id": "rug-center",   "x": 42, "feet_y": 91, "label": "on the rug",          "prefer": ["lie", "sit", "stand"], "w": 16, "pop": "right"},
    {"id": "by-plant",     "x": 11, "feet_y": 81, "label": "by the plant",        "prefer": ["stand", "sit"],        "w": 13, "pop": "right"},
    {"id": "by-bowl",      "x": 82, "feet_y": 87, "label": "by the food bowl",    "prefer": ["stand", "sit"],        "w": 11, "pop": "left"},
]
_AV_POSE = {
    "cat-orange-sit": "sit",  "cat-siamese-sit": "sit", "cat-black-sit": "sit",
    "cat-british-grey-sit": "sit", "cat-grey-lie": "lie",
    "dog-corgi-stand": "stand",    "dog-shiba-sit": "sit",  "dog-poodle-sit": "sit",
    "dog-dachshund-stand": "stand","dog-spaniel-lie": "lie",
    "rabbit-brown-stand": "stand",
    "bird-budgie-stand": "stand",  "bird-cockatiel-stand": "stand", "bird-canary-stand": "stand",
    "hamster-golden-stand": "stand",
    "guineapig-tricolor-sit": "sit",
}

_SPECIES_GLYPH = {
    "dog": "🐕", "cat": "🐈", "rabbit": "🐇", "bird": "🐦",
    "hamster": "🐹", "guinea pig": "🐾", "other": "🐾",
}

# Scale factor applied to slot width — small animals should appear smaller
_SPECIES_SCALE = {
    "dog": 1.0, "cat": 1.0,
    "rabbit": 0.65, "bird": 0.50,
    "hamster": 0.45, "guinea pig": 0.55, "guineapig": 0.55,
    "other": 0.90,
}


def _assign(pets_list):
    remaining = list(pets_list)
    result = {}
    for slot in _SLOTS:
        for pet in remaining:
            pose = _AV_POSE.get(pet.get("avatarId", ""), "sit")
            if pose == slot["prefer"][0]:
                result[slot["id"]] = pet
                remaining.remove(pet)
                break
    for slot in _SLOTS:
        if slot["id"] in result:
            continue
        for pet in remaining:
            pose = _AV_POSE.get(pet.get("avatarId", ""), "sit")
            if pose in slot["prefer"]:
                result[slot["id"]] = pet
                remaining.remove(pet)
                break
    for slot in _SLOTS:
        if slot["id"] in result:
            continue
        if remaining:
            result[slot["id"]] = remaining.pop(0)
    return result


# ── Build HTML ────────────────────────────────────────────────────────────────
if not displayed:
    components.html(
        f"""<div style="text-align:center;padding:40px;color:#8d8073;
            font-family:-apple-system,sans-serif;font-size:14px;">
          Add a pet to see them here.
        </div>""",
        height=80,
    )
else:
    assignments = _assign(displayed)

    stickers_html = ""
    popovers_html = ""

    for i, slot in enumerate(_SLOTS):
        pet = assignments.get(slot["id"])
        if not pet:
            continue

        av_id   = pet.get("avatarId", "cat-orange-sit")
        av_b64  = _av_cache.get(av_id, "")
        name    = pet.get("name") or pet.get("breed", pet.get("species", "—"))
        breed   = pet.get("breed", "")
        age     = f"{pet.get('age_value','')} {pet.get('age_unit','')}"
        weight  = f"{pet.get('weight_value','')} {pet.get('weight_unit','')}"
        goal    = pet.get("health_goal", "")
        allergies = pet.get("allergies", [])

        sub_parts = [x for x in [breed, age, weight] if x.strip()]
        sub_text  = " · ".join(sub_parts)
        goal_tag  = f'<span class="pt">{ goal }</span>' if goal else ""
        al_tags   = "".join(f'<span class="pt al">no {a.lower()}</span>' for a in allergies[:4])

        # Staggered animation timing
        blink_d  = (i * 1.7) % 5
        breath_d = (i * 0.9) % 3
        tilt_d   = (i * 2.3) % 9

        slot_x      = slot["x"]
        slot_bottom = 100 - slot["feet_y"]
        species_key = (pet.get("species") or "").lower().replace(" ", "")
        scale       = _SPECIES_SCALE.get(species_key, 1.0)
        slot_w      = round(slot["w"] * scale, 1)

        stickers_html += f"""
<button class="ps" id="ps{i}"
  style="left:{slot_x}%;bottom:{slot_bottom}%;width:{slot_w}%"
  onclick="tgl(event,{i})" aria-label="{name}">
  <div class="sh"></div>
  <div class="br" style="animation-delay:{breath_d:.1f}s">
    <div class="tl" style="animation-delay:{tilt_d:.1f}s">
      <img class="pi" src="data:image/png;base64,{av_b64}"
           style="animation-delay:{blink_d:.1f}s" alt="{name}" draggable="false">
    </div>
  </div>
  <span class="nt">{name}</span>
</button>"""

        if slot["pop"] == "left":
            pop_left  = max(slot_x - 28, 2)
            pop_class = "pl"
        else:
            pop_left  = min(slot_x + 2,  78)
            pop_class = "pr"
        pop_bottom = slot_bottom + 4

        popovers_html += f"""
<div class="pop {pop_class}" id="pop{i}"
     style="left:{pop_left}%;bottom:{pop_bottom}%;">
  <button class="pc" onclick="cls({i})">×</button>
  <div class="pe">{slot["label"]}</div>
  <div class="pn">{name}</div>
  <div class="ps2">{sub_text}</div>
  <div class="ptags">{goal_tag}{al_tags}</div>
</div>"""

    HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#f5efe3;font-family:-apple-system,"Helvetica Neue",sans-serif;overflow:hidden}}
.stage{{position:relative;width:100%;background:#fbf7ee;border-radius:24px;overflow:hidden;
  box-shadow:0 8px 16px rgba(58,44,25,.08),0 24px 48px rgba(58,44,25,.12)}}
.bg{{display:block;width:100%;height:auto;pointer-events:none;user-select:none}}

/* sticker */
.ps{{position:absolute;transform:translateX(-50%);cursor:pointer;background:none;border:none;
  padding:0;transition:transform 240ms cubic-bezier(.3,1.3,.5,1);z-index:2;outline:none}}
.ps:hover{{transform:translateX(-50%) translateY(-6px);z-index:3}}
.ps.active{{transform:translateX(-50%) translateY(-8px);z-index:4}}
.sh{{position:absolute;bottom:-6px;left:50%;transform:translateX(-50%);width:70%;height:10px;
  background:radial-gradient(ellipse,rgba(58,44,25,.35) 0%,transparent 70%);
  transition:width 200ms,opacity 200ms;pointer-events:none}}
.ps:hover .sh,.ps.active .sh{{width:78%;opacity:.7}}
.br{{animation:br 3.4s ease-in-out infinite;transform-origin:bottom center}}
.tl{{animation:tl 8s ease-in-out infinite;transform-origin:50% 80%}}
.pi{{display:block;width:100%;height:auto;user-select:none;-webkit-user-drag:none;
  animation:bk 5.2s ease-in-out infinite;transform-origin:50% 30%;
  filter:drop-shadow(0 4px 12px rgba(58,44,25,.2))}}
.ps:hover .br{{animation-duration:2.2s}}.ps:hover .pi{{animation-duration:2.8s}}
.nt{{position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);
  background:rgba(42,36,29,.85);color:#f5efe3;padding:4px 10px;border-radius:999px;
  font-size:12px;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity 150ms;
  backdrop-filter:blur(4px)}}
.ps:hover .nt,.ps.active .nt{{opacity:1}}
@keyframes br{{0%,100%{{transform:translateY(0) scaleY(1)}}50%{{transform:translateY(-1.5px) scaleY(1.015)}}}}
@keyframes tl{{0%,100%{{transform:rotate(0deg)}}30%{{transform:rotate(-.8deg)}}60%{{transform:rotate(.5deg)}}96%{{transform:rotate(1.2deg)}}}}
@keyframes bk{{0%,88%,92%,96%,100%{{transform:scaleY(1)}}90%,94%{{transform:scaleY(.92)}}}}

/* popover */
.pop{{position:absolute;width:210px;background:#fbf7ee;border:1px solid #c9b896;
  border-radius:16px;padding:16px;z-index:10;
  box-shadow:0 2px 4px rgba(58,44,25,.05),0 8px 24px rgba(58,44,25,.1);display:none}}
.pop.show{{display:block;animation:pi 200ms cubic-bezier(.3,1.3,.5,1)}}
.pl{{transform:translate(-100%,0)}}
.pr{{transform:translate(0,0)}}
@keyframes pi{{from{{transform:translate(var(--tx),0) scale(.92);opacity:0}}to{{transform:translate(var(--tx),0) scale(1);opacity:1}}}}
.pop.pl{{--tx:-100%}}.pop.pr{{--tx:0}}
.pc{{position:absolute;top:10px;right:12px;background:none;border:none;cursor:pointer;
  font-size:20px;color:#8d8073;line-height:1;padding:2px 4px}}
.pc:hover{{color:#2a241d}}
.pe{{font-family:monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  color:#8d8073;margin-bottom:4px}}
.pn{{font-family:Georgia,serif;font-size:22px;color:#2a241d;line-height:1.1}}
.ps2{{font-size:12px;color:#5b4f42;margin-top:4px}}
.ptags{{display:flex;flex-wrap:wrap;gap:4px;margin-top:10px}}
.pt{{display:inline-block;background:#ede4d2;border-radius:999px;padding:2px 9px;
  font-size:11px;font-family:monospace;color:#5b4f42;letter-spacing:.04em}}
.pt.al{{background:#f1d3c4;color:#c45a3a}}
</style></head><body>
<div class="stage" id="stage">
  <img class="bg" id="bgimg" src="data:image/png;base64,{bg_b64}" alt="living room" draggable="false">
  {stickers_html}
  {popovers_html}
</div>
<script>
var active=-1;
function tgl(e,i){{
  e.stopPropagation();
  if(active===i){{cls(i);return;}}
  if(active>=0)cls(active);
  document.getElementById('ps'+i).classList.add('active');
  document.getElementById('pop'+i).classList.add('show');
  active=i;
}}
function cls(i){{
  var b=document.getElementById('ps'+i);
  var p=document.getElementById('pop'+i);
  if(b)b.classList.remove('active');
  if(p)p.classList.remove('show');
  active=-1;
}}
document.getElementById('stage').addEventListener('click',function(e){{
  if(!e.target.closest('[id^="ps"]')&&!e.target.closest('[id^="pop"]')){{
    if(active>=0)cls(active);
  }}
}});
function resize(){{
  var h=document.getElementById('stage').offsetHeight;
  if(h>0)window.parent.postMessage({{type:'streamlit:setFrameHeight',height:h+4}},'*');
}}
document.getElementById('bgimg').addEventListener('load',resize);
window.addEventListener('resize',resize);
setTimeout(resize,200);
</script>
</body></html>"""

    components.html(HTML, height=600, scrolling=False)
