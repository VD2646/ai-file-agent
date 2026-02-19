import os
from groq import Groq
from dotenv import load_dotenv
from content_reader import extract_content
from config import MODEL_NAME

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DOCUMENTS = []


# -------- Index Documents --------
def index_documents(project_folder):
    global DOCUMENTS
    DOCUMENTS = []

    for root, dirs, files in os.walk(project_folder):
        for file in files:

            path = os.path.join(root, file)
            content = extract_content(path)

            if content.strip():
                DOCUMENTS.append({
                    "name": file,
                    "content": content[:2500]
                })


# -------- Ask Question --------
def answer_question(question):

    if not DOCUMENTS:
        return "No documents indexed yet. Please set folder first."

    docs_text = ""
    for i, doc in enumerate(DOCUMENTS):
        docs_text += f"\nDocument {i+1}: {doc['name']}\n{doc['content']}\n"

    prompt = f"""
You are a personal document assistant.

Answer the question ONLY using the provided documents.

If the answer exists, explain clearly and mention which document you used.

If unsure, say:
"I searched your files but couldn't find a clear answer."

DOCUMENTS:
{docs_text}

QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
