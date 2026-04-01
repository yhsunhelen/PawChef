# 🐾 PawChef 

A Streamlit web app that generates personalized weekly meal plans for pets using AI. Input your pet's profile and get a safe, balanced 7-day feeding schedule — no vet visit required.

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

**Developer:** [Developer Name]  
**Agreed Fee:** 500 GIX Bucks  
**Total Duration:** ~5 weeks  

| Check-in | Date | Required Progress |
|----------|------|-------------------|
| ✅ Check-in 1 | Week 1 | Project repo initialized; pet profile form (Page 1) fully functional with all input fields and validation |
| 🔄 Check-in 2 | Week 3 | AI API integrated and returning meal plans; allergy filtering working; basic results page (Page 2) displaying output |
| 🏁 Check-in 3 | Week 5 | Full app complete — portion sizes, UI polish, mobile responsiveness, README updated, deployed to Streamlit Cloud |

---

## Disclaimer

Pet Meal Planner is designed for general nutrition guidance only. It is **not a substitute for professional veterinary advice**. Always consult a licensed veterinarian for medical concerns or special dietary conditions.

---

## Author

**Mengqi Shi**  
TECHIN 510 — Programming for Digital and Physical User Interfaces  
University of Washington, GIX