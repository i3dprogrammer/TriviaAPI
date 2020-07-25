import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})


  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  
  @app.route('/categories', methods=['GET'])
  def categories():
    try:
      c = Category.query.all()
      r = {
        'categories': {}
      }
      for i in c:
        r['categories'][i.id] = i.type
      return jsonify(r)
    except:
      abort(422)

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  def searchQuestions(term, category=-1):
    try:
      if category != -1:
        qs = Question.query.filter(Question.question.ilike('%' + term.lower() +'%'), Question.category==category).all()
      else:
        qs = Question.query.filter(Question.question.ilike('%' + term.lower() +'%')).all()

      page = int(request.args.get('page', 1)) - 1
      cs = Category.query.all()
      r = {
        'questions': [],
        'total_questions': len(qs),
        'categories': {},
        'current_category': category
      }

      for i in cs:
        r['categories'][i.id] = i.type

      for i in qs[page*QUESTIONS_PER_PAGE:page*QUESTIONS_PER_PAGE+QUESTIONS_PER_PAGE]:
          r['questions'].append(i.format())

      return jsonify(r)

    except:
      abort(422)

  @app.route('/questions', methods=['GET'])
  def questions():
    try:
      return searchQuestions('')
    except:
      abort(500)

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def deleteQuestion(question_id):
    try:
      Question.query.get(question_id).delete()
      return jsonify({
        'success': True
      })
    except:
      abort(500)

  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions', methods=['POST'])
  def add_search_question():
    data = request.get_json()

    if 'searchTerm' in data:
      try:
        return searchQuestions(data['searchTerm'])
      except:
        abort(500)
      
    if 'question' not in data or 'answer' not in data or 'difficulty' not in data or 'category' not in data:
      abort(400)

    question = data['question']
    answer = data['answer']
    difficulty = data['difficulty']
    category = data['category']

    try:
      q = Question(question = question, answer=answer, difficulty=difficulty, category=category)
      q.insert()

      return jsonify({
        'success': True
      })
    except:
      abort(500)

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def questionsByCategory(cat_id):
    try:
      return searchQuestions('', cat_id)
    except:
      abort(500)

  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def quiz():
    data = request.get_json()

    if 'previous_questions' not in data or 'quiz_category' not in data:
      abort(400)

    previous = data['previous_questions']
    curr_cat = data['quiz_category']

    try:
      if curr_cat['id'] == 0:
        qs = Question.query.filter(Question.id.notin_(previous)).first()
      else:
        qs = Question.query.filter(Question.id.notin_(previous), Question.category==curr_cat['id']).first()

      if qs == None:
        return jsonify({})

      return jsonify({
        'question': qs.format()
      })
    except:
      abort(500)
    
  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(500)
  def interal_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Internal Server Error"
    }), 500

  return app

    