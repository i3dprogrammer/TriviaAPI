# TriviaAPI
TriviaAPI

### GET /categories
Fetches a list of all available categories.
#### Return
An object with a single key, categories, that contains a dictionary with the key value pair id and type.
#### Example
```bash
curl -x GET http://localhost:3000/categories
```
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### GET /questions
Fetches all available questions with max of 10 per page, specifiy the required page to view more questions.
#### Return
An object with the following keys [questions, total_questions, categories, current_category] 
questions: represents a list of all the available questions (max 10)
total_questions: holds the count of all available questions
categories: all the available categories
current_category: the current searching category
#### Example
```bash
curl -x GET http://localhost:3000/questions
```
```json
{
  "categories": {
    ...
    ...
    ...
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    ...
    ...
    ...
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
  ],
  "total_questions": 19
}
```
### POST /questions
Depending on the body data either searches the questions or add a new question.

if the body contains a searchTerm, will perform case-insensitive search on the questions
Otherwise will try to add a new question.
#### Body
Should contain only ONE of the following.
##### 1. Searching Questions
searchTerm: the value to search the questions for.
##### 2. Adding Question
question: question title.
answer: the answer for the question.
diffculity: the difficulty of the question.
category: the category the question belongs to.
#### Return
##### Searching Questions
If the body contained a searchTerm, returns the following

An object with the following keys [questions, total_questions, categories, current_category] 
questions: represents a list of questions that matches the search criteria (max 10)
total_questions: the count of all the questions that matches the search criteria
categories: all the available categories
current_category: the current searching category
##### Adding Question
An object with a single key success, representing the status of the action.
#### Example
##### Searching Questions
```bash
curl --location --request POST 'http://127.0.0.1:5000/questions' --header 'Content-Type: application/json' --data-raw '{ "searchTerm": "Whose" }'
```
```json
{
  "categories": {
    ...
    ...
    ...
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    ...
    ...
    ...
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "total_questions": 1
}
```
##### Adding Question
```bash
curl --location --request POST 'http://127.0.0.1:5000/questions' --header 'Content-Type: application/json' \
--data-raw '{
    "question": "What'\''s your name?",
    "answer": "Ahmed Magdy",
    "difficulty": 3,
    "category": 1
}'
```
```json
{
  "success": true
}
```
### DELETE /questions/<question_id>
Deletes the corresponding qusetion id from the database.
#### Arguments
Takes on argument and that's the question id 
#### Return
An object with a single key success, representing the status of the action.
#### Example
```bash
curl -x DELETE http://localhost:3000/questions/5
```
```json
{
  "success": true
}
```
