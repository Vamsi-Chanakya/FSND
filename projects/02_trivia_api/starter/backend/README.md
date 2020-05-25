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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

##REVIEW_COMMENT

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions'
POST 'questions/search'
GET '/categories/<ind: category_id>/questions'
POST '/quizzes'

##GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

##GET '/questions'

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, ...
    
  ], 
  "success": true, 
  "total_questions": 20
}

- Returns 404 on error, when no questions are available or invalid page param is provided
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

##DELETE '/questions/int:question_id'

- Delete a question with specified id
- Request Arguments: question_id, the id of the question to delete
- Returns success message on success

```bash
{
  "deleted": "12",
  "success": true
}
- Returns 422 on error
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}
```


##POST '/questions'

- Creates a new questiion
- Request Body: question to be created

```bash
curl -X POST -H "Content-Type: application/json" -d '
{"answer": "Vamsi Chanakya", "category": "4", "difficulty": "2", "question": "What is my full name ?"}
' http://127.0.0.1:5000/questions

- Returns: The newly created question. 

{
  "created": 25,
  "success": true
}

- Returns 422 on error, when bad format data is provided
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

##POST '/questions/search'

- Search a question
- Request Body: searchTerm
{"searchTerm": "search term"}
- Returns success message on success

```bash
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What is my full name"}' http://127.0.0.1:5000/questions/search
{
  "current_category": null,
  "questions": [
    {
      "answer": "Vamsi Chanakya",
      "category": 4,
      "difficulty": 2,
      "id": 25,
      "question": "What is my full name ?" 
    } 
  ],
  "success": true,
  "total_questions": 1
}
```


##GET '/categories/<ind: category_id>/questions'

- Get questions of specified category id
- Returns a list of questions od the specified category

```bash
{
  "current_category": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },....
    {
      "answer": "vamsi",
      "category": 5,
      "difficulty": 1,
      "id": 24,
      "question": "what is my name"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

##POST '/quizzes'

 - Fetches a question to play quiz
 - Request Body: 
    - previous_questions contains a list of ids for previously attempted questions
    - quiz_category contains the id of the question category for the quiz

```bash
curl -X POST -H "Content-Type: application/json" -d '
{"previous_questions": [],"quiz_category": {  "id": “1”}}
’ http://127.0.0.1:5000/quizzes

{
    "previous_questions": [],
    "quiz_category": {  "id": "1"}
}
- returns question to play quiz
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}

- Returns 422 on error
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

## Testing
To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```