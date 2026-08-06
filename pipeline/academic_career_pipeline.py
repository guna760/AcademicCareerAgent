from preprocessing.pdf_processor import (
    extract_text_from_pdf
)

from preprocessing.text_cleaner import (
    clean_text,
    chunk_text
)

from rag.embeddings import (
    EmbeddingModel
)

from rag.vector_store import (
    VectorStore
)

from rag.retriever import (
    Retriever
)

from rag.web_search import (
    WebSearch
)

from agents.orchestrator import (
    Orchestrator
)


class AcademicCareerPipeline:

    def __init__(self):

        print("\n========================================")
        print("Initializing Academic Career Pipeline")
        print("========================================")


        # ==================================================
        # 1. EMBEDDING MODEL
        # ==================================================

        print("\n[INIT 1] Loading embedding model...")

        self.embedding_model = (
            EmbeddingModel()
        )

        print(
            "Embedding model loaded successfully."
        )


        # ==================================================
        # 2. VECTOR STORE
        # ==================================================

        print("\n[INIT 2] Initializing vector store...")

        self.vector_store = (
            VectorStore()
        )

        print(
            "Vector store initialized successfully."
        )


        # ==================================================
        # 3. RAG RETRIEVER
        # ==================================================

        print("\n[INIT 3] Initializing RAG retriever...")

        self.retriever = Retriever(
            self.embedding_model,
            self.vector_store
        )

        print(
            "RAG retriever initialized successfully."
        )


        # ==================================================
        # 4. WEB SEARCH
        # ==================================================

        print("\n[INIT 4] Initializing Tavily web search...")

        self.web_search = (
            WebSearch()
        )

        print(
            "Web search initialized successfully."
        )


        # ==================================================
        # 5. MULTI-AGENT ORCHESTRATOR
        # ==================================================

        print("\n[INIT 5] Initializing multi-agent orchestrator...")

        self.orchestrator = (
            Orchestrator()
        )

        print(
            "Orchestrator initialized successfully."
        )


        print("\n========================================")
        print("Pipeline initialization completed")
        print("========================================")


    def process(
        self,
        pdf_file
    ):

        # ==================================================
        # STEP 1: PDF PROCESSING
        # ==================================================

        print(
            "\n[STEP 1] Extracting syllabus from PDF..."
        )


        if pdf_file is None:

            raise ValueError(
                "PDF file was not provided."
            )


        try:

            raw_text = (
                extract_text_from_pdf(
                    pdf_file
                )
            )

        except Exception as e:

            raise RuntimeError(
                f"PDF extraction failed: {str(e)}"
            )


        if not raw_text:

            raise ValueError(
                "No text could be extracted from the PDF."
            )


        syllabus_text = (
            clean_text(
                raw_text
            )
        )


        if not syllabus_text:

            raise ValueError(
                "Syllabus text is empty after cleaning."
            )


        print(
            "Syllabus extracted successfully."
        )

        print(
            "Characters extracted:",
            len(syllabus_text)
        )


        # ==================================================
        # STEP 2: CHUNKING
        # ==================================================

        print(
            "\n[STEP 2] Creating text chunks..."
        )


        try:

            chunks = (
                chunk_text(
                    syllabus_text
                )
            )

        except Exception as e:

            raise RuntimeError(
                f"Text chunking failed: {str(e)}"
            )


        if not chunks:

            raise ValueError(
                "No chunks were created from the syllabus."
            )


        print(
            "Number of chunks:",
            len(chunks)
        )


        # ==================================================
        # STEP 3: EMBEDDINGS
        # ==================================================

        print(
            "\n[STEP 3] Generating embeddings..."
        )


        try:

            embeddings = (
                self.embedding_model.encode(
                    chunks
                )
            )

        except Exception as e:

            raise RuntimeError(
                f"Embedding generation failed: {str(e)}"
            )


        if embeddings is None:

            raise ValueError(
                "Embedding model returned None."
            )


        print(
            "Embeddings generated successfully."
        )


        # ==================================================
        # STEP 4: VECTOR DATABASE
        # ==================================================

        print(
            "\n[STEP 4] Building vector database..."
        )


        try:

            self.vector_store.build(
                chunks,
                embeddings
            )

        except Exception as e:

            raise RuntimeError(
                f"Vector database creation failed: {str(e)}"
            )


        print(
            "Vector database created successfully."
        )


        # ==================================================
        # STEP 5: RAG RETRIEVAL
        # ==================================================

        print(
            "\n[STEP 5] Retrieving relevant syllabus context..."
        )


        # RAG can use a larger portion of the syllabus.
        retrieval_query = (
            syllabus_text[:3000]
        )


        try:

            rag_context = (
                self.retriever.get_context(
                    retrieval_query,
                    top_k=5
                )
            )

        except Exception as e:

            print(
                "\nRAG RETRIEVAL ERROR:"
            )

            print(
                str(e)
            )

            rag_context = ""


        if rag_context:

            print(
                "RAG context retrieved successfully."
            )

        else:

            print(
                "WARNING: No RAG context found."
            )


        # ==================================================
        # STEP 6: PREPARE SHORT WEB CONTEXT
        # ==================================================

        print(
            "\n[STEP 6] Preparing concise web-search context..."
        )


        # IMPORTANT:
        #
        # Do NOT send the entire syllabus to Tavily.
        #
        # This is only a temporary concise context.
        #
        # Later, this can be replaced by an LLM-generated
        # domain summary.

        domain_context = (
            syllabus_text[:800]
        )


        print(
            "Web-search context characters:",
            len(domain_context)
        )


        # ==================================================
        # STEP 7: TAVILY WEB SEARCH
        # ==================================================

        print(
            "\n[STEP 7] Starting Tavily web search..."
        )


        web_query = f"""
Find current and reliable industry information
related to this academic domain.

Focus specifically on:

- Industry-relevant skills
- Job roles
- Technologies
- Software tools
- Programming languages
- Certifications
- Career opportunities
- Industry trends
- Required skills
- Emerging technologies

Academic syllabus context:

{domain_context}
"""


        print(
            "\n========== WEB QUERY =========="
        )

        print(
            web_query
        )

        print(
            "==============================="
        )


        # --------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT silently convert Tavily errors into [].
        #
        # If Tavily fails, the actual error will be shown.
        # --------------------------------------------------

        try:

            web_results = (
                self.web_search.search(
                    web_query,
                    max_results=10
                )
            )

        except Exception as e:

            print(
                "\n========================================"
            )

            print(
                "TAVILY WEB SEARCH FAILED"
            )

            print(
                "========================================"
            )

            print(
                "Error type:",
                type(e).__name__
            )

            print(
                "Error:",
                str(e)
            )

            print(
                "========================================"
            )


            raise RuntimeError(
                f"Tavily web search failed: {str(e)}"
            )


        # --------------------------------------------------
        # PROTECT AGAINST NONE
        # --------------------------------------------------

        if web_results is None:

            web_results = []


        print(
            "\n========================================"
        )

        print(
            "Number of web sources:",
            len(web_results)
        )

        print(
            "========================================"
        )


        # ==================================================
        # STEP 7B: FORMAT WEB RESULTS
        # ==================================================

        print(
            "\n[STEP 7B] Formatting web context..."
        )


        if web_results:

            try:

                web_context = (
                    self.web_search.format_results(
                        web_results
                    )
                )

            except Exception as e:

                print(
                    "WEB FORMAT ERROR:"
                )

                print(
                    str(e)
                )

                web_context = str(
                    web_results
                )

        else:

            web_context = (
                "No live web search results are available."
            )


        print(
            "Web context prepared."
        )


        # ==================================================
        # STEP 8: MULTI-AGENT SYSTEM
        # ==================================================

        print(
            "\n[STEP 8] Running multi-agent system..."
        )


        try:

            result = (
                self.orchestrator.run(

                    syllabus_text=syllabus_text,

                    rag_context=rag_context,

                    web_context=web_context
                )
            )

        except Exception as e:

            raise RuntimeError(
                f"Multi-agent orchestration failed: {str(e)}"
            )


        if result is None:

            raise ValueError(
                "Orchestrator returned None."
            )


        # ==================================================
        # STEP 8B: NORMALIZE RESULT
        # ==================================================

        if isinstance(
            result,
            str
        ):

            result = {

                "report":
                result

            }


        elif not isinstance(
            result,
            dict
        ):

            result = {

                "report":
                str(result)

            }


        print(
            "Multi-agent analysis completed."
        )


        # ==================================================
        # STEP 9: ADD WEB SOURCES
        # ==================================================

        print(
            "\n[STEP 9] Adding web sources..."
        )


        # IMPORTANT:
        #
        # The actual Tavily results are preserved here.
        #

        result["sources"] = (
            web_results
        )


        result["syllabus_text"] = (
            syllabus_text
        )


        result["rag_context"] = (
            rag_context
        )


        result["web_context"] = (
            web_context
        )


        print(
            "Final web source count:",
            len(
                result["sources"]
            )
        )


        # ==================================================
        # STEP 10: PIPELINE METADATA
        # ==================================================

        result["pipeline_status"] = (
            "success"
        )


        result["chunk_count"] = (
            len(chunks)
        )


        # ==================================================
        # STEP 11: FINAL STATUS
        # ==================================================

        print(
            "\n========================================"
        )

        print(
            "Academic Career Pipeline Completed"
        )

        print(
            "Final Web Sources:",
            len(
                result["sources"]
            )
        )

        print(
            "========================================"
        )


        # ==================================================
        # RETURN
        # ==================================================

        return result