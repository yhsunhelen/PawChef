from __future__ import annotations

import json
import os

from dotenv import load_dotenv

from utils.nutrition import convert_weight_to_kg, get_portion_guidance

load_dotenv()

_ANTHROPIC_MODEL = "claude-sonnet-4-6"
_DEEPSEEK_MODEL = "deepseek-chat"

# Known toxic foods that must never appear regardless of user-supplied allergies.
_TOXIC: dict[str, list[str]] = {
    "Dog":    ["chocolate", "grapes", "raisins", "onion", "garlic", "xylitol",
               "macadamia nuts", "avocado", "alcohol", "caffeine"],
    "Cat":    ["onion", "garlic", "grapes", "raisins", "chocolate", "xylitol",
               "alcohol", "raw dough", "caffeine"],
    "Rabbit": ["chocolate", "avocado", "onion", "garlic", "rhubarb",
               "iceberg lettuce", "potato", "tomato leaves"],
    "Bird":   ["avocado", "chocolate", "onion", "garlic", "apple seeds",
               "alcohol", "xylitol", "caffeine", "salt"],
    "Other":  ["chocolate", "onion", "garlic", "grapes", "raisins", "xylitol", "alcohol"],
}


def _build_prompt(profile: dict, portions: dict) -> str:
    user_allergies = profile.get("allergies", [])
    species_toxic = _TOXIC.get(profile["species"], _TOXIC["Other"])
    forbidden = sorted({a.lower() for a in user_allergies} | set(species_toxic))

    allergy_str = ", ".join(user_allergies) if user_allergies else "none"
    forbidden_str = ", ".join(forbidden)
    weight_kg = convert_weight_to_kg(profile["weight_value"], profile["weight_unit"])

    return f"""You are a certified pet nutritionist. Generate a personalized 7-day meal plan.

PET PROFILE:
- Species: {profile['species']}
- Breed: {profile['breed']}
- Age: {profile['age_value']} {profile['age_unit']}
- Weight: {weight_kg:.1f} kg ({profile['weight_value']} {profile['weight_unit']})
- Health Goal: {profile['health_goal']}
- Owner-reported allergies: {allergy_str}

NUTRITION TARGETS:
- Estimated daily need: {portions['daily_kcal']} kcal
- Meals per day: {portions['meals_per_day']}
- Daily amount: ~{portions['wet_food_daily_g']}g ({portions['wet_food_daily_oz']} oz) wet/fresh food
  or ~{portions['dry_food_daily_g']}g ({portions['dry_food_daily_oz']} oz) dry kibble

MANDATORY RULES — failure to follow any rule makes the plan unsafe:
1. NEVER include any of these ingredients (toxic or allergenic): {forbidden_str}
2. Tailor every meal to the species; do not suggest foods only suitable for another species.
3. Scale portions to the weight and health goal above.
4. Use only ingredients available at standard grocery or pet stores.
5. Vary meals across the 7 days for nutritional diversity.

OUTPUT — return ONLY valid JSON, no markdown fences, no extra text:
{{
  "days": [
    {{
      "day": 1,
      "meals": [
        {{
          "name": "Meal name",
          "ingredients": ["ingredient with amount", "..."],
          "portion_g": <integer>,
          "portion_oz": <number with 1 decimal>,
          "notes": "optional short note or empty string"
        }}
      ],
      "daily_notes": "optional note about the day or empty string"
    }}
  ],
  "commercial_recommendations": [
    {{
      "brand": "Brand name",
      "product": "Specific product line",
      "type": "dry / wet / raw / treat",
      "why": "One sentence explaining why this suits the pet's profile"
    }}
  ]
}}

Generate exactly 7 days, each with exactly {portions['meals_per_day']} meal(s).
Also provide 4-5 real commercial pet food recommendations suited to this pet's species, age, weight, and health goal. Exclude any product containing the forbidden ingredients."""


def _parse_response(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3].strip()
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"AI returned invalid JSON.\n\nRaw response (first 500 chars):\n{raw[:500]}"
        ) from exc
    if "days" not in plan or len(plan["days"]) != 7:
        raise ValueError("AI returned an unexpected meal plan structure (expected 7 days).")
    return plan


def _call_deepseek(prompt: str, api_key: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model=_DEEPSEEK_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _call_anthropic(prompt: str, api_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=_ANTHROPIC_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_meal_plan(profile: dict) -> dict:
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not deepseek_key and not anthropic_key:
        raise ValueError(
            "No API key found. Set DEEPSEEK_API_KEY or ANTHROPIC_API_KEY in your .env file."
        )

    weight_kg = convert_weight_to_kg(profile["weight_value"], profile["weight_unit"])
    portions = get_portion_guidance(profile["species"], weight_kg, profile["health_goal"])
    prompt = _build_prompt(profile, portions)

    # Prefer DeepSeek if key is present, otherwise fall back to Anthropic.
    if deepseek_key:
        raw = _call_deepseek(prompt, deepseek_key)
    else:
        raw = _call_anthropic(prompt, anthropic_key)

    plan = _parse_response(raw)
    plan["_portions"] = portions
    return plan
