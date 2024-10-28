import streamlit as st
import json
from typing import List



def main():
	st.set_page_config(layout = "wide")
	st.title('Quizzlet')
	st.sidebar.title("Generate Quizzlet")
	quizzlet = st.sidebar.text_area("Quizzlet Streamlit")
	submit = st.sidebar.button('Submit')

	if submit:
		st.session_state['quizzlet'] = quizzlet
		if quizzlet is None or quizzlet == "":
			st.warning("Quizzlet is empty")
	# Lưu câu trả lời của người dùng
	user_answers = {}
	if 'quizzlet' in st.session_state:
		col1, col2 = st.columns([2, 1])
		with col1:

			questions: [Question] = get_questions_from_json(quizzlet)
			for question in questions:
				st.markdown(f'##### {question.content}')
				answer = None
				if question.q_type == "true_false":
					answer = st.radio(f"Trả lời câu hỏi {question.question_id}", question.options,
					                  key = f"q{question.question_id}",index=None)
				elif question.q_type == "single_choice":
					answer = st.radio(f"Trả lời câu hỏi {question.question_id}", question.options,
					                  key = f"q{question.question_id}",index=None)
				elif question.q_type == "multi_choice":
					answer = st.multiselect(f"Trả lời câu hỏi {question.question_id}", question.options,
					                        key = f"q{question.question_id}")
				user_answers[question.question_id] = answer
		with col2:
			# Nút kiểm tra tất cả các câu hỏi
			if st.button("Kiểm tra tất cả các câu hỏi"):
				correct_count = 0
				results = []
				for question in questions:
					is_correct = False
					if question.q_type == "multiple_choice_multiple":
						if set(user_answers[question.question_id]) == set([question.answer]):
							is_correct = True
					else:
						if user_answers[question.question_id] == question.answer:
							is_correct = True
					results.append((question.question_id, is_correct))
					if is_correct:
						correct_count += 1

				# Hiển thị kết quả dưới dạng lưới 4 cột
				question_div = ""
				for result in results:
					question_id, is_correct = result
					border_color = "green" if is_correct else "red"
					question_div += f"""<div style='width: 50px; height: 50px; background-color: white; 
					                display: flex; align-items: center; justify-content: center; margin: 5px;;
					                 border: 2px solid {border_color}; border-radius: 10px;'>
					                {question_id}
					                </div>"""

				st.markdown(f"""<div style='display: flex;align-items: center;
				justify-content: flex-start;flex-wrap: wrap;'>{question_div}</div>
				<div>Bạn đã trả lời đúng {correct_count} / {len(questions)} câu hỏi.</div>
				""",unsafe_allow_html = True)



def get_questions_from_json(json_quizz) -> []:
	data = json.loads(json_quizz)
	questions = [
		Question(
			question_id = item["id"],
			level = item["level"],
			q_type = item["type"],
			content = item["content"],
			options = item["options"],
			answer = item["answer"]
		) for item in data
	]
	return questions


class Question:
	def __init__(self, question_id: int, level: str, q_type: str, content: str, options: List[str], answer: str):
		self.question_id = question_id
		self.level = level
		self.q_type = q_type
		self.content = content
		self.options = options
		self.answer = answer


if __name__ == '__main__':
	main()
