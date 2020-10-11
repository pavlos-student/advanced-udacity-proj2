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
    
    # Test GET /categories/<int:id>/questions 
    def test_get_questions_by_categoryId(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test POST /quizzes
    def test_quiz(self):
        # set the test's request body
        quiz_request_body = {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1}}
        response = self.client().post('/quizzes', json=quiz_request_body)
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test 404 NOT FOUND for GET questions per page
    def test_404_get_questions(self):
        response = self.client().get('/questions?page=5000')
        data = json.loads(response.data)

        # check status code & false success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test 422 unprocessable for creating a question - POST question 
    def test_422_create_question(self):
        # get all questions before creating a new question
        questions_before_create_question = Question.query.all()

        # create an empty question - empty json body
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        # get all questions after creating a new question
        questions_after_create_question = Question.query.all()

        # check status code & false success message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

        # compare both questions varriables, if they are equal then the new post questions was created wrongly
        self.assertTrue(len(questions_before_create_question) == len(questions_after_create_question))

    # Test 404 NOT FOUND for GET questions by category
    def test_404_get_questions_by_category(self):
        # send a wrong category
        response = self.client().get('/categories/z/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    # Test 422 Unprocessable for playing the quiz
    def test_422_play_quiz(self):
        # send an empty request body json
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # check status code & false success message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()