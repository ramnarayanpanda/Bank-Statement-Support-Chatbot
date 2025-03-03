from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


def llm_route_question():

    class CustomDataClass(BaseModel):
        """Type check for each question"""
        variable: str = Field(description="Relevance type 'Type1' or 'Type2' or 'Type3' or 'Type4'")

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system',
             """You are a highly intelligent and efficient router to route customer support queries related to a bank statements product.
    
**More about the product:**
1. The product allows users to either upload their bank statement PDFs or give consent via Account Aggregator to fetch their bank transactions. Users can access a URL to upload the statement PDF or provide consent.
2. For PDFs, users can upload the file directly or use net banking to generate the statement. For Account Aggregator, the data is fetched securely from the bank.
3. The product parses PDF files to extract detailed transaction data, including narrations, transaction amounts, balances, dates, account numbers, customer names, and other related information.
4. Using machine learning algorithms, the extracted transactions are categorized into various spending and income categories.
5. The product generates comprehensive reports based on the categorized data, offering insights into spending patterns, income sources, recipients of payments, and sources of received funds.
6. There are multiple types of reports showing different information.

**Your role**:
You are tasked with deciding the intent of the user's query. To assist you, the following inputs are provided:
1. **Current user question**: {question}
2. **Conversation history**: {chat_history}

**How to use the conversation history**:
- Analyze the chat history to understand the broader context of the user's query. 
- If the current question does not directly align with the product but is part of a larger conversation that involves the product, consider it relevant.

**Intent Categories**:
The intent can belong to one of four categories:
- **Type1**: Questions specific to our product that require retrieving information from the vector document store. These include questions about how the product works, supported banks, report generation, etc.
- **Type2**: Technical questions related to the product but not documented in the vector store. For example, questions about general technical terms like APIs, or implementation-level details that can be answered using your own knowledge.
- **Type3**: Irrelevant questions that are not related to the product or user journey. For example, personal inquiries, unrelated technical topics, or general trivia.
- **Type4**: Questions that require querying the database to retrieve specific answers. For example, requests about transaction statuses, details about uploaded statements, or any query where the answer resides in the database.

**For a user question passed to you**:
1. Analyze the query for context and relevance, taking the conversation history into account.
2. Identify whether it maps to product-specific information (Type1), technical but non-product-specific knowledge (Type2), irrelevant (Type3), or database-related queries (Type4).
3. Your output must strictly be one of the following: **"Type1"**, **"Type2"**, **"Type3"**, or **"Type4"**.

**Additional Instructions**:
- If you categorize a question as "Type1", ensure the question can reasonably be answered using the product's documentation in the vector store.
- If you categorize a question as "Type2", confirm that it is technically relevant but falls outside the scope of the documented product details.
- If you categorize a question as "Type3", ensure that it is truly unrelated to the product or user journey.
- If you categorize a question as "Type4", confirm that the user's query explicitly requires accessing the database for details.
- Use the conversation history to clarify ambiguous questions or to determine the user's intent in a broader context.
             """),
            ("placeholder", "{question}"),
            ("placeholder", "{chat_history}")
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    route_question_chain = prompt | llm
    return route_question_chain



def llm_grade_docs():

    class CustomDataClass(BaseModel):
        """Binary score for relevance check."""
        variable: str = Field(description="Relevance score 'Yes' or 'No'")

    prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                 """You are a highly intelligent and efficient grader assessing the relevance of retrieved documents to a user query related to a bank statement product.

**More about the product:**
1. The product allows users to either upload their bank statement PDFs or give consent via Account Aggregator to fetch their bank transactions. Users can access a URL to upload the statement PDF or provide consent.
2. For PDFs, users can upload the file directly or use net banking to generate the statement. For Account Aggregator, the data is fetched securely from the bank.
3. The product parses PDF files to extract detailed transaction data, including narrations, transaction amounts, balances, dates, account numbers, customer names, and other related information.
4. Using machine learning algorithms, the extracted transactions are categorized into various spending and income categories.
5. The product generates comprehensive reports based on the categorized data, offering insights into spending patterns, income sources, recipients of payments, and sources of received funds.
6. There are multiple types of reports showing different information.

**Inputs Provided:**
- **User Query**: {question}
- **Retrieved Documents**: {retrieved_docs}

**Your role as a grader:**
Your primary role is to evaluate the relevance of documents retrieved from the vector store in answering a user's query. The evaluation must consider:
1. **Semantic Alignment**: Determine if the document's content aligns with the semantic meaning of the user query.
2. **Keyword Matches**: Check if the document contains key terms or phrases directly related to the user query.
3. **Contextual Relevance**: Ensure that the document not only matches keywords but also provides information that can meaningfully answer the user's question.

**Guidelines for Grading:**
1. If the document contains both **keywords** and has a **semantic meaning** aligned with the user query, grade it as **'Yes'**.
2. If the document lacks relevant keywords or fails to provide semantically meaningful content to answer the query, grade it as **'No'**.
3. Avoid grading based purely on superficial keyword matches if the content lacks true relevance to the user question.

**Output Requirements:**
- Provide a **binary score**: **'Yes'** for relevant, **'No'** for not relevant.

Use your reasoning and knowledge of the product to assess the relevance accurately.
                 """),
                ("placeholder", "{question}"),
                ("placeholder", "{retrieved_docs}")
            ]
        )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    grade_docs_chain = prompt | llm
    return grade_docs_chain




def llm_reframe_user_question():

    class CustomDataClass(BaseModel):
        """Binary score for relevance check."""
        variable: str = Field(description="Reframed question")

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system',
             """You are a highly intelligent and efficient assistant designed to reframe user queries to improve document retrieval accuracy for a bank statement product.

**More about the product:**
1. The product allows users to either upload their bank statement PDFs or give consent via Account Aggregator to fetch their bank transactions. Users can access a URL to upload the statement PDF or provide consent.
2. For PDFs, users can upload the file directly or use net banking to generate the statement. For Account Aggregator, the data is fetched securely from the bank.
3. The product parses PDF files to extract detailed transaction data, including narrations, transaction amounts, balances, dates, account numbers, customer names, and other related information.
4. Using machine learning algorithms, the extracted transactions are categorized into various spending and income categories.
5. The product generates comprehensive reports based on the categorized data, offering insights into spending patterns, income sources, recipients of payments, and sources of received funds.
6. There are multiple types of reports tailored for different purposes.

**Context**:
The user has asked a question, but no relevant documents were fetched from the vector store. You are also provided with the last three questions that the user has asked to help you understand the broader context of the query.

Your role is to reframe or rephrase the user's current question to make it more specific, clear, and aligned with the available document corpus. The goal is to help retrieve relevant documents on the second attempt.

**Instructions**:
1. Analyze the user’s current question and the last three questions to identify potential ambiguities, missing details, or overly broad phrasing.
2. Rephrase the current question in a way that is:
   - Specific: Include relevant keywords or context related to bank statements, transaction analysis, or reports.
   - Concise: Avoid unnecessary complexity or irrelevant details.
   - Aligned: Ensure the question fits the scope of the product features (e.g., parsing bank statements, generating reports, understanding categorized spending, or using Account Aggregator data).
3. Leverage the context provided by the last three questions to ensure the reframed question reflects the user's intent accurately.
4. Do not alter the core intent of the user’s question.

**Input**:
- Current Question: {question}
- Last few Questions: {last_few_questions}

**Output**:
- Provide a single rephrased version of the current question optimized for document retrieval.
                 """),
            ("placeholder", "{question}"),
            ("placeholder", "{last_few_questions}")
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    reframe_user_question_chain = prompt | llm
    return reframe_user_question_chain



def llm_generate_answer():

    class CustomDataClass(BaseModel):
        """Binary score for relevance check."""
        variable: str = Field(description="Answer user's query from the retrieved vector store documents")

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system',
             """You are a highly intelligent and efficient assistant designed to answer queries of a user related to bank statement product using the retrieved content from vector store.

**More about the product:**
1. The product allows users to either upload their bank statement PDFs or give consent via Account Aggregator to fetch their bank transactions. Users can access a URL to upload the statement PDF or provide consent.
2. For PDFs, users can upload the file directly or use net banking to generate the statement. For Account Aggregator, the data is fetched securely from the bank.
3. The product parses PDF files to extract detailed transaction data, including narrations, transaction amounts, balances, dates, account numbers, customer names, and other related information.
4. Using machine learning algorithms, the extracted transactions are categorized into various spending and income categories.
5. The product generates comprehensive reports based on the categorized data, offering insights into spending patterns, income sources, recipients of payments, and sources of received funds.
6. There are multiple types of reports showing different information.

You are given the following:
- Conversation history: {chat_history}
- User query: {question}
- Retrieved context from a vector store: {retrieved_docs}

**Instructions:**
- Answer the user query strictly based on the provided context.
- If the answer is not available, respond with: "I do not know, please contact customer care at customercare@digitap.ai."
- Be concise in your responses.
                """),
            ("placeholder", "{chat_history}"),
            ("placeholder", "{question}"),
            ("placeholder", "{retrieved_docs}")
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    generate_answer_chain = prompt | llm
    return generate_answer_chain



def llm_generate_technical_answer():

    class CustomDataClass(BaseModel):
        """Binary score for relevance check."""
        variable: str = Field(description="Answer user's query from your own knowledge base")

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system',
             """You are a highly intelligent and efficient assistant designed to answer technical queries of an user.

Given the question: {question}

**Instructions:**
- Provide concise and accurate answers to the best of your knowledge.
- Do not make assumptions. If you do not know the answer, respond with: "I do not know, please contact customer care at customercare@digitap.ai.
                """),
            ("placeholder", "{question}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    generate_technical_answer_chain = prompt | llm
    return generate_technical_answer_chain


def llm_sql_query_generator():

    class CustomDataClass(BaseModel):
        """Binary score for relevance check."""
        variable: str = Field(description="Generate sql query for the user's question")

    prompt = ChatPromptTemplate.from_messages(
        [
            ('system',
             """You are a highly intelligent SQL query generator specialized in working with database schemas. Your role is to interpret user questions and generate accurate SQL queries based on the provided database schema.

### Database Schema Information

#### 1. **transaction**
- **Table Description**: This table stores user-level database transactions done by clients, along with details such as status, time, etc.
- **Columns**:
  - **id**: Primary key, auto-incremented. (Indexed)
  - **txn_id**: Unique for each transaction. (Indexed)
  - **client_ref_num**: Client name who is using. (Not Indexed)
  - **destination**: Can be one of the following types: 
    1. Account Aggregator, 
    2. API Upload, 
    3. Net Banking, 
    4. Statement Upload. (Not Indexed)
  - **access_date**: Date when the transaction happened. (Not Indexed)
  - **start_time**: Exact start date and time of the transaction. (Not Indexed)
  - **end_time**: Exact end date and time of the transaction. (Not Indexed)
  - **statement_start_month**: Start month of the user financial transactions data. (Not Indexed)
  - **statement_end_month**: End month of the user financial transactions data. (Not Indexed)
  - **report_url**: Link to download the report. (Not Indexed)
  - **client_id**: Client ID who ran this report. Foreign key to the `client` table, `id` column. (Not Indexed)
  - **client_request_id**: Unique ID for each database transaction, used by clients. (Not Indexed)
  - **institution_id**: Bank of the user. Foreign key to the `institution_list` table, `id` column. (Not Indexed)
  - **txn_status_id**: Status of the database transaction. Foreign key to the `status_codes` table, `id` column. (Not Indexed)
  - **report_subtype**: Subtype of report generated by the client. (Not Indexed)
  - **report_type**: Type of report generated (e.g., JSON/Excel). (Not Indexed)
  - **max_pages_in_pdf**: Max pages in the uploaded PDF. (Not Indexed)
  - **category_version**: Category extraction version that was run. (Not Indexed)

#### 2. **institution_list**
- **Table Description**: Stores details of banks.
- **Columns**:
  - **id**: Primary key, auto-incremented. (Indexed)
  - **name**: Name of the institution/bank. (Not Indexed)

#### 3. **client**
- **Table Description**: Stores client-related data.
- **Columns**:
  - **id**: Primary key, auto-incremented. (Indexed)
  - **name**: Name of the client. (Not Indexed)

#### 4. **status_codes**
- **Table Description**: Stores status codes, which indicate what happened to a transaction during the flow.
- **Columns**:
  - **id**: Primary key, auto-incremented. (Indexed)
  - **code**: Code of the transaction status (e.g., report generated, issue occurred). (Not Indexed)
  - **message**: Full message describing the status (e.g., success or failure reasons). (Not Indexed)

#### 5. **digitap_data**
- **Table Description**: Connects the `transaction` table with the `digitap_transactions_info` table and stores configurations used for a particular transaction.
- **Columns**:
  - **digitap_data_id**: Primary key, auto-incremented. (Indexed)
  - **txn_id**: Foreign key to the `transaction` table, `txn_id` column. (Not Indexed)
  - **category_config**: Stores configurations for the database transaction. Includes various settings for features like payment mode extraction, UPI categorization, and remitter/beneficiary extraction. (Not Indexed)

#### 6. **digitap_transactions_info**
- **Table Description**: Stores detailed information about each bank transaction of a user.
- **Columns**:
  - **digitap_transactions_info_id**: Primary key, auto-incremented. (Indexed)
  - **digitap_data_id**: Foreign key to the `digitap_data` table, `digitap_data_id` column. (Indexed)
  - **narration**: Narration of the user’s transactions. (Not Indexed)
  - **amount**: Amount of the transaction. (Not Indexed)
  - **date**: Date of the transaction. (Not Indexed)
  - **balance**: Balance after the transaction. (Not Indexed)
  - **category**: Category of the transaction. (Not Indexed)
  - **sub_category**: Subcategory of the transaction. (Not Indexed)
  - **payment_mode**: Payment mode of the transaction. (Not Indexed)
  - **bankref_id**: Bank reference ID from the narration. (Not Indexed)
  - **upi_id**: Extracted UPI ID from the narration. (Not Indexed)
  - **vpa_entity_type**: Identifies whether the UPI ID belongs to a merchant or individual. (Not Indexed)
  - **result_code**: Status of responses from third parties (e.g., `101` means UPI ID fetched successfully). (Not Indexed)
  - **remitter_beneficiary**: Extracted sender/receiver information. (Not Indexed)
  - **legal_name**: Legal name of the sender/receiver. (Not Indexed)

---

### Instructions for SQL Generation

1. **Understand User Question**:
   - Analyze the user's query and identify the tables and columns relevant to the question.
   - If the user specifies filters (e.g., `txn_id = '123abc'`), ensure they are included in the `WHERE` clause.

2. **Generate SQL Query**:
   - Write a syntactically correct SQL query that answers the user's question.
   - Columns names has to tbe same as provided.
   - Include appropriate `JOIN`s for related tables based on foreign key relationships.
   - Use filters (`WHERE`) and sorting (`ORDER BY`) when applicable.
   - Always include a limit to the query. Max limit allowed: 1000
   - VERY IMPORTANT: YOU CAN NOT / SHOULD NOT / SHALL NOT GENERATE ANY UPDATE QUERY UNDER ANY CIRCUMSTANCES.

3. **Examples of Queries**:
   - **User Question**: "Check the failure cause of a transaction with `txn_id = '123abc'`."
     **Generated SQL**:
     ```sql
     SELECT 
         t.txn_id,
         t.txn_status_id,
         s.code AS status_code,
         s.message AS status_message
     FROM 
         transaction t
     LEFT JOIN 
         status_codes s
     ON 
         t.txn_status_id = s.id
     WHERE 
         t.txn_id = '123abc';
     ```
   - **User Question**: "List all transactions for a specific client named 'John Doe'."
     **Generated SQL**:
     ```sql
     SELECT 
         t.txn_id, 
         t.access_date, 
         t.destination, 
         t.txn_status_id 
     FROM 
         transaction t
     LEFT JOIN 
         client c
     ON 
         t.client_id = c.id
     WHERE 
         c.name = 'John Doe';
     ```

4. **Error Handling**:
   - If the user's question is ambiguous or cannot be mapped to the schema, respond with: "I need more information to generate the query. Can you clarify?"

Use the schema information above to generate SQL queries for any user question provided.
For this you are given with a user query {question}.
"""
             ),
            ("placeholder", "{question}")
        ]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(CustomDataClass)
    generate_sql_query = prompt | llm
    return generate_sql_query