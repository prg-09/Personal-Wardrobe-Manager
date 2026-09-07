import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def generate_outfit(clothes, occasion, season, style):

    wardrobe = ""

    for cloth in clothes:
        wardrobe += f"""
        ID: {cloth.id}
        Name: {cloth.name}
        Category: {cloth.category}
        Color: {cloth.color}
        Season: {cloth.season}
        Style: {cloth.style}
        """

    prompt = f"""
    You are an AI fashion assistant.

    The user owns the following clothing items:

    {wardrobe}

    The user wants an outfit for:

    Occasion: {occasion}
    Season: {season}
    Style: {style}

    Create ONE outfit using ONLY the clothing items listed above.

    Return ONLY valid JSON.
    Do not include markdown, explanations outside the JSON, or code fences.

    The JSON must have exactly this structure:

    {{
        "outfit_name": "Name of the outfit",
        "item_ids": [1, 2],
        "explanation": "Short explanation of why these items work together."
    }}

    Important:
    - item_ids must contain ONLY IDs from the wardrobe above.
    - Do not invent clothing items or IDs.
    """

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    output = interaction.output_text.strip()

    recommendation = json.loads(output)

    return recommendation