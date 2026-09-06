import os
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

    Create one outfit using ONLY the clothing items listed above.

    Give:
    1. Outfit name
    2. IDs of the items you selected
    3. A short explanation of why the items work together.

    Do not invent clothing items that are not in the wardrobe.
    """

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return interaction.output_text