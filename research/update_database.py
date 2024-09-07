import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_funcation import get_embedding_funcation
from langchain_community.vectorstores import Chroma

DATA_PATH = "./Data"
CHROMA_PATH = "./user_data"


def main():

    # create or update data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
        


def load_documents():
    try:
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        return document_loader.load()
    except Exception as e:
        raise e
    
def split_documents(documents:list):
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
    

def add_to_chroma(chunks:list):
    try:
        db = Chroma(
            persist_directory = CHROMA_PATH,
            embedding_function = get_embedding_funcation()
        )

        # calculate page ids
        chunks_with_ids = calculate_chunk_ids(chunks)

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
            db.persist()
        else:
            print("No new documents added.")
        
    except Exception as e:
        raise e
    

def calculate_chunk_ids(chunks:list):
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
    
def clear_database():
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
    except Exception as e:
        raise e
    


if __name__ =="__main__":
    main()