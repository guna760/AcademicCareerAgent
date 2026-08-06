import streamlit as st

from pipeline.academic_career_pipeline import (
    AcademicCareerPipeline
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AcademicCareerAgent",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title(
    "🎓 Academic-to-Career Intelligence System"
)

st.write(
    """
Upload any academic syllabus PDF and the system
will dynamically analyze it, identify industry skills,
recommend careers, find skill gaps, and generate a
personalized 6-month career roadmap.
"""
)


# ============================================================
# SIDEBAR
# ============================================================

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

llm_provider = "Groq"
llm_model = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

with st.sidebar:

    st.header("⚙️ System")

    st.info(f"""
LLM:
{llm_provider} - {llm_model}

Embeddings:
Sentence Transformers

Vector Database:
FAISS

Web Intelligence:
Tavily

Groq API:
Enabled
""")


# ============================================================
# PDF UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload Syllabus PDF",
    type=["pdf"]
)


# ============================================================
# PROCESS UPLOADED PDF
# ============================================================

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Analyze Syllabus",
        type="primary"
    ):

        try:

            # ==================================================
            # RUN PIPELINE
            # ==================================================

            with st.spinner(
                "Running AcademicCareerAgent..."
            ):

                pipeline = AcademicCareerPipeline()

                result = pipeline.process(
                    uploaded_file
                )


            # ==================================================
            # CHECK RESULT
            # ==================================================

            if not result:

                st.error(
                    "The pipeline returned an empty result."
                )

                st.stop()


            st.success(
                "Analysis completed successfully!"
            )


            # ==================================================
            # 1. DOMAIN / SYLLABUS ANALYSIS
            # ==================================================

            st.header(
                "🎓 1. Domain / Syllabus Analysis"
            )

            academic_analysis = result.get(
                "academic_analysis",
                "Academic analysis was not generated."
            )

            st.markdown(
                academic_analysis
            )


            # ==================================================
            # 2. INDUSTRY & CAREER INTELLIGENCE
            # ==================================================

            st.header(
                "💼 2. Industry & Career Intelligence"
            )

            career_analysis = result.get(
                "career_analysis",
                "Career analysis was not generated."
            )

            st.markdown(
                career_analysis
            )


            # ==================================================
            # 3. PERSONALIZED ROADMAP
            # ==================================================

            st.header(
                "🗺️ 3. Personalized 6-Month Roadmap"
            )

            roadmap = result.get(
                "roadmap",
                "Career roadmap was not generated."
            )

            st.markdown(
                roadmap
            )


            # ==================================================
            # 4. WEB SOURCES
            # ==================================================

            st.header(
                "🌐 4. Web Sources"
            )

            # --------------------------------------------------
            # Get sources returned by Tavily
            # --------------------------------------------------

            sources = result.get(
                "sources",
                []
            )


            # --------------------------------------------------
            # Make sure sources is a list
            # --------------------------------------------------

            if not isinstance(
                sources,
                list
            ):

                sources = []


            # --------------------------------------------------
            # Display source count
            # --------------------------------------------------

            st.write(
                f"**Number of web sources: {len(sources)}**"
            )


            # --------------------------------------------------
            # DISPLAY WEB SOURCES
            # --------------------------------------------------

            if sources:

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    # ------------------------------------------
                    # Safely extract source information
                    # ------------------------------------------

                    if not isinstance(
                        source,
                        dict
                    ):

                        continue


                    title = source.get(
                        "title",
                        "Untitled Web Source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )

                    content = source.get(
                        "content",
                        ""
                    )


                    # ------------------------------------------
                    # SOURCE TITLE
                    # ------------------------------------------

                    st.subheader(
                        f"{i}. {title}"
                    )


                    # ------------------------------------------
                    # CLICKABLE WEB LINK
                    # ------------------------------------------

                    if url:

                        st.markdown(
                            f"🔗 **Web Link:** "
                            f"[Open Source]({url})"
                        )

                        # Show actual URL
                        st.caption(
                            url
                        )

                    else:

                        st.warning(
                            "URL not available for this source."
                        )


                    # ------------------------------------------
                    # SOURCE CONTENT
                    # ------------------------------------------

                    if content:

                        with st.expander(
                            "📄 View source content"
                        ):

                            st.write(
                                content
                            )


                    st.divider()


            else:

                st.warning(
                    "No web sources were returned by Tavily."
                )

                st.info(
                    """
If you expected web sources, check the terminal
for the Tavily search status and make sure
TAVILY_API_KEY is correctly loaded from your .env file.
"""
                )


            # ==================================================
            # 5. DOWNLOAD REPORT
            # ==================================================

            st.header(
                "📥 Download Report"
            )


            # --------------------------------------------------
            # CREATE TEXT REPORT
            # --------------------------------------------------

            report = f"""
ACADEMIC-TO-CAREER INTELLIGENCE REPORT
========================================


1. DOMAIN / SYLLABUS ANALYSIS
========================================

{academic_analysis}


2. INDUSTRY & CAREER INTELLIGENCE
========================================

{career_analysis}


3. PERSONALIZED 6-MONTH CAREER ROADMAP
========================================

{roadmap}


4. WEB SOURCES
========================================

"""


            # --------------------------------------------------
            # ADD WEB SOURCES TO REPORT
            # --------------------------------------------------

            if sources:

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    if not isinstance(
                        source,
                        dict
                    ):

                        continue


                    title = source.get(
                        "title",
                        "Untitled Web Source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )


                    report += (
                        f"\n{i}. {title}\n"
                        f"URL: {url}\n"
                    )


            else:

                report += (
                    "\nNo web sources were found.\n"
                )


            # --------------------------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------------------------

            st.download_button(

                label=(
                    "📥 Download Complete Career Report"
                ),

                data=report,

                file_name=(
                    "Academic_Career_Report.txt"
                ),

                mime="text/plain"
            )


        # ======================================================
        # ERROR HANDLING
        # ======================================================

        except Exception as e:

            st.error(
                "An error occurred while analyzing the syllabus."
            )

            st.exception(
                e
            )