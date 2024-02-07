from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/get-example/<int:user_id>', methods=['GET'])
def get_example(user_id):
    # Access the path variable user_id
    # For example, you can use it to fetch user data from a database
    user_data = {
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    }

    # Access the request body (if it exists)
    request_data = request.json

    # Return a JSON response with user data and request body
    return jsonify({
        'user_data': user_data,
        'request_data': request_data
    })


if __name__ == '__main__':
    app.run(debug=True)
