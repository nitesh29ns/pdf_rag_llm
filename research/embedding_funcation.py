import os
from langchain_nomic import NomicEmbeddings

os.system("nomic login nk-2qWDlRSfhpW2XxhDackPfJxBMJwVfFoxx_Hy-ae5dxE")

key = "nk-2qWDlRSfhpW2XxhDackPfJxBMJwVfFoxx_Hy-ae5dxE"

os.environ["COHERE_API_KEY"] = key


def get_embedding_funcation():
    embedding = NomicEmbeddings(
        model="nomic-embed-text-v1.5",)
    
    return embedding


"""
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name,trust_remote_code=True)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.model.encode(documents)

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0]

"""

"""
from sentence_transformers import SentenceTransformer


def get_embedding_funcation():
    embedding = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    
    return embedding



from langchain_nomic import NomicEmbeddings



def get_embedding_funcation():
    embedding = NomicEmbeddings(
        model="nomic-embed-text-v1.5",)
    
    return embedding


from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_funcation():
    embedding = OllamaEmbeddings(model="nomic-embed-text")

    return embedding

"""