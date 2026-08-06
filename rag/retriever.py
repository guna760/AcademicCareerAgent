class Retriever:

    def __init__(
        self,
        embedding_model,
        vector_store
    ):

        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query,
        top_k=5
    ):

        query_embedding = (
            self.embedding_model
            .encode([query])[0]
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results

    def get_context(
        self,
        query,
        top_k=5
    ):

        results = self.retrieve(
            query,
            top_k
        )

        context = []

        for result in results:

            context.append(
                result["text"]
            )

        return "\n\n".join(context)