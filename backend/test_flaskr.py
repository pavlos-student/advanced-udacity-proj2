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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # sample question
        self.new_question = {
            'question': 'Q',
            'answer': 'A',
            'difficulty': '2',
            'category': '3'
        }

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Test GET /categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        # check if categories exist
        self.assertTrue(len(data['categories']))

    # Test GET /questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if questions exist & if their total number is set
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        
    # Test POST /questions 
    def test_create_question(self):
        # get number of questions before post
        questions_before_post = Question.query.all()

        # create a new question and load its response data
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        # get number of questions after post
        questions_after_post = Question.query.all()

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if one more question after post
        self.assertTrue(len(questions_after_post) - len(questions_before_post) == 1)

    # Test DELETE /questions/{id}
    def test_delete_question(self):
        question = Question(question="Q", answer='A', category=1, difficulty=1)
        question.insert()
        question_id = question.id
        print('question: ', question, ' question id: ', question_id)

        questions_before_delete = Question.query.all()

        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)
        print('response: ', response, ' data :', data)

        questions_after_delete = Question.query.all()
        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(len(questions_before_delete) - len(questions_after_delete) == 1)
        self.assertEqual(question, None)
    
    #  Test POST /questions/search
    def test_search_questions(self):
        # perform post request with search term 'searchTerm', load response data
        response = self.client().post('/questions/search', json={'searchTerm': 'taj'})
        data = json.loads(response.data)

        # check status code & success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()