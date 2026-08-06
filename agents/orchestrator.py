from agents.academic_agent import AcademicAgent
from agents.career_agent import CareerAgent
from agents.roadmap_agent import RoadmapAgent


class Orchestrator:

    def __init__(self):

        self.academic_agent = (
            AcademicAgent()
        )

        self.career_agent = (
            CareerAgent()
        )

        self.roadmap_agent = (
            RoadmapAgent()
        )

    def run(
        self,
        syllabus_text,
        rag_context,
        web_context
    ):

        print(
            "Running Academic Agent..."
        )

        academic_analysis = (
            self.academic_agent.analyze(
                syllabus_text,
                rag_context
            )
        )

        print(
            "Running Career Agent..."
        )

        career_analysis = (
            self.career_agent.analyze(
                academic_analysis,
                web_context
            )
        )

        print(
            "Running Roadmap Agent..."
        )

        roadmap = (
            self.roadmap_agent.generate(
                academic_analysis,
                career_analysis,
                web_context
            )
        )

        return {

            "academic_analysis":
                academic_analysis,

            "career_analysis":
                career_analysis,

            "roadmap":
                roadmap,

            "web_sources":
                web_context
        }