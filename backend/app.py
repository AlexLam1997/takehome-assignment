from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

from formatException import formatException

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

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

# Catch and handle all unexpected, unhandled errors
@app.errorhandler(Exception)
def handle_error(e):
    return create_response(status = 500, message=str(e))

# ---------------------- Part 2 ----------------------
@app.route("/shows/<int:id>", methods=['GET'])
def get_show(id):
    show = db.getById("shows", id)
    if show is None: 
        return create_response(status=404, message="No show with this id exists")
    return create_response({"result": show})

# ---------------------- Part 3 ----------------------
@app.route("/shows", methods= ['POST'])
def create_show():
    show = request.json
    try:
        # validate the input is correct
        validate_show(show)
        created_show = db.create("shows", show)
        return create_response(data = created_show, message="Show created")
    except formatException as formatException:
        return create_response(status = 422, message=str(formatException))

def validate_show(show):
    if "name" not in show: 
        raise formatException("Show name cannot be empty")
    if "episodes_seen" not in show: 
        raise formatException("Episode seen cannot be empty")

# ---------------------- Part 4 ----------------------
@app.route("/shows/<int:id>", methods = ['PUT'])
def update_show(id):
    update_request = request.json
    update_response = db.updateById("shows", id, update_request)
    if(update_response is None):
        return create_response(status=404, message="Show could not be updated: does not exist")
    return create_response(data=update_response, message="Show updated")

# ---------------------- Part 6 ----------------------

@app.route("/shows", methods=['GET'])
def get_all_shows():
    min_episodes_query = request.args.get("minEpisodes", -1 , int)
    shows = db.get("shows")
    # filter the list of shows 
    filtered_shows = list(filter(lambda show: show["episodes_seen"] >= min_episodes_query, shows))
    return create_response(data={"shows": filtered_shows}, message="Shows retrieved")


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
