# 🐾 PawChef 

A Streamlit web app that generates personalized weekly meal plans for pets using AI. Input your pet's profile and get a safe, balanced 7-day feeding schedule — no vet visit required.

**Live Demo:** https://swbenchmini-ewzmhdfhrvd9zrsnzds4dz.streamlit.app

---

## What It Does

Pet owners often rely on generic food packaging guidelines that don't account for their animal's individual needs. **Pet Meal Planner** solves this by letting you describe your pet — species, age, weight, allergies, and health goals — and instantly generating a tailored 7-day meal plan with portion sizes and ingredient suggestions.

---

## Features

- **Pet Profile Form** — Enter species, breed, age, weight, allergies, and health goals
- **AI-Powered Meal Plans** — 7-day plan generated via Claude or OpenAI API
- **Allergy Safety** — Forbidden ingredients are excluded from all suggestions
- **Portion Guidance** — Portion sizes scaled to your pet's weight and life stage
- **Clean Results View** — Day-by-day meal breakdown, easy to read and copy

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Backend | Python |
| AI | Claude API / OpenAI API |
| Storage | Session state / CSV |

---

## Getting Started
```bash
# Clone the repo
git clone https://github.com/<your-username>/pet-meal-planner.git
cd pet-meal-planner

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY or OPENAI_API_KEY

# Run the app
streamlit run app.py
```

---

## Project Structure
```
pet-meal-planner/
├── app.py                # Main Streamlit app entry point
├── pages/
│   ├── 1_profile.py      # Pet profile input form
│   └── 2_meal_plan.py    # Meal plan results display
├── utils/
│   ├── ai_client.py      # AI API integration and prompt logic
│   └── nutrition.py      # Portion size and species safety rules
├── requirements.txt
├── .env.example
├── SPEC.md
└── README.md
```

---

## Development Timeline

**Developer:** Yuhang Sun  
**Agreed Fee:** 35 GIX Bucks  
**Total Duration:** ~8 weeks  

| Check-in | Date | Status | Progress |
|----------|------|--------|----------|
| Check-in 1 | 2026-04-06 | ✅ Complete | Project repo initialized; Streamlit entry point running; pet profile form (Page 1) fully functional with all input fields, validation, and session state |
| Check-in 2 *(mid-point)* | 2026-05-03 | ✅ Complete | AI API integrated (Anthropic Claude + DeepSeek fallback); species-aware toxic food filtering; portion size calculation via veterinary RER formula; 7-day meal plan + commercial food recommendations; plain-text export |
| Check-in 3 | 2026-05-24 | ⏳ Upcoming | Full app complete — UI polish, mobile responsiveness, input edge-case fixes, README finalized, deployed to Streamlit Cloud |

### Mid-Point Check (Check-in 2) — 2026-05-03

**Completed since Check-in 1:**
- `utils/ai_client.py` — AI prompt engineering with species-specific toxic food exclusion, dual-provider support (Anthropic primary / DeepSeek fallback), JSON response parsing with error handling
- `utils/nutrition.py` — Veterinary RER-based calorie calculation, per-species meal frequency, wet/dry food portion conversion
- `pages/2_meal_plan.py` — Full results UI: daily nutrition targets, collapsible day-by-day breakdown, commercial food recommendations, regenerate button, plain-text export
- `Final/` subdirectory restructured with all production code

**Remaining for Check-in 3:**
- Fix input validation edge cases (weight/age = 0 accepted; see Bug #13, #14)
- Handle AI provider fallback on error (see Bug #15)
- Clear stale meal plan when profile is re-submitted (see Bug #16)
- UI polish and mobile layout testing
- Deploy to Streamlit Cloud and update README with live URL

---

## Disclaimer

Pet Meal Planner is designed for general nutrition guidance only. It is **not a substitute for professional veterinary advice**. Always consult a licensed veterinarian for medical concerns or special dietary conditions.

---

## Author

**Mengqi Shi**  
TECHIN 510 — Programming for Digital and Physical User Interfaces  
University of Washington, GIX