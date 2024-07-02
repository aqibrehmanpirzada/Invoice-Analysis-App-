import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import pandas as pd
import tempfile

# Function to read and combine text from all pages in a PDF
def read_pdf(uploaded_file):
    # Save the uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Initialize PyPDFLoader with the temporary file path
    loader = PyPDFLoader(temp_file_path)

    # Load PDF and combine text from all pages
    docs = loader.load()
    combined_text = ""
    for doc in docs:
        combined_text += doc.page_content + "\n"

    # Delete the temporary file
    temp_file.close()
    return combined_text

# Streamlit app title and instructions
st.title("PDF Invoice Analyzer")
st.write("Upload a PDF invoice to analyze its content.")

# File upload widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Process the uploaded PDF file
    pdf_text = read_pdf(uploaded_file)

    # Initialize OpenAI client
    openai_api_key = "Enter api Key Here"
    llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

    # Define template for OpenAI prompt
    template = """
    You are an intelligent bot that can analyze any text with invoice information. Your job is to read and analyze the information and create a JSON dictionary with the fields you find in the invoice.

    The output must be in JSON format, nothing else.

    {doc_text}
    """
    prompt = PromptTemplate(template=template, input_variables=["doc_text"])
    llmchain = LLMChain(llm=llm, prompt=prompt)

    # Invoke OpenAI model with PDF text
    response = llmchain.invoke({"doc_text": pdf_text})
    data = response["text"]
    data = data.replace("```json", "").replace("```", "").strip()

    try:
        # Attempt to parse JSON and convert to DataFrame
        invoice_data = json.loads(data)
        df = pd.json_normalize(invoice_data)

        # Display DataFrame
        st.subheader("Fields and their values from PDF Invoice")
        st.write(df)

    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON: {e}")
        st.write("Raw response from the model:")
        st.code(data)  # Display raw response from the model
