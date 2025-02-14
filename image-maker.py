import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Image.create(
    prompt="A futuristic cityscape at night with neon lights",
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']
print("Generated Image URL:", image_url)
