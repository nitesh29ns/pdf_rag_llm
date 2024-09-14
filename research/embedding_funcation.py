from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_funcation():
    embedding = OllamaEmbeddings(model="nomic-embed-text")

    return embedding
