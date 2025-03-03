# import tiktoken
#
#
# def get_token_count(text, model="gpt-4o"):
#     encoding = tiktoken.encoding_for_model(model)  # Get the tokenizer for the specified model
#     tokens = encoding.encode(text)
#     return len(tokens)
#
# text = """Can I configure both one-time and recurring data sharing for GST?
# Can I set up both one-time and recurring data sharing for GST?
# Can I set up both one-time and recurring data sharing for GST?
# Can I set up both one-time and recurring data sharing for GST?
# Can you describe the types of data I can access regarding my Mutual Funds through the AA?
# Can you detail the types of information I can obtain regarding my Mutual Funds through the AA?
# Can you explain what kind of information I can retrieve about my Mutual Funds through the AA?
# Can you outline the types of data I can retrieve about my Mutual Funds through the AA?
# Can you tell me what information I can access about my Mutual Funds through the AA?
# Could you elaborate on the types of information available about my Mutual Funds through the AA?
# Could you explain the types of data I can retrieve about my Mutual Funds through the AA?
# Could you explain the types of information I can access regarding my Mutual Funds through the AA?
# For how long can I access GST data through the AA?
# For how long can I access GST data through the AA?
# For what duration is GST data available through the AA?
# For what duration is GST data available through the AA?
# For what duration is GST data available through the AA?
# How can I effectively manage my Mutual Funds using the AA?
# How can I manage my Mutual Funds effectively using the AA?
# How long can I access GST data through the AA?
# How long is GST data accessible through the AA?
# How long is GST data available for access through the AA?
# Is it possible to configure both one-time and recurring data sharing for GST?
# Is it possible to configure both one-time and recurring data sharing for GST?
# Is it possible to set up both one-time and recurring data sharing for GST?
# Is it possible to set up both one-time and recurring data sharing for GST?
# What approaches can I take to effectively manage my Mutual Funds with the AA?
# What are some effective methods to manage my Mutual Funds using the AA?
# What are some effective strategies for managing my Mutual Funds with the AA?
# What challenges should I be aware of when using Mutual Funds data?
# What challenges should I be aware of when using Mutual Funds data?
# What challenges should I be aware of when working with Mutual Funds data?
# What details do I need to provide to access my Mutual Funds and Equities?
# What difficulties might I encounter when using the Mutual Funds data?
# What do I need to provide to access my Mutual Funds and Equities?
# What do I need to submit to access my Mutual Funds and Equities?
# What do I need to submit to access my Mutual Funds and Equities?
# What do I need to submit to access my Mutual Funds and Equities?
# What GST information can I retrieve through the AA?
# What GST information can I retrieve through the AA?
# What GST information can I retrieve through the AA?
# What GST-related information can I access through the AA?
# What identifiers are necessary for discovering GSTINs?
# What identifiers are necessary to discover GSTINs?
# What identifiers are necessary to find GSTINs?
# What identifiers are needed to discover GSTINs?
# What identifiers are required to find GSTINs?
# What identifiers do I need to discover GSTINs?
# What identifiers do I need to find GSTINs?
# What identifiers do I need to find GSTINs?
# What identifiers do I need to provide to access my Mutual Funds and Equities?
# What information do I need to provide to access my Mutual Funds and Equities?
# What information do I need to provide to access my Mutual Funds and Equities?
# What issues might I encounter when working with Mutual Funds data?
# What kind of GST information can I access through the AA?
# What kind of GST-related information can I access through the AA?
# What kind of GST-related information can I access through the AA?
# What kind of GST-related information can I access through the AA?
# What methods can I use to effectively manage my Mutual Funds with the AA?
# What methods can I use to effectively manage my Mutual Funds with the AA?
# What potential issues should I be aware of when using Mutual Funds data?
# What potential issues should I consider when working with Mutual Funds data?
# What potential problems should I consider when using Mutual Funds data?
# What strategies can I use to manage my Mutual Funds effectively with the AA?
# Which categories of taxpayers can share their GSTR information?
# Which taxpayers are permitted to share their GSTR information?
# Which types of taxpayers are eligible to share their GSTR?
# Who is allowed to share their GSTR information?
# Who is eligible to share GSTR information?
# Who is eligible to share their GSTR information?
# Who qualifies to share GSTR information?
# Who qualifies to share their GSTR information?"""
#
# print(get_token_count(text))






from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredExcelLoader, PyPDFLoader

def split_large_text(text, chunk_size=4000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_raw_data(src_file):
    if src_file.endswith(".docx"):
        loader = Docx2txtLoader(src_file)
    elif src_file.endswith(".xlsx"):
        loader = UnstructuredExcelLoader(src_file)
    elif src_file.endswith(".pdf"):
        loader = PyPDFLoader(src_file)
    else:
        loader = None
    raw_data = loader.load()
    return raw_data[0].page_content


raw_data = get_raw_data("/home/rampanda/Documents/DG Assist/data/bank_data/AA - Insights on Mutual Funds, Equities & GST.docx")
print(raw_data)

