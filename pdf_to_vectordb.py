import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from research.embedding_funcation import get_embedding_funcation
from langchain_community.vectorstores import Chroma


class vectordb:

    def __init__(self,pdf_path:str, chroma_path:str):
        try:
            self.pdf_path = pdf_path
            self.chroma_path = chroma_path
        except Exception as e:
            raise e
        
    def load_documents(self):
        try:
            document_loader = PyPDFLoader(self.pdf_path)
            return document_loader.load()
        except Exception as e:
            raise e
    
    def split_documents(self,documents:list):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 800,
                chunk_overlap = 80,
                length_function = len,
                is_separator_regex = False,
            )

            return text_splitter.split_documents(documents)
        
        except Exception as e:
            raise e
        

    def add_to_chroma(self,chunks:list):
        try:
            db = Chroma(
                persist_directory = self.chroma_path,
                embedding_function = get_embedding_funcation()
            )

            # calculate page ids
            chunks_with_ids = self.calculate_chunk_ids(chunks)

            # add or update documents
            existing_items = db.get(include=[])
            existing_ids = set(existing_items['ids'])
            print(f"Number of existing documents in DB {len(existing_ids)}.")

            # update DB with new documents
            new_chunks = []
            for chunk in chunks_with_ids:
                if chunk.metadata['id'] not in existing_ids:
                    new_chunks.append(chunk)

            if len(new_chunks):
                print(f"➕ Adding new documents: {len(new_chunks)}")
                new_chunks_ids = [chunk.metadata['id'] for chunk in new_chunks]
                db.add_documents(new_chunks, ids=new_chunks_ids)
                return "vector db is created."
            else:
                print("No new documents added.")
            
        except Exception as e:
            raise e
        

    def calculate_chunk_ids(self,chunks:list):
        try:
            last_page_id = None
            current_chunk_index = 0

            for chunk in chunks:
                source = chunk.metadata.get('source')
                page = chunk.metadata.get('page')
                current_page_id = f"{source}:{page}"

                if current_page_id == last_page_id: # check chunk is from the same page
                    current_chunk_index += 1
                else:
                    current_chunk_index = 0

                chunk_id = f"{current_page_id}:{current_chunk_index}"
                last_page_id = current_page_id

                chunk.metadata['id'] = chunk_id

            return chunks
        except Exception as e:
            raise e
        
    def upload_to_vectordb(self):
        try:
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            self.add_to_chroma(chunks)
            return "db created."
        except Exception as e:
            raise e
        


"""
dd = vectordb(pdf_path="D:/ml/PDF_RAG_llm/pdf_rag_llm/research/Data/monopoly.pdf",chroma_path="./test1")

d = dd.upload_to_vectordb()

print(d)"""