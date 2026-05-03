# PawChef

A Streamlit web app that generates personalized weekly meal plans for pets using AI.

## What It Does

Pet owners often rely on generic food packaging guidelines that don't account for their animal's individual needs. PawChef solves this by letting you describe your pet — species, age, weight, allergies, and health goals — and instantly generating a tailored 7-day meal plan with portion sizes and ingredient suggestions.

## Tech Stack

| Layer   | Technology              |
|---------|-------------------------|
| UI      | Streamlit               |
| Backend | Python                  |
| AI      | Claude API (Anthropic)  |
| Storage | Session state / CSV     |

## Project Structure

```
pawchef/
├── app.py                # Main Streamlit app entry point
├── pages/
│   ├── 1_profile.py      # Pet profile input form
│   └── 2_meal_plan.py    # Meal plan results display (AI coming soon)
├── utils/
│   ├── ai_client.py      # AI API integration (coming soon)
│   └── nutrition.py      # Portion size and safety rules (coming soon)
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/GIX-Luyao/final-project-codebase-MengqiS21.git
cd final-project-codebase-MengqiS21
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Development Timeline

| Check-in | Week | Milestone |
|----------|------|-----------|
| Check-in 1 | Week 1 | Project repo initialized; placeholder homepage running |
| Check-in 2 | Week 4 | AI API integrated; meal plan results page functional |
| Check-in 3 | Week 8 | Full app complete with UI polish and mobile responsiveness |

## Status

- [x] Project repository initialized
- [x] Streamlit app entry point created
- [x] Dependencies configured
- [x] Pet profile form — species, breed, age, weight, allergies, health goal, validation, session state
- [ ] AI meal plan generation (Issue #3)
- [ ] Portion sizing and nutrition rules (Issue #3)
