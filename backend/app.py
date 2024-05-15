"""import openai

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
        print("Chatbot: ", response)"""

from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

model = Ollama(model = "llama3")

message = "all chinese people are ugly"

classifier = Agent(
    role = 'Hate Speech Detector',
    goal = 'Detect Hate speech',
    backstory = """You are a social media page moderator. You're responsible for answering to hate speech comments and mitigate the hate under your posts.""",
    verbose = True,
    allow_delegation = False,
    llm = model
)

responder = Agent(
    role = 'Counter-Narrative Generator',
    goal = 'Returning a good Counter-Narrative to Hate Speech that can be used to moderate an instagram page comment section',
    backstory = """You are a social media page moderator. You're responsible for answering to hate speech comments and mitigate the hate under your posts.""",
    verbose = True,
    allow_delegation = False,
    llm = model
)

classify_comment = Task(
    description = f"Classify the following message in hate speech or non-hate-speech: '{message}'",
    agent = classifier,
    expected_output = "A binary classification of hate speech or not"
)

generate_CN = Task(
    description = f"Generate a Counter-Narrative for the following hate speech message: '{message}'",
    agent = classifier,
    expected_output = "Counter-Narrative for hatespeech that is mitigating further hate speech comments"
)

crew = Crew(
    agents = [classifier, responder],
    tasks = [classify_comment, generate_CN],
    verbose = 2,
    process = Process.sequential
)

output = crew.kickoff()
print(output)



