import os
import requests
from dotenv import load_dotenv


load_dotenv()


class CareerAgent:

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
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 500
        }
    },
    timeout=600
)

        response.raise_for_status()

        return response.json()["response"]

    def analyze(
        self,
        academic_analysis,
        web_context
    ):

        prompt = f"""
You are the Career Intelligence Agent.

Analyze the academic profile and current industry information.

Identify:

1. Current industry-relevant skills
2. Industry technologies
3. Relevant tools/software
4. Recommended career roles
5. Career match reasoning
6. Skill gaps
7. Missing industry skills
8. Suggested certifications
9. Industry expectations

Use current web information where available.

Do not assume the student belongs to Computer Science.

The domain must be dynamically inferred from the academic analysis.

ACADEMIC ANALYSIS:

{academic_analysis}

CURRENT WEB / INDUSTRY INFORMATION:

{web_context}

Give a structured career intelligence report.
"""

        return self.ask_llm(prompt)