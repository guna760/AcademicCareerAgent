import os

from dotenv import load_dotenv
from tavily import TavilyClient


print("========================================")
print("TAVILY DIRECT TEST")
print("========================================")


# Load .env
load_dotenv()


api_key = os.getenv("TAVILY_API_KEY")

print(
    "API key loaded:",
    bool(api_key)
)

if not api_key:

    raise ValueError(
        "TAVILY_API_KEY is not loaded."
    )


print(
    "API key prefix:",
    api_key[:8]
)


# Create Tavily client
client = TavilyClient(
    api_key=api_key
)


# VERY SIMPLE QUERY
query = "Python programming jobs"


print("\nQUERY:")
print(query)


try:

    response = client.search(

        query=query,

        search_depth="basic",

        max_results=10

    )

    print("\n========================================")
    print("RAW RESPONSE")
    print("========================================")

    print(response)


    results = response.get(
        "results",
        []
    )


    print("\n========================================")
    print(
        "RESULT COUNT:",
        len(results)
    )
    print("========================================")


    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nSOURCE {i}"
        )

        print(
            "TITLE:",
            result.get("title")
        )

        print(
            "URL:",
            result.get("url")
        )


except Exception as e:

    print("\n========================================")
    print("TAVILY ERROR")
    print("========================================")

    print(
        "ERROR TYPE:",
        type(e).__name__
    )

    print(
        "ERROR:",
        str(e)
    )