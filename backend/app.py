from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})

@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/restaurants", methods=['GET'])
def get_all_restaurants():
    restaurants = db.get('restaurants')
    minRating = request.args.get('minRating')
    filtered_restaurants = []

    if minRating is None:
        return create_response({"restaurants": restaurants})

    # If this is not an int then return an error
    try:
        minRating = int(minRating)
    except Exception as e:
        # We can flash exception e here using Flask built in 
        return create_response(status=404, message="minRating parameter is not an integer")

    for restaurant in restaurants:
        if restaurant['rating'] >= minRating:
            filtered_restaurants.append(restaurant)
    
    return create_response({"restaurants": filtered_restaurants})

@app.route("/restaurants", methods=['POST'])
def add_restaurant():
    # To check if there are even any name/rating
    try:
        name = request.form['name']
        rating = request.form['rating']
    except Exception as e:
        return create_response(status=422, message="Missing parameters name or rating")
    
    # Assumption that we are only rating with integers
    try:
        rating = int(rating)
    except Exception as e:
        return create_response(status=422, message="Rating is not an integer")

    if rating < 0 or rating > 10:
        return create_response(status=422, message="Rating is not between 0 and 10")

    payload = {'name': name, 'rating': rating}
    # new restaurant might not be needed but it is clearer than payload
    new_restaurant = db.create('restaurants', payload)
    return create_response({'restaurant': new_restaurant}, status=201)

@app.route("/restaurants/<id>", methods=['DELETE'])
def delete_restaurant(id):
    if db.getById('restaurants', int(id)) is None:
        return create_response(status=404, message="No restaurant with this id exists")
    db.deleteById('restaurants', int(id))
    return create_response(message="Restaurant deleted")

@app.route("/restaurants/<id>", methods=['GET'])
def get_restaurant(id):
    try:
        restaurant = db.getById('restaurants', int(id))
    except Exception as e:
        return create_response(status=422, message="Id is not an integer")

    if restaurant is None:
        return create_response(status=404, message="No restaurant with this id exists")
    return create_response({"restaurant": restaurant})

@app.route("/restaurants/<id>", methods=['PUT'])
def change_restaurant(id):
    try:
        name = request.form['name']
        rating = request.form['rating']
    except Exception as e:
        return create_response(status=422, message="Missing parameters name or rating")
    
    # Assumption that we are only rating with integers
    # Also we could try to modularize this since it is the same in add_restaurant
    try:
        id = int(id)
        rating = int(rating)
    except Exception as e:
        return create_response(status=422, message="Rating or Id is not an integer")

    if rating < 0 or rating > 10:
        return create_response(status=422, message="Rating is not between 0 and 10")
    
    payload = {'name': name, 'rating': rating}
    restaurant = db.updateById('restaurants', id, payload)

    if restaurant is None:
        return create_response(status=404, message="No restaurant with this id exists")
    return create_response({"restaurant": restaurant})

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
