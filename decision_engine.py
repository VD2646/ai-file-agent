from groq import Groq
import os
from dotenv import load_dotenv
from config import MODEL_NAME, MAX_INPUT_CHARS

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def choose_or_create_category(text, filename, existing_folders):
    text = text[:MAX_INPUT_CHARS]

    folders_list = "\n".join(f"- {f}" for f in existing_folders) if existing_folders else "None"

    prompt = f"""
You are an AI file organizer.

Goal:
- If the file fits one of the EXISTING folders, choose it EXACTLY.
- Otherwise, create ONE new short, professional folder name.

Rules:
- Prefer reusing existing folders when meanings match.
- Keep names consistent and simple (e.g., 'Exam Schedules', 'Poultry Farming').
- No symbols or markdown.
- Return ONLY in this format:

Category: <folder name>
Reason: <short reason>

Existing Folders:
{folders_list}

File Name:
{os.path.basename(filename)}

Content:
{text}
"""

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content.strip()
