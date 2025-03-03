from langgraph.graph import StateGraph, START, END

from state import CustomState
from nodes import *


def cond_question_router(state: CustomState):
    print("\nstate question", state['questions'][-1], "\n")
    if state['questions'][-1].content == "That is all":
        print("update node called")
        return "node_update_db"
    elif state['question_type'].lower() == "type1":
        return "node_grade_docs"
    elif state['question_type'].lower() == "type2":
        return "node_generate_technical_answer"
    elif state['question_type'].lower() == "type3":
        print("I am not supposed answer these type of question.")
        return "node_get_question"
    return "node_get_question"


def cond_grade_docs(state: CustomState):
    if state['grade_of_retrieved_docs'].lower() == 'yes':
        return "node_generate_answer"
    elif state['grade_of_retrieved_docs'].lower() == 'no':
        return "node_reframe_question"
    elif state['cur_reframe_cnt'] >= state['max_reframe_cnt']:
        print("Could not get your question, please reframe it, Also make sure that you are asking relevant question only about the project")
        return "node_get_question"
    return "node_get_question"


builder = StateGraph(CustomState)
builder.add_node("node_user_authentication", node_user_authentication)
builder.add_node("node_get_question", node_get_question)
builder.add_node("node_question_router", node_question_router)
builder.add_node("node_grade_docs", node_grade_docs)
builder.add_node("node_reframe_question", node_reframe_question)
builder.add_node("node_generate_answer", node_generate_answer)
builder.add_node("node_generate_technical_answer", node_generate_technical_answer)
builder.add_node("node_update_db", node_update_db)

builder.add_edge(START, "node_user_authentication")
builder.add_edge("node_user_authentication", "node_get_question")
builder.add_edge("node_get_question", "node_question_router")
builder.add_conditional_edges(
"node_question_router",
    cond_question_router,
    path_map=['node_grade_docs', 'node_generate_technical_answer', 'node_get_question', 'node_update_db']
)
builder.add_edge("node_generate_technical_answer", "node_get_question")
builder.add_conditional_edges(
"node_grade_docs",
    cond_grade_docs,
    path_map=['node_generate_answer', 'node_reframe_question', 'node_get_question']
)
builder.add_edge("node_generate_answer", "node_get_question")
builder.add_edge("node_reframe_question", "node_grade_docs")
builder.add_edge("node_update_db", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path='architecture.png')
