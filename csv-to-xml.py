import csv
import sys
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def csv_to_xml(csv_file_path, xml_file_path):
	# Create the root element
	root = ET.Element("wpProQuiz")

	# Add the header element
	header = ET.SubElement(root, "header")
	header.set("LEARNDASH_SETTINGS_DB_VERSION", "2.5")
	header.set("exportVersion", "1")
	header.set("ld_version", "4.10.0")
	header.set("version", "0.28")

	# Add the data and quiz elements
	data = ET.SubElement(root, "data")
	quiz = ET.SubElement(data, "quiz")

	# Extract the base name without the extension
	base_name = os.path.splitext(os.path.basename(csv_file_path))[0]

	# Add title, text, and post elements to quiz
	title = ET.SubElement(quiz, "title")
	title.set("titleHidden", "true")
	title.text = f"{base_name} Quiz"

	text = ET.SubElement(quiz, "text")
	text.text = f"{base_name} quiz"

	post = ET.SubElement(quiz, "post")
	post_title = ET.SubElement(post, "post_title")
	post_title.text = f"{base_name} quiz"
	ET.SubElement(post, "post_content")

	# Add quiz definition elements
	comment = ET.Comment(" =============== Custom Values =============== ")
	quiz.append(comment)

	result_text = ET.SubElement(quiz, "resultText", {"gradeEnabled": "true"})
	ET.SubElement(result_text, "text", {"prozent": "0"})

	ET.SubElement(quiz, "emailNotification").text = "0"
	ET.SubElement(quiz, "forms", {"activated": "false", "position": "0"})
	ET.SubElement(quiz, "quizModus", {"questionsPerPage": "0"}).text = "0"
	ET.SubElement(quiz, "quizRunOnce", {"cookie": "false", "time": "0", "type": "0"}).text = "false"
	ET.SubElement(quiz, "showMaxQuestion", {"showMaxQuestionPercent": "false", "showMaxQuestionValue": "0"}).text = "false"
	ET.SubElement(quiz, "statistic", {"activated": "true", "ipLock": "0"})
	ET.SubElement(quiz, "timeLimit").text = "0"
	ET.SubElement(quiz, "toplist", {"activated": "false"})

	comment_true = ET.Comment(" =============== True =============== ")
	quiz.append(comment_true)

	true_tags = ["answerRandom", "hideQuestionNumbering", "hideQuestionPositionOverview", "quizSummaryHide", 
	"showReviewQuestion", "skipQuestionDisabled"]
	for tag in true_tags:
		ET.SubElement(quiz, tag).text = "true"

	comment_false = ET.Comment(" =============== False =============== ")
	quiz.append(comment_false)

	false_tags = ["autostart", "btnRestartQuizHidden", "btnViewQuestionHidden", "disabledAnswerMark", 
	"forcingQuestionSolve", "hideAnswerMessageBox", "hideResultCorrectQuestion", "hideResultPoints",
	"hideResultQuizTime", "numberedAnswer", "prerequisite", "questionRandom", "showAverageResult",
	"showCategory", "showCategoryScore", "showPoints", "sortCategories", "startOnlyRegisteredUser",
	"userEmailNotification"]
	for tag in false_tags:
		ET.SubElement(quiz, tag).text = "false"

	comment_questions = ET.Comment(" =============== Questions =============== ")
	quiz.append(comment_questions)

	# Now create the questions element and nest it inside quiz
	questions = ET.SubElement(quiz, "questions")

	with open(csv_file_path, newline='') as csvfile:
		reader = csv.reader(csvfile)
		current_question_id = None
		question_elem = None
		answers_elem = None

		for row in reader:
			question_id, question_body, question_type, *answers = row

			# Check if we have moved to a new question
			if question_id != current_question_id:
				current_question_id = question_id

				# Create a new question element
				question_elem = ET.SubElement(questions, "question")
				question_elem.set("answerType", "single" if question_type == "Single" else "multiple")

				# Question ID
				title_elem = ET.SubElement(question_elem, "title")
				title_elem.text = question_id

				# Question points
				points_elem = ET.SubElement(question_elem, "points")
				points_elem.text = "1"

				# Question text
				question_text_elem = ET.SubElement(question_elem, "questionText")
				question_text_elem.text = question_body

				# Misc. elements
				for tag in ["correctMsg", "incorrectMsg", "category"]:
					ET.SubElement(question_elem, tag)

				tipMsg_elem = ET.SubElement(question_elem, "tipMsg")
				tipMsg_elem.set("enabled", "false")

				# More misc. elements
				for tag in ["correctSameText", "showPointsInBox", "answerPointsActivated", 
				"answerPointsDiffModusActivated", "disableCorrect"]:
					elem = ET.SubElement(question_elem, tag)
					elem.text = "false"

				# Create answers element
				answers_elem = ET.SubElement(question_elem, "answers")

			# Add answers to the question
			for i in range(0, len(answers), 2):
				correct, answer_body = answers[i], answers[i+1]
				answer_elem = ET.SubElement(answers_elem, "answer")
				answer_elem.set("correct", correct)	# Mark asnwer as correct if it is marked as such in CSV
				answer_elem.set("points", "0") # 'answerPointsActivated' quiz setting is false, so this is always 0

				answer_text_elem = ET.SubElement(answer_elem, "answerText")
				answer_text_elem.set("html", "false") # HTML formatting is not used
				answer_text_elem.text = answer_body 
	
	# Convert the ElementTree to a string
	xml_string = ET.tostring(root, encoding='utf-8')

	# Pretty-print the XML string
	parsed_xml = minidom.parseString(xml_string)
	pretty_xml = parsed_xml.toprettyxml(indent="    ", newl="\n", encoding="utf-8")

	# Write the pretty-printed XML to file
	with open(xml_file_path, "wb") as file:
	    file.write(pretty_xml)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python csv_to_xml.py <input_file.csv>\n")
		print("The input CSV file should be formatted with the following columns:")
		print('"ID", "Question", "Question Type", "IsCorrect1", "Answer1", "IsCorrect2", "Answer2", ...')
		print("Where: ")
		print(" - 'ID' is the unique ID of the question,")
		print(" - 'Question' is the text body of the question,")
		print(" - 'Question Type' is either 'Single' or 'Multiple',")
		print(" - 'IsCorrectN' is a boolean indicating if the answer is correct,")
		print(" - 'AnswerN' is the text of the answer.")
		print("\nFor single-answer questions:")
		print('question-001,"Single-answer Question Title?","Single","False","Incorrect Answer","True","Correct Answer","False","Incorrect Answer"')
		print("\nFor multiple-answer questions:")
		print('question-002,"Multiple-answer Question Title? (Choose TWO)","Multiple","True","Correct Answer 1","False","Incorrect Answer","True","Correct Answer 2","False","Incorrect Asnwer"')
		sys.exit(1)

	input_file = sys.argv[1]

	# Extract the base name without the extension
	base_name = os.path.splitext(os.path.basename(input_file))[0]

	# Construct the output XML file name
	xml_file = f"{base_name}.xml"

	csv_to_xml(input_file, xml_file)