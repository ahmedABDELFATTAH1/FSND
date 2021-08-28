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
        self.database_path = 'postgresql://postgres:12@localhost:5432/trivia'
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

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(True, 'categories' in data)
        self.assertEqual(res.status_code, 200)

    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(True, 'questions' in data)
        self.assertEqual(res.status_code, 200)

    def test_get_questions_page_exxedded(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_categories_questions_success(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(True, 'questions' in data)
        self.assertEqual(res.status_code, 200)

    def test_categories_questions_success(self):
        res = self.client().get('/categories/120/questions')
        data = json.loads(res.data)
        # print(res)
        self.assertEqual(False, data['success'])
        self.assertEqual(res.status_code, 422)
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_delete_question_success(self):
        res = self.client().delete('/questions/4')
        self.assertEqual(res.status_code, 200)

    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/5000')
        self.assertEqual(res.status_code, 404)

    def test_add_question_success(self):
        res = self.client().post('/questions', json={
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        })
        self.assertEqual(res.status_code, 200)

    def test_add_question_fail(self):
        res = self.client().post('/questions', json={
            'question':  'Heres a new question string',
            'difficulty': 1,
            'category': 3,
        })
        self.assertEqual(res.status_code, 404)

    def test_search_question(self):
        res = self.client().post('/questions', json={
            'searchTerm':  'mahal'
        })

        data = json.loads(res.data)
        self.assertGreaterEqual(data['totalQuestions'], 0)
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
