import os

from dotenv import load_dotenv
from openai import OpenAI


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# OPENAI CLIENT
# ==========================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in .env"
    )


client = OpenAI(
    api_key=api_key
)


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini"
)


# ==========================================================
# ASK LLM
# ==========================================================

def ask_llm(prompt):

    try:

        response = client.responses.create(

            model=MODEL,

            input=prompt

        )

        return response.output_text

    except Exception as e:

        raise RuntimeError(
            f"OpenAI API Error: {str(e)}"
        )