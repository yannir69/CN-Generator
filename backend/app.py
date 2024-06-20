#from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from flask import Flask, render_template, request, send_from_directory, jsonify
import os

os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
os.environ["OPENAI_MODEL_NAME"] = 'mixtral-8x7b-32768'
os.environ["OPENAI_API_KEY"] = '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'

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generateCN', methods=['POST'])
def generate():
    message = request.json

    agent_profi = Agent(
        role = 'Moderator eines Accounts auf einer Social Media Plattform',
        goal = 'Generator von Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern.',
        backstory = 'Dein Kommentarstil ist professionell, sachlich, und auf Fakten basiert',
        verbose = True,
        allow_delegation = False,
        language = 'de',
    )

    agent_humor = Agent(
        role = 'Moderator eines Accounts auf einer Social Media Plattform',
        goal = 'Generator von Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern',
        backstory = 'Dein Kommentarstil ist humorvoll, kreativ und schlagfertig. Benutze Emojis um den Humor hervorzuheben',
        verbose = True,
        allow_delegation = False,
        language = 'de'
    )

    agent_affection = Agent(
        role = 'Moderator eines Accounts auf einer Social Media Plattform',
        goal = 'Generator von Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern',
        backstory = 'Dein Kommentarstil ist einfühlsam und sensibel. Versuche die Ansichtsweise des Hassredners anzuerkennen, aber freundlich zu widerlegen',
        verbose = True,
        allow_delegation = False,
        language = 'de'
    )

    agent_problem = Agent(
        role = 'Hassrede-Analytiker',
        goal = 'Analysiere Hasskommentare und schreibe einen Paragraph, warum diese Hassrede problematisch ist',
        backstory = 'Du bist ein Experte in Hassrede und kannst Problematiken von Hassrede-Kommentaren erkennen und beschreiben.',
        verbose = True,
        allow_delegation = False,
        language = 'de'
    )

    task_problem = Task(
        description = f"Finde die Problematik der folgenden Hassrede. Schreibe eine ausführliche Erklärung, warum dies als Hassrede gilt '{message}'",
        agent = agent_problem,
        expected_output = "Ein Paragraph mit einer Erklärung, warum der Kommentar problematisch hinsichtlich Hassrede ist.",
        language = 'de',
        async_execution = True
    )

    task_profi = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_profi,
        expected_output = "Ein bis drei Sätze Gegenrede, die die weitere Hassrede in der Kommentarspalte vermindern wird",
        language = 'de',
        async_execution = True,
        context = [task_problem]
    )

    task_humor = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_humor,
        expected_output = "Ein bis drei Sätze Gegenrede, die die weitere Hassrede in der Kommentarspalte vermindern wird",
        language = 'de',
        async_execution = True,
        context = [task_problem]
    )

    task_affection = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_affection,
        expected_output = "Ein bis drei Sätze Gegenrede, die die weitere Hassrede in der Kommentarspalte vermindern wird",
        language = 'de',
        async_execution = True,
        context = [task_problem]
    )

   
    crew = Crew(
        agents = [agent_profi, agent_affection, agent_humor, agent_problem],
        tasks = [task_profi, task_affection, task_humor, task_problem],
        verbose = 2,
        temperature = 0.6,
        process = Process.sequential
    )
    output = crew.kickoff()
    return output

if __name__ == '__main__':
    app.run(debug=True, port=5500)




