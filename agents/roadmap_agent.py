from llm.groq_client import ask_llm
class RoadmapAgent:

    def generate(
        self,
        academic_analysis,
        career_analysis,
        web_context
    ):

        prompt = f"""
You are the Personalized Career Roadmap Agent.

Create a comprehensive and realistic 6-month Academic-to-Career Roadmap based on:

- Academic knowledge
- Industry requirements
- Current market trends
- Skill gaps
- Career opportunities
- Recommended technologies
- Certifications
- Practical learning

The roadmap must be personalized according to the academic domain.

Do NOT assume the syllabus belongs to Computer Science.

The roadmap should adapt dynamically to any academic discipline such as:

- Computer Science
- Artificial Intelligence
- Deep Learning
- Renewable Energy
- Mechanical Engineering
- Civil Engineering
- Electrical Engineering
- Biotechnology
- Commerce
- Management
- MBA
- Any other academic field

Create exactly SIX months.

For EACH month include:

Month:
Main Goal:
Topics to Learn:
Technical Skills:
Tools / Software:
Practical Tasks:
Mini Project:
Expected Outcome:

After the monthly roadmap, also provide:

1. Final Capstone Project
2. Portfolio Project Recommendations
3. Recommended Certifications
4. Internship Preparation
5. Resume Preparation
6. Interview Preparation
7. GitHub / Portfolio Recommendations
8. Career Readiness Checklist

ACADEMIC ANALYSIS

{academic_analysis}

CAREER ANALYSIS

{career_analysis}

CURRENT INDUSTRY INFORMATION

{web_context}

Return the roadmap in a well-structured and easy-to-read format.
"""

        return ask_llm(prompt)