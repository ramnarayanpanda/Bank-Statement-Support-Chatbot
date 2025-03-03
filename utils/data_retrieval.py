import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStoreRetriever:
    def __init__(self, project_name, embed_type='openai', vector_store_type='faiss', vector_store_path="./vector_stores/"):
        self.embed_type = embed_type
        self.vector_store_type = vector_store_type
        self.vector_store_path = os.path.join(vector_store_path, project_name + "_" + vector_store_type)

    def transform(self, question):
        embeddings = self._get_embeddings()
        vector_store = FAISS.load_local(
            self.vector_store_path, embeddings, allow_dangerous_deserialization=True
        )
        results = vector_store.similarity_search(
            question,
            k=7,
        )
        retrieved_docs = "Retrieved Docs: \n"
        print("Metadata for the retrieved docs", [i.metadata for i in results])

        for i, doc in enumerate(results):
            retrieved_docs += f"Document {i}: \n:" + doc.page_content + "\n"
        return retrieved_docs

    def _get_embeddings(self):
        if self.embed_type == 'openai':
            embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
        elif self.embed_type == 'ollama':
            embeddings = OllamaEmbeddings(model='llama3')
        else:
            raise ValueError(f"Embedding type {self.embed_type} is not supported.")
        return embeddings


# question = "What all banks are supported"
# res = VectorStoreRetriever(project_name='bank_data').transform(question)
# print(res)
#
# for doc in res:
#     print(doc.metadata)