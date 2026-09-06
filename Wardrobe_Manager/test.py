import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="""
You are an AI fashion assistant.

The user has these clothing items:

1. White T-Shirt
   Category: Top
   Color: White
   Season: Summer
   Style: Casual

2. Blue Jeans
   Category: Pants
   Color: Blue
   Season: All
   Style: Casual

3. Black Formal Trousers
   Category: Pants
   Color: Black
   Season: All
   Style: Formal

4. White Sneakers
   Category: Shoes
   Color: White
   Season: Summer
   Style: Casual

The user wants an outfit for:
Occasion: College
Season: Summer
Style: Casual

Create one outfit using ONLY the clothing items listed above.

Give:
1. Outfit name
2. Items used
3. A short explanation of why they work together.
"""
)

print(interaction.output_text)