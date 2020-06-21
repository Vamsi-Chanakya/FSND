import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


db_drop_and_create_all()


# ROUTES
'''
implement endpoint
    GET /drinks
    this is a public endpoint and contain drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks or appropriate status code
    indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks_list = Drink.query.all()

    if len(drinks_list) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks_list]
    }), 200


'''
implement endpoint
    GET /drinks-detail
    require the 'get:drinks-detail' permission and
    contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks_list = Drink.query.all()

    if len(drinks_list) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks_list]
    }), 200


'''
implement endpoint
    POST /drinks
    create a new row in the drinks table
    require the 'post:drinks' permission and
    contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly
    created drink or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    body = request.get_json()

    if not ('title' in body and 'recipe' in body):
        abort(422)

    add_drink = body.get('title')
    add_recipe = body.get('recipe')

    try:
        drink = Drink(title=add_drink, recipe=json.dumps(add_recipe))
        drink.insert()

    except:
        abort(404)

    finally:
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200

        db.session.close()


'''
implement endpoint
    PATCH /drinks/<id> where <id> is the existing model id
    respond with a 404 error if <id> is not found
    update the corresponding row for <id>
    require the 'patch:drinks' permission and
    contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the
    updated drink or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    upd_drink = Drink.query.get(id)

    if upd_drink:
        try:
            body = request.get_json()
            print(body)

            title = body.get('title')
            recipe = body.get('recipe')

            if title:
                upd_drink.title = title
            if recipe:
                upd_drink.recipe = json.dumps(recipe)

            upd_drink.update()

            return jsonify({
                "success": True,
                "drinks": [upd_drink.long()]
            }), 200

        except:
            abort(422)
            db.session.rollback()

        finally:
            db.session.close()

    else:
        abort(404)


'''
implement endpoint
    DELETE /drinks/<id> where <id> is the existing model id
    respond with a 404 error if <id> is not found
    delete the corresponding row for <id>
    require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    del_drink = Drink.query.get(id)

    if del_drink:
        try:

            del_drink.delete()

        except:
            abort(422)

        finally:

            return jsonify({
                "success": True,
                "delete": id
            }), 200

            db.session.close()

    else:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
implement error handler for 404
error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
implement error handler for AuthError
error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error_handler(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        'message': error.error
    }), 401
