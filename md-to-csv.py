import csv
import sys
import os 

def parse_markdown_quiz(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    questions = content.split('### ')[1:]  # Split the content by question
    parsed_data = []

    for idx, question in enumerate(questions):
        question_id = f"{sanitized_filename}-{idx+1:03}" # Use sanitized input filename as a question ID
        parts = question.strip().split('\n- [') # Strip away markdown list element and a part of chechbox element
        question_body = parts[0].strip().replace('\n', ' ')  # Remove newlines from question body
        answers = parts[1:] 
        question_type = 'Multiple' if '(Choose' in question_body else 'Single' # Question body must contain the line "(Choose N)" to be recognized as a multiple-choice question
        
        row = [question_id, question_body, question_type] # Create a new row for the question
        
        for answer in answers:
            correct = 'true' if 'x]' in answer else 'false' # Marking correct answers using the rest of the checkbox element
            answer_body = answer.replace('x]', '').replace(' ]', '').strip() # Remove the rest of the checkbox element, what's left is the body of an answer
            row.extend([correct, answer_body])  # Append answer to the CSV string

        parsed_data.append(row) # Parsed question+answers

    return parsed_data

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Quote all fields
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python md_to_csv.py <input_file.md>")
        print("The input file name will be used as a key for question IDs and will be visible in the resulting LearnDash quiz.\n")
        print("The input Markdown file should be formatted with questions and answers as follows:")
        print("\nFor single-answer questions:")
        print("### Single-answer Question Title?")
        print("- [ ] Incorrect Answer")
        print("- [x] Correct Answer")
        print("- [ ] Incorrect Answer")
        print("\nFor multiple-answer questions:")
        print("### Multiple-answer Question Title? (Choose TWO)")
        print("- [x] Correct Answer 1")
        print("- [ ] Incorrect Answer")
        print("- [x] Correct Answer 2")
        print("- [ ] Incorrect Answer")
        sys.exit(1)

    input_file = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(input_file))[0] 
    sanitized_filename = base_name.lower().replace(" ", "-") 
    output_file = f"{base_name}.csv"

    quiz_data = parse_markdown_quiz(input_file)
    write_to_csv(quiz_data, output_file)