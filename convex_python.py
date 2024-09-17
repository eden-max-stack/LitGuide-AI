import os

from dotenv import load_dotenv

from convex import ConvexClient

load_dotenv("litguide_gemini_venv\.env.local")

#print(os.getenv("https://descriptive-seahorse-440.convex.cloud"))

client = ConvexClient("https://descriptive-seahorse-440.convex.cloud")
