import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import Docx2txtLoader, UnstructuredExcelLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


class CustomDataLoader:
    def __init__(self, src_dir, project_name, embed_type='openai', vector_store_type='faiss', vector_store_path="../vector_stores/"):
        self.src_dir = src_dir
        self.embed_type = embed_type
        self.vector_store_type = vector_store_type
        self.vector_store_path = os.path.join(vector_store_path, project_name + "_" + vector_store_type)
        if not os.path.isdir(self.vector_store_path):
            os.makedirs(self.vector_store_path)

    def transform(self):
        documents = self._get_documents()
        embeddings = self._get_embeddings()
        status = self._save_embed_vector(documents, embeddings)

    def _get_documents(self):
        src_files_lst = os.listdir(self.src_dir)
        documents_list = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=500)

        for src_file in src_files_lst:
            print(f"Reading file {src_file}")
            src_file = os.path.join(self.src_dir, src_file)

            if src_file.endswith(".docx"):
                loader = Docx2txtLoader(src_file)
            elif src_file.endswith(".xlsx"):
                loader = UnstructuredExcelLoader(src_file)
            elif src_file.endswith(".pdf"):
                loader = PyPDFLoader(src_file)
            else:
                raise ValueError(f"The file format {src_file.split('.')[-1]} is not supported")

            raw_data = loader.load()
            documents = text_splitter.split_documents(raw_data)
            # here I am just adding more metadata to each document object returned by text splitter
            for i, doc in enumerate(documents):
                doc.metadata.update({'doc_cnt': i})
                documents_list.append(doc)

        return documents_list


    def _get_embeddings(self):
        if self.embed_type == 'openai':
            embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
        elif self.embed_type == 'ollama':
            embeddings = OllamaEmbeddings(model='llama3')
        else:
            raise ValueError(f"Embedding type {self.embed_type} is not supported.")
        return embeddings

    def _save_embed_vector(self, documents, embeddings):
        try:
            status = True

            if self.vector_store_type == "faiss":
                vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
                vector_store.save_local(self.vector_store_path)

            elif self.vector_store_type == 'pinecone':
                vector_store = PineconeVectorStore(index=os.environ['PINECONE_INDEX_NAME'], embedding = embeddings)
                vector_store.add_documents(documents=documents)

        except Exception as e:
            status = False

        return status


CustomDataLoader(src_dir="../data/bank_data/", project_name='bank_data').transform()