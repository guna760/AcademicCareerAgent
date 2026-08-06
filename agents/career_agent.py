from llm.openai_client import ask_llm


class CareerAgent:

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

        return ask_llm(prompt)