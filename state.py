from typing import Annotated

from langchain_core.messages import HumanMessage, AIMessage
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages


class CustomState(TypedDict):
    user_id: str
    user_password: str

    # questions variable can store more question than answers variable,
    # cause when we use reframe question then ww can have multiple questions, while only one answer (only if the llm is able to reframe the question correctly) for the last reframed question
    # hence it makes sense to use a separate question variable and messages variable
    # chat_history: For each answered question only, we will add the question and then the answer of the question, In between if there are any tool calls those messages will also get added here
    # chat_history is only useful in sending the chat history to the llm
    questions: Annotated[list[HumanMessage], add_messages]
    answers: Annotated[list[AIMessage], add_messages]
    chat_history: Annotated[list[AnyMessage], add_messages]

    question_type: str
    retrieved_docs: HumanMessage
    grade_of_retrieved_docs: str
    cur_reframe_cnt: int
    max_reframe_cnt: int
