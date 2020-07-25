# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Error Handling
All the end points could return an error as JSON object descriping what happened, the following is the JSON data returned

success: False.

error: The error code that occurred (400, 404, 405, 422, 500).

message: a simple message descriping what went wrong.

### Example
Since patch is not a method that we implement or allow.
```bash
curl --location --request PATCH 'http://127.0.0.1:5000/questions'
```
```json
{
  "error": 405,
  "message": "Method Not Allowed",
  "success": false
}
```

## Endpoints
### GET /categories
Fetches a list of all available categories.
#### Return
An object with a single key, categories, that contains a dictionary with the key value pair id and type.
#### Example
```bash
curl --request GET http://localhost:3000/categories
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
curl --request GET http://localhost:3000/questions
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
#### JSON Body
Should contain only ONE of the following.
##### 1. Searching Questions
searchTerm: the value to search the questions for.
##### 2. Adding Question
question: question title.
answer: the answer for the question.
diffculity: the difficulty of the question.
category: the category the question belongs to.
#### Return
##### 1. Searching Questions
If the body contained a searchTerm, returns the following

An object with the following keys [questions, total_questions, categories, current_category] 
questions: represents a list of questions that matches the search criteria (max 10)
total_questions: the count of all the questions that matches the search criteria
categories: all the available categories
current_category: the current searching category
##### 2. Adding Question
An object with a single key success, representing the status of the action.
#### Example
##### 1. Searching Questions
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
##### 2. Adding Question
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
Takes one argument and that's the question id 
#### Return
An object with a single key success, representing the status of the action.
#### Example
```bash
curl --request DELETE http://localhost:3000/questions/5
```
```json
{
  "success": true
}
```
### GET /categories/<category_id>/questions
Fetches all qusetions that belongs to that category id
#### Arguments
Takes only one argument, category_id
#### Return
An object with the following keys [questions, total_questions, current_category] 
questions: represents a list of all the available questions (max 10)
total_questions: holds the count of all available questions
current_category: the current searching category
#### Example
```bash
curl --request GET http://localhost:3000/categories/4/questions
```
```json
{
  "current_category": 4,
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
  "total_questions": 3
}
```
### POST /quizzes
Generates a new question that's not in the previous_questions list and in a certain category.
#### JSON Body
previous_questions: A list of questions ids that has been already processed, the new question id will not belong to this list.
quiz_category: An object with kvp (id, type) that represents the category that the question should belong to (id 0 = all categories)
#### Return
Returns a dictionary that contains a single key, questions, that has the following key value pairs
id: question id
question: the question itself.
answer: the answer to the question.
difficulty: the difficulty of the question.
category: the category the question belogns to.
#### Example
```bash
curl --location --request POST 'http://127.0.0.1:5000/quizzes' --header 'Content-Type: application/json' 
--data-raw '{
    "previous_questions": [],
    "quiz_category": {
        "id": 0,
        "type": "History"
    }
}'
```
```json
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }
}
```
