from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    cv_filename = data.get('cv_filename')
    prompt = data.get('prompt')
    country = data.get('country')

    # Example: Log the received data
    print(f"Received data - CV Filename: {cv_filename}, Prompt: {prompt}, Country: {country}")

    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(port=4000)