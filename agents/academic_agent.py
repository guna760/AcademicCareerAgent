import os
import requests
from dotenv import load_dotenv


load_dotenv()


class AcademicAgent:

    def __init__(self):

        self.ollama_url = os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434"
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2"
        )

    def ask_llm(self, prompt):

        response = requests.post(

            f"{self.ollama_url}/api/generate",

            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },

            timeout=600
        )

        response.raise_for_status()

        return response.json()["response"]

    def analyze(
        self,
        syllabus_text,
        rag_context
    ):

        prompt = f"""
You are the Academic Analysis Agent.

Analyze the uploaded academic syllabus.

Your task is to dynamically identify:

1. Academic domain
2. Major subjects/modules
3. Important concepts
4. Learning outcomes
5. Academic skills
6. Technical skills
7. Tools/software mentioned
8. Knowledge areas

Do NOT assume a fixed domain.

The syllabus could belong to:
Computer Science,
Deep Learning,
Commerce,
Renewable Energy,
Mechanical Engineering,
Civil Engineering,
Biotechnology,
MBA,
or another field.

Use the syllabus as the primary source.

Relevant retrieved syllabus context:

{rag_context}

FULL SYLLABUS:

{syllabus_text}

Provide a clear structured analysis.
"""

        return self.ask_llm(prompt)