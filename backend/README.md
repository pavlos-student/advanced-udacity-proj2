# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt

pip3 install psycopg2-binary
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


## API Reference

### Getting Started
Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
which is stated here as localhost:5000

### Error Handling
- General: four status codes
  - 404: Not found
  - 422: unprocessable
  - 400: bad request
  - 500: internal server error

### Endpoints

#### GET /categories

- General: returns all categories in the database
- Sample URI Request: ``` curl http://127.0.0.1:5000/categories ```

- Sample Response:

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

#### GET /questions

- General: 
  - returns all questoins in the database
  - questions are paginated in groups of 10 questions per page
  - it returns a list of the available categories and the total number of available questions
- Sample URI Request: ``` curl http://127.0.0.1:5000/questions ```

- Sample Response:

```
{
  "categories": "Selected all Categories", 
  "current_category": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "A2", 
      "category": 1, 
      "difficulty": 5, 
      "id": 25, 
      "question": "Q2"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "A1", 
      "category": 2, 
      "difficulty": 3, 
      "id": 24, 
      "question": "Q1"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```

#### POST /questions

- General: 
  - creates a new question as per the users' inputs: question, answer, difficulty, and category.
  - returns a sample JSON with the object's id & a success value

- Sample URI request: 
``` curl -d '{"question":"Q3", "answer":"A3", "category": 3, "difficulty": 3}' -H "Content-Type: application/json" -X POST localhost:5000/questions ```

- Sample Response:
```
{
  "question": {
    "answer": "A3", 
    "category": 3, 
    "difficulty": 3, 
    "id": 26, 
    "question": "Q3"
  }, 
  "success": true
}
```

#### DELETE /questions/int:id

- General:
  - Delete a question by its id (passed as a query parameter)
  - Returns id of successful deleted question

- Sample URI request:
```curl -X DELETE localhost:5000/questions/31```

- Sample Response:
```
{
  "deleted": 31, 
  "success": true
}
```

#### POST /questions/search

- General:
  - searches for questions with the keyword that the user's input
  - returns paginated questions

- Sample URI Request:
```curl -d '{"searchTerm":"Taj"}' -H "Content-Type: application/json" -X POST localhost:5000/questions/search```

- Sample Response:
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

#### GET /categories/int:id/questions

- General:
  - get all questions by category id, passed as the URI parameter
  - return paginated questions in a JSON object with its info (as in the sample response below)

- Sample URI request:
``` curl localhost:5000/categories/3/questions ```

- Sample Response:
```
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "A3", 
      "category": 3, 
      "difficulty": 3, 
      "id": 35, 
      "question": "Q3"
    }
  ], 
  "success": true, 
  "total_questions": 22
```

#### POST /quizzes

- General:
  - user plays a game answering random questions
  - uses the user's chosen category & previous question
  - retruns a random, unseen, question info to be rendered to the user

- Sample URI Request:
```curl -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}' -H "Content-Type: application/json" -X POST localhost:5000/quizzes ```

- Sample Response:
```
{
  "question": {
    "answer": "A1", 
    "category": 1, 
    "difficulty": 1, 
    "id": 33, 
    "question": "Q1"
  }, 
  "success": true
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```