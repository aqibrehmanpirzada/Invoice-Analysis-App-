import streamlit as st

def main():
    st.title('Invoice Analyzer App')
    
    st.markdown("""
    Welcome to the Invoice Analyzer App! This app helps you analyze and extract information from invoices automatically. 
    Upload your invoices, and let our powerful AI engine process them to extract key data such as total amount, due date, 
    vendor details, and more. Streamline your invoice management process with ease!
    """)

    st.markdown('---')

    st.header('Key Features:')
    st.markdown("""
    - **Upload PDF Invoices**: Upload your invoice PDF files for analysis.
    - **Automatic Data Extraction**: Extract key data such as total amount, due date, and vendor details.
    - **Efficient Invoice Management**: Streamline your invoice processing workflow.
    """)

    st.markdown('---')

    st.subheader('How to Use:')
    st.markdown("""
    1. Upload your invoice PDF file using the file uploader.
    2. Our app will automatically process the uploaded invoice to extract relevant information.
    3. Review and use the extracted data for your invoice management needs.
    """)

if __name__ == '__main__':
    main()
