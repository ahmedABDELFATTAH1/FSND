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

    def format_categories():
        categories = Category.query.all()
        categories_formated = {}
        categories_formated["categories"] = {}
        for category in categories:
            cate = category.format()
            categories_formated["categories"][str(cate["id"])] = cate["type"]

        return categories_formated

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def get_categories():

        categories_formated = format_categories()

        return jsonify(
            categories_formated
        )

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        all_questions = Question.query.all()
        page = int(request.args.get("page"))
        if page*10 > len(all_questions):
            abort(404)
        target_questions = all_questions[int(
            page)*10:min(len(all_questions), int(page)*10+10)]
        formated_questions = []
        for question in target_questions:
            formated_questions.append(question.format())
        print(formated_questions)
        categories_formated = format_categories()
        return jsonify({
            "questions": formated_questions,
            "totalQuestions": len(all_questions),
            "categories": categories_formated["categories"],
            "currentCategory": 'History'
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:id>', methods=["DELETE"])
    def delete_question(id):
        print(id)
        try:
            question = Question.query.filter_by(id=id).first()
            print(question)
            question.delete()
            return str(id), 200
        except:
            abort(404)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=["POST"])
    def add_question():
        question_data = request.get_json()
        print(question_data)
        if 'searchTerm' in question_data:
            search_term = question_data['searchTerm']
            print(search_term)
            questions = Question.query.all()
            questions_result = []
            for question in questions:
                question_formatted = question.format()
                if search_term.lower() in question_formatted['question'].lower():
                    questions_result.append(question_formatted)
            print(questions_result)
            result = {
                "questions": questions_result,
                "totalQuestions": len(questions_result),
                "currentCategory": 'Entertainment'
            }
            print(result)
            return jsonify(result)

        else:
          try:
            question_name = question_data['question']
            question_answer = question_data['answer']
            question_diff = question_data['difficulty']
            question_cate = question_data['category']
            question = Question(question_name, question_answer,
                                question_cate, question_diff)
            try:
                question.insert()
                return jsonify({"result": "success"}), 200
            except:
                return abort(404)
          except:
            abort(404)

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
    @app.route('/categories/<int:id>/questions')
    def categorie_questions(id):
        categorie_questions_list = Question.query.filter_by(
            category=id).all()

        print("hello")
        print(len(categorie_questions_list))
        if len(categorie_questions_list) == 0:                                        
          abort(422)
          
        print(categorie_questions_list)
        formatted_questions = []
        for question in categorie_questions_list:
            formatted_questions.append(question.format())

        categories = format_categories()
        print(categories)
        category_name = categories["categories"][str(id)]

        return jsonify({
            "questions": formatted_questions,
            "totalQuestions": len(categorie_questions_list),
            "currentCategory": category_name
        })

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

    @app.route('/quizzes', methods=["POST"])
    def play_quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category')['id']
        quiz_prev_questions = body.get('previous_questions', [])
        questions = None
        if quiz_category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category).all()
        print(questions)
        next_question = {}
        for question in questions:
            if question.id not in quiz_prev_questions:
                next_question = question.format()
        print(next_question)
        return jsonify({"question": next_question})

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unable_to_proccess(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unable to process the contained instructions"
        }), 422

    return app
