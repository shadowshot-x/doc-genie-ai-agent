__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

def init_chroma_retiever():

    chroma_client = chromadb.Client()

    _ = chroma_client.create_collection(name="rag-chroma")

    file_paths = [
        "resources/opensource.txt"
    ]

    docs = [TextLoader(file_path).load() for file_path in file_paths]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)

    embedding_model = OllamaEmbeddings(model='granite3.2:2b')

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embedding_model)
    
    
    # vectorstore = Chroma("rag-chroma",embedding_model)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":1})

    return retriever
