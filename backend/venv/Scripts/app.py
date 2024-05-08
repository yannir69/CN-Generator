from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
OPENAI_API_KEY = 'sk-proj-xksa4YXhxn1XqzX0OOTKT3BlbkFJN4kdtt5lIkziFbOuE1oS'
openai.api_key = OPENAI_API_KEY

# Route to handle incoming text input and generate response
@app.route('/generate', methods=['POST'])
def generate_response():
    input_text = request.json.get('text')
    if not input_text:
        return jsonify({'error': 'Input text is missing'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=50
        )
        generated_text = response.choices[0].text.strip()
        return jsonify({'generated_text': generated_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)