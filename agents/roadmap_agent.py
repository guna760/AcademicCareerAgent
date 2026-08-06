import os
import requests
from dotenv import load_dotenv


load_dotenv()


class RoadmapAgent:

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

    def generate(
        self,
        academic_analysis,
        career_analysis,
        web_context
    ):

        prompt = f"""
You are the Personalized Career Roadmap Agent.

Create a detailed 6-month academic-to-career roadmap.

The roadmap must be personalized based on:

Academic knowledge
+
Industry requirements
+
Skill gaps
+
Career goals

Create exactly six months.

For EACH month provide:

Month:
Main Goal:
Topics:
Skills:
Tools:
Practical Tasks:
Mini Project:
Expected Outcome:

Also provide:

1. Final capstone project
2. Recommended portfolio projects
3. Recommended certifications
4. Job preparation
5. Interview preparation
6. Portfolio/GitHub recommendations

ACADEMIC ANALYSIS:

{academic_analysis}

CAREER ANALYSIS:

{career_analysis}

CURRENT INDUSTRY INFORMATION:

{web_context}

Make the roadmap realistic and domain-specific.
"""

        return self.ask_llm(prompt)