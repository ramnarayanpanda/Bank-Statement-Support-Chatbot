from langchain_core.messages import HumanMessage, AIMessage
import asyncio
import threading

from state import CustomState
from prompts_llms import *
from utils.data_retrieval import VectorStoreRetriever
from utils.db_utils import *

route_question_chain = llm_route_question()
grade_docs_chain = llm_grade_docs()
reframe_user_question_chain = llm_reframe_user_question()
generate_answer_chain = llm_generate_answer()
generate_technical_answer_chain = llm_generate_technical_answer()
retriever_object = VectorStoreRetriever(project_name="bank_data")


def node_user_authentication(state: CustomState) -> CustomState:

    while True:
        is_new_user = input("If you are new user, then put yes or put no>").strip().lower()
        if is_new_user in ['yes', 'no']:

            user_id = input("Please put your email>").strip().lower()
            user_password = input("Please put your password>").strip()
            if is_new_user == 'yes':
                status = register_user(user_id, user_password)
                if status:
                    break
            elif is_new_user == 'no':
                status = authenticate_user(user_id, user_password)
                if status:
                    break

        else:
            print("Please only select enter yes or no")

    state['user_id'] = user_id
    state['user_password'] = user_password
    chat_history = load_conversation_history(user_id)[1:][:-1]
    if chat_history:
        state['chat_history'] = eval(chat_history)
    else:
        state['chat_history'] = []
    return state


def node_get_question(state: CustomState) -> CustomState:
    print(f"node_called: node_get_question")
    question = input("Enter your question:>").strip()
    state['questions'].append(HumanMessage(content=question))
    return state


def node_question_router(state: CustomState) -> CustomState:
    print(f"node_called: node_question_router")
    # question refers to the latest question that user has asked
    question = state['questions'][-1]
    chat_history = state['chat_history']

    question_type = route_question_chain.invoke({'question': [question], 'chat_history': chat_history}).variable
    state['question_type'] = question_type
    print("Here>>>>>>>>>", state)
    return state


def node_grade_docs(state: CustomState) -> CustomState:
    print(f"node_called: node_grade_docs")
    question = state['questions'][-1]
    # get retrieved docs and convert them to HumanMessage so that we can send them to llm
    retrieved_docs = HumanMessage(
        content = retriever_object.transform(question.content)
    )
    state['retrieved_docs'] = retrieved_docs

    grade_of_retrieved_docs = grade_docs_chain.invoke(
        {'question': [question], 'retrieved_docs': [retrieved_docs]}
    ).variable
    state['grade_of_retrieved_docs'] = grade_of_retrieved_docs
    return state


def node_reframe_question(state: CustomState) -> CustomState:
    print(f"node_called: node_reframe_question")
    question = state['questions'][-1]
    # reframe may need last few questions to reframe it better, so for now I am including just last 3 question
    last_few_questions = state['questions'][-3:]

    reframed_question = reframe_user_question_chain.invoke({'question': [question], 'last_few_questions': last_few_questions}).variable

    # here reframed_question will have the type as AIMessage, but we need to convert it to HumanMessage before appending
    state['questions'].append(HumanMessage(content=reframed_question))
    state['cur_reframe_cnt'] += 1
    return state


def node_generate_answer(state: CustomState) -> CustomState:
    print(f"node_called: node_generate_answer")
    question = state['questions'][-1]
    chat_history = state['chat_history']
    retrieved_docs = state['retrieved_docs']

    # retrieve docs from vector store
    answer = generate_answer_chain.invoke(
        {
            'chat_history': chat_history,
            'question': [question],
            'retrieved_docs': [retrieved_docs]
        }
    ).variable
    print(answer)

    state['answers'].append(answer)
    state['chat_history'].append(question)
    state['chat_history'].append(AIMessage(content=answer))
    # this update may not be necessary cause I am already updating it inside node_get_question
    state['cur_reframe_cnt'] = 0
    return state


def node_generate_technical_answer(state: CustomState) -> CustomState:
    print(f"node_called: node_generate_technical_answer")
    question = state['questions'][-1]
    answer = generate_technical_answer_chain.invoke({'question': [question]}).variable
    print(answer)

    state['chat_history'].append(question)
    state['chat_history'].append(AIMessage(content=answer))
    return state


def node_update_db(state: CustomState) -> CustomState:
    print("\nhere we are::::::::::", type(state['user_id']), type(state['chat_history']))
    print("\nhere we are::::::::::", state['chat_history'])
    save_conversation_history(state['user_id'], str(state['chat_history']))
    print("here we are:::::::::: save completed")
    return state


def node_get_sql_query(state: CustomState) -> CustomState:
    return state