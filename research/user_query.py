import argparse
from langchain_community.vectorstores import Chroma
#from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from embedding_funcation import get_embedding_funcation

CHROMA_PATH = './user_data'

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---


Answer the question based on the above context: {question}
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="question you want to asked.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text:str):
    embedding_function = get_embedding_funcation()
    db =Chroma(persist_directory=CHROMA_PATH, 
               embedding_function=embedding_function)

    Results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc ,_score in Results])
    
    prompt_tamplate = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_tamplate.format(context=context_text, question=query_text)
    print(prompt)

    model = Ollama(model="llama3.1:8b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get('id', None) for doc, _score in Results]
    formatted_response = f"Response: {response_text}\nScource: {sources}"
    print(formatted_response)
    
    return response_text


if __name__ == "__main__":
    main()