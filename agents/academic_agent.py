from llm.openai_client import ask_llm


class AcademicAgent:

    def analyze(
        self,
        syllabus_text,
        rag_context
    ):

        prompt = f"""
You are the Academic Analysis Agent.

Analyze the uploaded academic syllabus and produce a structured academic analysis.

Your tasks are to identify:

1. Academic domain
2. Major subjects/modules
3. Important concepts
4. Learning outcomes
5. Academic skills
6. Technical skills
7. Tools, software, frameworks, or programming languages mentioned
8. Core knowledge areas

Instructions:

- Use the uploaded syllabus as the primary source.
- Use the retrieved RAG context only as supporting information.
- Do NOT assume the syllabus belongs to Computer Science.
- Dynamically infer the academic domain from the syllabus.
- The syllabus may belong to Engineering, Commerce, Management,
  Biotechnology, Renewable Energy, Civil Engineering, Mechanical Engineering,
  Artificial Intelligence, Deep Learning, or any other discipline.

Retrieved RAG Context:

{rag_context}

Uploaded Syllabus:

{syllabus_text}

Return the output using the following headings:

# Academic Domain

# Major Subjects / Modules

# Important Concepts

# Learning Outcomes

# Academic Skills

# Technical Skills

# Tools / Software / Programming Languages

# Core Knowledge Areas
"""

        return ask_llm(prompt)