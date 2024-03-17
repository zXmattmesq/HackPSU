from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def vector_search(query):
    documents = []

    # Load documents from each CSV file
    for i in range(2, 4):
        file_path = f"tokenized_data_{i}.csv"
        loader = CSVLoader(file_path=file_path)
        documents.extend(loader.load())

    # Create vector store from loaded documents
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Search for similar documents for the given query
    similar_responses = []
    for i in range(4):
        similar_response = vectorstore.similarity_search(query, k=2)
        similar_responses.extend([doc.page_content for doc in similar_response])

    return similar_responses

model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

template = """
Based on the previous best practice examples bellow, answer the question:

Question:

{input message}

Past Examples:

{vector_search_results}

Be human and friendly but most importantly do not answer anything an advior would not, and do not fabricate, invent, or extrapolate information. be specific to the examples and question, make sure to directly reference the best match of question and previous examples.
As an advisor, you must respond as if having a conversation. Do not mention that you are an AI, that you are an advisor, or that you were given best practice examplse.

"""

prompt = PromptTemplate(
    input_variables=["input message", "vector_search_results"],
    template=template
)

chain = LLMChain(llm=model, prompt=prompt)


def get_response(input_message):
    input_data = {
        'input message': input_message,
        'vector_search_results': vector_search(input_message)
    }
    response = chain.run(input_data)
    return response


def main():
    st.set_page_config(
        page_title="Kweery"
    )

    col1, col2 = st.columns([1, 3])  
    col1.image("guy.png", use_column_width=True) 

    with col2:
        st.header("Kweery")
        message = st.text_area("What do you want to ask me?", height=200)  

        if message:
            result = get_response(message)
            st.write(" "*20) 
            st.write(" "*20) 
            st.write("One second I'm thinking...")
            st.info(result)

if __name__ == '__main__':
    main()