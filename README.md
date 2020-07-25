# TriviaAPI
TriviaAPI

### GET /categories
Fetches a list of all available categories.
#### Return
An object with a single key, categories, that contains a dictionary with the key value pair id and type.
#### Example
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
#### e.g.
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
