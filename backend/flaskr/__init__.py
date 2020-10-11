import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def questions_pagination(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  question_collection = [question.format() for question in questions]
  current_questions = question_collection[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  # Set up CORS. Allow '*' for origins
  CORS(app, resources={'/': {'origins': '*'}})

  # Using the after_request decorator to set Access-Control-Allow in the response headers for CORS
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

    return response

  # endpoint to handle GET requests for all available categories
  @app.route('/categories')
  def get_categories():
    # get all categories ordered by category Id
    categories = Category.query.order_by(Category.id).all()

    # if there was no available categories then return 404 'not found'
    if len(categories) == 0:
      abort(404)

    # format the data to return to the FE 'id' & 'type'
    categories_to_render = {category.id: category.type for category in categories}

    # return JSON object with 'Key' names typical to the ones in the Front-end (to be rendered)
    return jsonify ({
      'success': True,
      'categories': categories_to_render,
      'total_categories': len(Category.query.all())
    })
  
  '''
  endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  This endpoint returns a list of questions, number of total questions, current category, categories.
  '''
  @app.route('/questions')
  def get_questions():

    # get all quesitons and paginate them
    questions_collection = Question.query.order_by(Question.category).all()
    current_questions = questions_pagination(request, questions_collection)

    # throw an error if there's no quesitons
    if len(current_questions) == 0:
      abort(404)
    
    # get all categories and add to a dict (category_types)
    category_collection = Category.query.order_by(Category.id).all()
    category_types = {}

    for item in category_collection:
      category_types[item.id] = item.type

    # return JSON object with 'Key' names typical to the ones in the Front-end (to be rendered)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': 'Selected all Categories',
      'current_category': category_types
    })

  
  # an endpoint to DELETE question using a question ID
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_quesiton(question_id):
    try:
      # retrieve the question from db by id, get only one result
      question = Question.query.filter_by(id=question_id).one_or_none()
      
      # throw exception NOT_FOUND if the id doesn't exist
      if question_id is None:
        abort(404)
      
      question.delete()

      # return the id of the question deleted &  msg stating that it was successfully deleted
      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      # abort, if a problem occurred while deleting the question
      abort(422)


  # an endpoint to POST a new question, requires the question and answer text, category, and difficulty score.
  @app.route('/questions', methods=['POST'])
  def create_question():
    # get JSON from FE user inputs request
    body = request.get_json()

    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)

    # collecting the data from the JSON body (user inputs)
    question = body.get('question')
    answer = body.get('answer')
    category = body.get('category')
    difficulty = body.get('difficulty')
    # search = body.get('searchTerm')

    # TODO: include a condition related to the search functionality

    # if any of the user data is missing then throw a bad request exception
    if not question or not answer or not category or not difficulty:
      abort(400)

    try:
      # construct question from the Question Model using the FE user inputs
      question = Question(question=question, answer=answer, difficulty=difficulty, category=category)

      # insert: add & commit data to the db
      question.insert()

      # return JSON object with 'Key' names typical to the ones in the Front-end (to be rendered)
      return jsonify({
        'success': True,
        'question': question.format()
      })
    except:
      # throw an unprocessable entity exception
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    