import os
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredExcelLoader, PyPDFLoader
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
from langchain_openai import ChatOpenAI
import re
import pandas as pd
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter


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


def get_token_count(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)  # Get the tokenizer for the specified model
    tokens = encoding.encode(text)
    return len(tokens)

def split_large_text(text, chunk_size=4000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_llm_output(raw_data, previous_questions):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
"""You are an AI assistant generating **natural, human-like** user questions and answers for a bank statement parsing and analysis product.

### **Strict Rules**:
1. **Focus on the part of the document for which questions has not been generated yet, are not present in the previous questions.
2. **Do NOT generate the exact same question** that has already been asked.
3. **Reword previous questions** in a way that makes them feel new (use synonyms, different tones, different user perspectives).
4. **Vary question styles**:
   - Conversational: ("how to upload statement")
   - Scenario-based: ("I got a salary increase—how can I check my past income?")
   - Direct: ("How do I categorize transactions?")
   - Slightly structured: ("What types of reports does the system generate?")
5. Ensure **questions sound human-like** and natural.

### **Output Format (MUST follow this JSON structure)**:
```json
[
  {{ "question": "some question1", "answer": "some answer1" }},
  {{ "question": "some question2", "answer": "some answer2" }}
]

### **Previously Generated Questions**:
{previous_questions}

### **Document Content**:
{documents_content}
"""
            ),
            ("placeholder", "{previous_questions}"),
            ("placeholder", "{documents_content}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    route_question_chain = prompt | llm
    result = route_question_chain.invoke({'previous_questions': [previous_questions], 'documents_content': [raw_data]})
    return result


src_folder = "/home/rampanda/Documents/DG Assist/data/bank_data/"

for file in os.listdir(src_folder):

    src_file = src_folder + file
    print(file)
    raw_data = get_raw_data(src_file)
    print("Token size of raw data: ", get_token_count(raw_data))
    prev_question_lst = []
    all_data = []
    chunks = split_large_text(raw_data)

    for j, _chunk in enumerate(chunks):
        print("Token count:", get_token_count(_chunk))
        for i in range(5):
            print(j, i)
            result = get_llm_output(raw_data, "\n".join(prev_question_lst))
            sub_data_lst = [eval(i) for i in re.findall(r"\{.*\}", result.content)]
            all_data.extend(sub_data_lst)
            prev_question_lst = [i['question'] for i in all_data]

    pd.DataFrame(all_data, columns=['question', 'answer']).to_excel("/home/rampanda/Documents/DG Assist/data/synthetic_data/" + src_file.split("/")[-1].split(".")[0] + ".xlsx", index=False)


