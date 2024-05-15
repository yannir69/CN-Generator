import openai

# Set your OpenAI API key
OPENAI_API_KEY = 'sk-proj-xksa4YXhxn1XqzX0OOTKT3BlbkFJN4kdtt5lIkziFbOuE1oS'
openai.api_key = OPENAI_API_KEY

# Route to handle incoming text input and generate response
def generate_response(input):
    response = openai.chat.completions.create(
            model = "text-davinci-002",
            messages=[{"role": "user", "content": input}],
        )
    generated_text = response.choices[0].message.content.strip()
    return generated_text

if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit"]:
            break

        response = generate_response(user_input)
        print("Chatbot: ", response)