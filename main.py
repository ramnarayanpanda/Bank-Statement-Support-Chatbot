from graph import graph
from utils.db_utils import *

if __name__ == "__main__":

    # setup_database()

    initial_state = {
        "user_id": "1001",
        "user_password": "Password",
        "questions": [],
        "answers": [],
        "chat_history": [],
        "question_type": "",
        "retrieved_docs": "",
        "grade_of_retrieved_docs": "",
        "cur_reframe_cnt": 0,
        "max_reframe_cnt": 3
    }
    res = graph.invoke(initial_state)