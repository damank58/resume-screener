import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
load_dotenv()

class ResumeAI(object):
    def __init__(self):
        self.chunk_size = 400
        self.chunk_overlap = 200
        self.openai_key = os.environ['OPENAI_API_KEY']
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"
        self.CONNECTION_STRING = os.environ['PGVECTOR_CONNECTION_STRING']
        self.COLLECTION_NAME = "resume_embeddings"

    def loader(self, file_path):
        if os.path.basename(file_path).split(sep=".")[1].lower() == 'pdf':
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            return docs
        else:
            return None


    def splitter(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = text_splitter.split_documents(docs)
        return chunks

    def get_embedding(self):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key, model=self.embedding_model)
        return embeddings

    def get_pgvector_connection(self, embeddings):
        pg_vectordb = PGVector(connection_string= self.CONNECTION_STRING,
                               collection_name=self.COLLECTION_NAME,
                               embedding_function=embeddings,
                               use_jsonb=True)
        return pg_vectordb

    def load_docs_to_vs(self, chunks, embeddings):
        docs_vectordb = self.get_pgvector_connection(embeddings).from_documents(documents=chunks,
                                                                                embedding=embeddings,
                                                                                collection_name=self.COLLECTION_NAME,
                                                                                connection_string=self.CONNECTION_STRING)
        return docs_vectordb

    def retriever(self, db, file_path):
        return db.as_retriever(search_kwargs={'filter': {'source': file_path}})

    def llm(self):
        llm = ChatOpenAI(model=self.chat_model, openai_api_key=self.openai_key)
        return llm

    def retrieval_qa(self, llm, retriever):
        qa_stuff = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            return_source_documents=True,
            retriever=retriever,
            verbose=True
        )
        return qa_stuff

    def run_for_candidate_profile(self, file_path):
        docs = self.loader(file_path)
        chunks = self.splitter(docs)
        embeddings = self.get_embedding()
        pg_vectordb = self.load_docs_to_vs(chunks, embeddings)
        retriever = self.retriever(pg_vectordb, file_path)
        llm = self.llm()
        qa_stuff = self.retrieval_qa(llm, retriever)
        return qa_stuff

    def run_for_chat(self, file_path):
        embeddings = self.get_embedding()
        pg_vectordb = self.get_pgvector_connection(embeddings)
        retriever = self.retriever(pg_vectordb, file_path)
        llm = self.llm()
        qa_stuff = self.retrieval_qa(llm, retriever)
        return qa_stuff