from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_funcation():
    embedding = OllamaEmbeddings(model="nomic-embed-text")

    return embedding


"""
# test the funcation

text = "This is the testing text for checking that our embedding funcation is working properly."

single_vector = get_embedding_funcation().embed_query(text)
print(str(single_vector)[:100])

"""