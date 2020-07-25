import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Categories 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_405_post_categories(self):
        res = self.client().post('/categories', json = {})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)

    # Questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        qs_count = len(Question.query.all())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], qs_count)
        self.assertEqual(len(data['categories']), 6)

    def test_500_get_questions_wrong_page(self):
        res = self.client().get('/questions', query_string={'page': 'asd'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)

    def test_post_questions_search(self):
        res = self.client().post('/questions', json={'searchTerm': 'Whose'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)

    def test_post_questions_search_empty(self):
        res = self.client().post('/questions', json={'searchTerm': 'plumberjack'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_post_questions_add_new(self):
        qs_old = len(Question.query.all())

        res = self.client().post('/questions', json={'question': "What's your name?", "answer": "Ahmed Magdy", "difficulty": 5, "category": 2})
        data = json.loads(res.data)

        qs_new = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(qs_new, qs_old+1)

    def test_400_post_questions_add_new(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_delete_question(self):
        qs_old = len(Question.query.all())

        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        qs_new = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(qs_new, qs_old-1)
        
    def test_search_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['current_category'], 1)

    def test_quiz_get_question(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"id": 0, "type": None}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
    
    def test_quiz_get_different_from_previous_question(self):
        res = self.client().post('/quizzes', json={"previous_questions": [5], "quiz_category": {"id": 0, "type": None}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertNotEqual(data["question"]["id"], 5)

    def test_400_quizzes(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_500_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions": [5], "quiz_category": {"id": "asd", "type": None}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()