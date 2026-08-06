import os

from dotenv import load_dotenv
from tavily import TavilyClient


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


class WebSearch:

    def __init__(self):

        print("\n========================================")
        print("INITIALIZING TAVILY WEB SEARCH")
        print("========================================")

        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )

        if not self.api_key:

            raise ValueError(
                "TAVILY_API_KEY was not found in .env"
            )

        print(
            "TAVILY_API_KEY loaded successfully."
        )

        self.client = TavilyClient(
            api_key=self.api_key
        )

        print(
            "Tavily client initialized successfully."
        )


    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query,
        max_results=10
    ):

        if not query or not query.strip():

            raise ValueError(
                "Tavily search query is empty."
            )


        print("\n========================================")
        print("TAVILY SEARCH")
        print("========================================")

        print(
            "Query:",
            query[:1000]
        )

        print(
            "Maximum results:",
            max_results
        )


        try:

            response = self.client.search(

                query=query,

                search_depth="advanced",

                max_results=max_results

            )

        except Exception as e:

            raise RuntimeError(
                f"Tavily search failed: {str(e)}"
            )


        # ----------------------------------------------------
        # GET RESULTS
        # ----------------------------------------------------

        raw_results = response.get(
            "results",
            []
        )


        print(
            "Tavily returned:",
            len(raw_results),
            "results."
        )


        results = []


        for item in raw_results:

            url = item.get(
                "url",
                ""
            )

            title = item.get(
                "title",
                ""
            )

            content = item.get(
                "content",
                ""
            )


            if url:

                results.append({

                    "title": title,

                    "content": content,

                    "url": url

                })


        print(
            "Final usable web sources:",
            len(results)
        )


        for i, source in enumerate(
            results,
            start=1
        ):

            print(
                f"{i}. {source['title']}"
            )

            print(
                source["url"]
            )


        return results


    # ========================================================
    # FORMAT RESULTS
    # ========================================================

    def format_results(
        self,
        results
    ):

        if not results:

            return (
                "No live web search results are available."
            )


        formatted = []


        for i, result in enumerate(
            results,
            start=1
        ):

            formatted.append(

                f"""
WEB SOURCE {i}

TITLE:
{result.get("title", "")}

CONTENT:
{result.get("content", "")}

SOURCE:
{result.get("url", "")}
"""
            )


        return "\n".join(
            formatted
        )