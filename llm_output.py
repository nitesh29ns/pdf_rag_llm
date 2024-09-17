from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
#from langchain_community.llms.ollama import Ollama
from research.embedding_funcation import get_embedding_funcation
#from research.embedding_funcation import SentenceTransformerEmbeddings
import yaml


#model_name = "nomic-ai/nomic-embed-text-v1"
#embedding = SentenceTransformerEmbeddings(model_name)


with open(r"./constent.yaml") as f:
    con = yaml.safe_load(f)


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---


Answer the question based on the above context: {question}
"""

class generate_output():
    def __init__(self,chroma_path:str):
        try:
            self.chroma_path = chroma_path
        except Exception as e:
            raise e
        
    def query_rag(self,query_text:str):
        embedding_function = get_embedding_funcation()
        db =Chroma(persist_directory= self.chroma_path,
                embedding_function=embedding_function)

        Results = db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc ,_score in Results])
        
        prompt_tamplate = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        prompt = prompt_tamplate.format(context=context_text, question=query_text)
        print(prompt)

        # for local influence
        #model = Ollama(model="llama3.1:8b")
        #response_text = model.invoke(prompt)

        # using graq api
        llm = ChatGroq(
                temperature=0,
                groq_api_key= con['GROQ_API_KEY'],
                model_name="llama-3.1-70b-versatile"
            )

        response_text = llm.invoke(prompt)

        #sources = [doc.metadata.get('id', None) for doc, _score in Results]
        #formatted_response = f"Response: {response_text.content}\nScource: {sources}"
        #print(formatted_response)
        
        return response_text.content