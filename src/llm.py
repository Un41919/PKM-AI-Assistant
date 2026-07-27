import os

from dotenv import load_dotenv
from groq import Groq

# ==========================================================
# Load Environment
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if API_KEY is None:
    raise ValueError(
        "GROQ_API_KEY tidak ditemukan di file .env"
    )

# ==========================================================
# Groq Client
# ==========================================================

client = Groq(
    api_key=API_KEY
)

# ==========================================================
# Prompt Template
# ==========================================================

SYSTEM_PROMPT = """
Kamu adalah PKM AI Assistant.

Tugasmu adalah menjawab pertanyaan pengguna
BERDASARKAN konteks yang diberikan.

Aturan:

1. Gunakan HANYA informasi dari Context.

2. Jangan mengarang jawaban.

3. Jika informasi tidak tersedia,
jawab:

"Maaf, informasi tersebut tidak ditemukan
pada dokumen Panduan PKM yang tersedia."

4. Jawab menggunakan Bahasa Indonesia.

5. Berikan jawaban yang jelas,
ringkas,
dan mudah dipahami.

6. Jangan menyebutkan informasi
yang tidak ada pada Context.
"""

# ==========================================================
# Generate Answer
# ==========================================================

def generate_answer(question, context):

    prompt = f"""
Context:

{context}

--------------------------------------

Question:

{question}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.2,

        max_tokens=700,

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )

    return response.choices[0].message.content


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample_context = """
Program Kreativitas Mahasiswa (PKM)
bertujuan mempersiapkan mahasiswa
yang kreatif,
inovatif,
kompetitif,
adaptif,
produktif,
dan berkarakter Pancasila.
"""

    question = "Apa tujuan PKM?"

    answer = generate_answer(
        question,
        sample_context
    )

    print("="*80)

    print(answer)