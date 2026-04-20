# PR #1 — Initial Architecture for Pet Meal Planner

## Summary
This PR submits the initial architectural approach for the **Pet Meal Planner** project.

It includes:
- `ARCHITECTURE.md`
- proposed app structure
- data model
- tech stack justification
- agentic engineering plan
- initial safety strategy for AI-generated pet meal plans

This PR does **not** implement full product functionality yet. It establishes the technical foundation for future feature PRs.

---

## Deliverables Included

- [x] Added `ARCHITECTURE.md`
- [x] Defined initial file/module structure
- [x] Defined in-memory data model for pet profiles and meal plans
- [x] Justified Streamlit + Python + LLM API stack
- [x] Documented AI safety and allergy filtering strategy
- [x] Documented agentic engineering workflow

---

## Architectural Approach

### Proposed Stack
- **Frontend/UI:** Streamlit
- **Backend/Logic:** Python
- **AI Integration:** Claude API or OpenAI API
- **Storage:** Session state / CSV only

### Main Components
- Pet profile input page
- Meal plan results page
- Prompt builder
- AI client
- Nutrition/safety rules module
- Response parser
- Validation helpers

### Data Model
This project uses lightweight in-memory Python dictionaries stored in Streamlit session state.

Main entities:
- `pet_profile`
- `meal_plan`
- `species_rules`

### Safety Strategy
To reduce unsafe outputs, the architecture uses layered protection:
1. prompt-level safety instructions
2. allergy + toxic food filtering before API call
3. post-generation validation
4. visible disclaimer in UI

---

## Why This Architecture

This approach was chosen because it:
- fits the agreed MVP scope
- is realistic for one developer within the course timeline
- keeps the app modular and easy to test
- avoids unnecessary database or auth complexity
- supports safe iteration on prompts and meal plan formatting

---

## Out of Scope for This PR

This PR does not yet include:
- full Streamlit UI implementation
- live AI API integration
- deployed app
- multiple pet profile storage
- advanced veterinary nutrition calculations

These will be implemented in later feature PRs.

---

## Linked Spec / Agreement

This PR follows the agreed project scope in `SPEC.md`.

Client-recorded agreement:
- **Developer:** Yuhang Sun
- **Development Fee:** 35 GIX Bucks

---

## Review Notes for Client

Please review the following in particular:
- whether the proposed app structure matches project expectations
- whether the safety strategy is sufficient for the MVP
- whether the milestone sequencing looks reasonable
- whether any required feature is missing from the architecture

---

## Next Planned Step

After approval of this architecture PR, the next implementation PR will focus on:
**Pet profile form (Page 1) with validation**

