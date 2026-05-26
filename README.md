# 🐾 PawChef

A Streamlit web app that generates personalized weekly meal plans for pets using AI. Input your pet's profile and get a safe, balanced 7-day feeding schedule — no vet visit required.

**Live Demo:** https://swbenchmini-ewzmhdfhrvd9zrsnzds4dz.streamlit.app

---

## What It Does

Pet owners often rely on generic food packaging guidelines that don't account for their animal's individual needs. **PawChef** solves this by letting you describe your pet — species, age, weight, allergies, and health goals — and instantly generating a tailored 7-day meal plan with portion sizes and ingredient suggestions.

---

## Features

- **Multi-Pet Household** — Add up to 10 pets; each has its own profile, avatar, and meal plan
- **Species-Aware Avatars** — Cat, Dog, Rabbit, Bird, Hamster, Guinea Pig characters (16 total)
- **Interactive Living Room** — All your pets appear in an animated scene; tap any pet to check in
- **AI-Powered Meal Plans** — 7-day homemade plan generated via Claude (Anthropic) or DeepSeek API
- **Allergy Safety** — User allergies + species-specific toxic foods are excluded from every suggestion
- **Portion Guidance** — Portions scaled via veterinary RER formula to weight and health goal
- **Recent Plans** — Browse and compare all saved plans day-by-day, with gram/ounce toggle
- **Stale Plan Detection** — Automatically clears or warns when a plan no longer matches the profile
- **Plain-Text Export** — Download any plan as a `.txt` file

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Backend | Python |
| AI | Anthropic Claude API (primary) / DeepSeek (fallback) |
| Storage | Streamlit session state |
| Tests | pytest |

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/GIX-Luyao/final-project-codebase-MengqiS21.git
cd final-project-codebase-MengqiS21/Final

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY (and optionally DEEPSEEK_API_KEY)

# Run the app
streamlit run app.py
```

---

## Project Structure

```
Final/
├── app.py                    # Homepage — pet grid, living room CTA, recent plans
├── pages/
│   ├── 1_profile.py          # Add / edit pet profile with species-aware avatar picker
│   ├── 2_meal_plan.py        # Generate, view, and export 7-day meal plans
│   ├── 3_living_room.py      # Interactive animated scene with all pets
│   └── 4_recent_plans.py     # Browse all saved plans day-by-day
├── utils/
│   ├── ai_client.py          # AI API integration, prompt engineering, fallback logic
│   └── nutrition.py          # RER calorie calculation, portion sizes, species rules
├── lib/
│   └── ui.py                 # CSS design system (design tokens, inject_css helper)
├── assets/
│   ├── avatars/              # 16 PNG pet avatars + manifest.json
│   └── scenes/               # Living room background image
├── tests/
│   ├── test_nutrition.py     # Calorie math and portion guidance (14 tests)
│   ├── test_ai_client.py     # Prompt building, JSON parsing, allergy filtering (10 tests)
│   ├── test_profile_validation.py  # Input validation + stale plan detection (16 tests)
│   └── test_security.py      # No leaked keys, .env.example, .gitignore (5 tests)
├── .env.example              # API key template — copy to .env, never commit .env
├── .gitignore                # Excludes .env and pycache
├── BUGS.md                   # Client bug report with fix documentation
├── SPEC.md                   # Agreed project scope
└── README.md
```

---

## Running Tests

```bash
pytest tests/ -v
```

**45 tests, all passing.** Coverage spans:

| File | Tests | What it covers |
|------|-------|----------------|
| `test_nutrition.py` | 14 | RER calorie formula, weight conversion, portion keys |
| `test_ai_client.py` | 10 | Prompt construction, allergen inclusion, JSON parsing |
| `test_profile_validation.py` | 16 | Zero/negative age & weight rejection, stale plan detection |
| `test_security.py` | 5 | No API keys in source, `.env.example` present and clean |

---

## Security

- API keys are loaded from `.env` (never committed — listed in `.gitignore`)
- `.env.example` provides a safe template with placeholder values
- `test_security.py` scans all `.py` and `.env*` files for leaked key patterns on every test run
- No secrets are hard-coded anywhere in the codebase

---

## Bug Fixes (Client Report)

All four reported bugs are resolved. See [BUGS.md](BUGS.md) for full details.

| Bug | Severity | Status |
|-----|----------|--------|
| Weight = 0 bypasses form validation | Medium | ✅ Fixed |
| Age = 0 bypasses form validation | Low | ✅ Fixed |
| Stale meal plan shown after profile update | Medium | ✅ Fixed |
| Invalid DeepSeek key blocks valid Anthropic key | High | ✅ Fixed |

---

## Development Timeline

**Developer:** Yuhang Sun
**Agreed Fee:** 35 GIX Bucks
**Total Duration:** ~8 weeks

| Check-in | Date | Status | Progress |
|----------|------|--------|----------|
| Check-in 1 | 2026-04-06 | ✅ Complete | Repo initialized; pet profile form fully functional with validation and session state |
| Check-in 2 | 2026-05-03 | ✅ Complete | AI integration (Claude + DeepSeek fallback); RER nutrition engine; 7-day meal plan UI; export |
| Check-in 3 | 2026-05-25 | ✅ Complete | All bugs fixed; multi-pet architecture; living room scene; recent plans page; 45 automated tests; security checks; full avatar set (16 species); deployed |

---

## Disclaimer

PawChef is designed for general nutrition guidance only. It is **not a substitute for professional veterinary advice**. Always consult a licensed veterinarian for medical concerns or special dietary conditions.

---

## Author

**Yuhang Sun** (Developer)
**Mengqi Shi** (Client)
TECHIN 510 — Programming for Digital and Physical User Interfaces
University of Washington, GIX
