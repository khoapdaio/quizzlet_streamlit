import json
from typing import List
import streamlit as st

# Hàm hiển thị và kiểm tra câu hỏi
def display_questions(questions: List['Question'], user_answers: dict):
    for question in questions:
        st.markdown(f'##### {question.content}')
        answer = get_user_answer(question)
        user_answers[question.question_id] = answer

        if 'answers' in st.session_state and st.session_state['answers'] == "True":
            with st.expander("Answers"):
                st.write(f"Đáp án: {question.answer}")


# Hàm lấy câu trả lời của người dùng cho từng loại câu hỏi
def get_user_answer(question: 'Question'):
    if question.q_type in ["true_false", "single_choice"]:
        return st.radio(f"Trả lời câu hỏi {question.question_id}", question.options, key=f"q{question.question_id}")
    elif question.q_type == "multi_choice":
        return st.multiselect(f"Trả lời câu hỏi {question.question_id}", question.options, key=f"q{question.question_id}")
    elif question.q_type == "write_answer":
        return st.text_input(f"Trả lời câu hỏi {question.question_id}", key=f"q{question.question_id}")
    return None


# Hàm kiểm tra câu trả lời và hiển thị kết quả
def check_answers(questions: List['Question'], user_answers: dict):
    correct_count = 0
    results = []

    for question in questions:
        is_correct = evaluate_answer(question, user_answers[question.question_id])
        results.append((question.question_id, is_correct))
        if is_correct:
            correct_count += 1

    display_results(results, correct_count, len(questions))


# Hàm đánh giá câu trả lời
def evaluate_answer(question: 'Question', user_answer):
    if question.q_type == "multi_choice":
        return set(user_answer) == set(question.answer)
    elif question.q_type == "write_answer":
        return user_answer.strip().lower() == question.answer.strip().lower()
    else:
        return user_answer == question.answer


# Hàm hiển thị kết quả
def display_results(results, correct_count, total_questions):
    question_div = ""
    for question_id, is_correct in results:
        question_div += f"""<div style='width: 50px; height: 50px; background-color: white; 
        				display: flex; align-items: center; justify-content: center; margin: 5px;
        				 border: 2px solid {'green' if is_correct else 'red'}; border-radius: 10px;'>
        				{question_id} </div>"""
    st.markdown(f"""<div style='display: flex;align-items: center;
    				justify-content: flex-start;flex-wrap: wrap;'>{question_div}</div>
    				<div>Bạn đã trả lời đúng {correct_count} / {total_questions} câu hỏi.</div>
    				""", unsafe_allow_html = True)


# Hàm đọc câu hỏi từ JSON
def get_questions_from_json(json_quizz) -> List['Question']:
    data = json.loads(json_quizz)
    return [
        Question(
            question_id=item["id"],
            level=item["level"],
            q_type=item["type"],
            content=item["content"],
            options=item["options"],
            answer=item["answer"]
        ) for item in data
    ]


# Class mô tả câu hỏi
class Question:
    def __init__(self, question_id: int, level: str, q_type: str, content: str, options: List[str], answer: str):
        self.question_id = question_id
        self.level = level
        self.q_type = q_type
        self.content = content
        self.options = options
        self.answer = answer


# Hàm chính của ứng dụng
def main():
    st.set_page_config(layout="wide")
    st.title('Quizzlet')
    st.sidebar.title("Generate Quizzlet")
    quizzlet = st.sidebar.text_area("Quizzlet Streamlit")
    submit = st.sidebar.button('Submit')

    if submit:
        st.session_state['quizzlet'] = quizzlet
        if not quizzlet.strip():
            st.warning("Quizzlet is empty")
        if 'answers' in st.session_state:
            st.session_state.pop("answers")

    user_answers = {}

    if 'quizzlet' in st.session_state:
        questions = get_questions_from_json(st.session_state['quizzlet'])
        col1, col2 = st.columns([2, 1])

        with col1:
            display_questions(questions, user_answers)

        with col2:
            st.session_state['answers'] = "True"
            if st.button("Kiểm tra tất cả các câu hỏi"):
                check_answers(questions, user_answers)


if __name__ == '__main__':
    main()
