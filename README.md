# LearnDash tools

## LearnDash quiz creator

LearnDash quiz creator consists the main `csv-to-xml.py` script that converts a CSV file into a valid XML quiz ready to be imported into LearnDash and an optional `md-to-csv.py` script to convert a Markdown version of a quiz into ready-to-use CSV.

### `md-to-csv.py`
Usage: 
```
python md_to_csv.py <input_file.md>
```

The input file name will be used as a key for question IDs and will be visible in the resulting LearnDash quiz.
The input Markdown file should be formatted with questions and answers as follows:

For single-answer questions:
```
### Single-answer Question Title?
- [ ] Incorrect Answer
- [x] Correct Answer
- [ ] Incorrect Answer
```

For multiple-answer questions:
```
### Multiple-answer Question Title? (Choose TWO)
- [x] Correct Answer 1
- [ ] Incorrect Answer
- [x] Correct Answer 2
- [ ] Incorrect Answer
```

### `csv-to-xml.py`
Usage:
```
python csv_to_xml.py <input_file.csv>
```

The input CSV file should be formatted with the following columns:
"ID", "Question", "Question Type", "IsCorrect1", "Answer1", "IsCorrect2", "Answer2", ...

Where: 
 - 'ID' is the unique ID of the question,
 - 'Question' is the text body of the question,
 - 'Question Type' is either 'Single' or 'Multiple',
 - 'IsCorrectN' is a boolean indicating if the answer is correct,
 - 'AnswerN' is the text of the answer.

For single-answer questions:
```
question-001,"Single-answer Question Title?","Single","False","Incorrect Answer","True","Correct Answer","False","Incorrect Answer"
```

For multiple-answer questions:
```
question-002,"Multiple-answer Question Title? (Choose TWO)","Multiple","True","Correct Answer 1","False","Incorrect Answer","True","Correct Answer 2","False","Incorrect Asnwer"
```

