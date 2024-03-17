from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

loader = CSVLoader(file_path=r"output.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

def vector_search(query):
    similar_response = vectorstore.similarity_search(query, k=3)

    contents_array = [doc.page_content for doc in similar_response]

    return contents_array

model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

template = """
You are playing the role of an advisor at Penn State university. Based on the previous best practice examples bellow, answer the question:

Question:

{input message}

Past Examples:

{vector_search_results}

Be human and friendly but most importantly do not answer anything an advior would not, and do not fabricate, invent, or extrapolate information.

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
        page_title="Penn State Advisor"
    )

    st.header("PSU Advisor")
    message = st.text_area("message")

    if message:
        st.write("Thinking...")

        result = get_response(message)

        st.info(result)

if __name__ == '__main__':
    main()