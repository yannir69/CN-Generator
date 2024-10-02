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

    agent_problem = Agent(
        role = 'Hassrede-Analytiker',
        goal = 'Analysiere Hasskommentare und schreibe einen Paragraph, warum diese Hassrede problematisch ist. Hassrede wird wie folgt definiert: Hassrede meint abwertende und menschenverachtende Sprache und Inhalte. Zum Beispiel in Form von rassistischen oder sexistischen Beleidigungen, manchmal auch verbunden mit Anstiftung zur Gewalt gegen Minderheiten. Hassrede ist kein juristischer Begriff und nicht in allen Fällen strafbar. Verwende ausschließlich die deutsche Sprache für die Antwort.',
        backstory = 'Du bist ein Experte in Hassrede und kannst Problematiken von Hassrede-Kommentaren erkennen und beschreiben. Deine Antworten sollen immer auf Deutsch sein.',
        verbose = True,
        #allow_delegation = False,
        language = 'de'
    )

    agent_profi = Agent(
        role = 'Formeller Gegenredner',
        goal = 'Generator von deutschen Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern. Verwende ausschließlich die deutsche Sprache für die Antwort.',
        backstory = 'Du bist ein Moderator einer Social Media Platform. Dein Kommentarstil ist professionell, sachlich, und auf Fakten basiert. Deine Antworten sollen immer auf Deutsch sein.',
        verbose = True,
        #allow_delegation = False,
        language = 'de'
    )

    agent_humor = Agent(
        role = 'Humorvoller Gegenredner',
        goal = 'Generator von deutschen Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern. Verwende ausschließlich die deutsche Sprache für die Antwort.',
        backstory = 'Du bist ein Moderator einer Social Media Platform. Dein Kommentarstil ist humorvoll, kreativ und schlagfertig. Benutze Emojis um den Humor hervorzuheben. Deine Antworten sollen immer auf Deutsch sein.',
        verbose = True,
        #allow_delegation = False,
        language = 'de'
    )

    agent_affection = Agent(
        role = 'Einfühlsamer Gegenredner',
        goal = 'Generator von deutschen Antworten auf gegebene Hasskommentare, um weitere Hassrede in der Kommentarspalte zu verringern. Verwende ausschließlich die deutsche Sprache für die Antwort.',
        backstory = 'Du bist ein Moderator einer Social Media Platform. Dein Kommentarstil ist einfühlsam und sensibel. Versuche die Ansichtsweise des Hassredners anzuerkennen, aber freundlich zu widerlegen. Deine Antworten sollen immer auf Deutsch sein.',
        verbose = True,
        #allow_delegation = False,
        language = 'de'
    )

    agent_evaluator = Agent(
        role = 'Experte in Gegenrede auf Hassrede',
        goal = 'Evaluation der Gegenrede von jedem Agenten in 1 bis 5 Sternen. Verwende ausschließlich die deutsche Sprache für die Antwort.',
        backstory = 'Hier ist die Definition der einzelnen Sterne von 1 bis 5: 1 Stern: Die Antwort auf die Gegenrede hat wenig bis gar keine Verbindung oder Relevanz zu dem Hassrede-Beispiel. Die Antwort kann ein völlig anderes Thema ansprechen oder den Kontext der Hassrede nicht angemessen berücksichtigen. 2 Sterne: Die Antwort auf die Gegenerzählung hat eine gewisse Verbindung oder Relevanz für das Beispiel der Hassrede, aber die Verbindung ist schwach. Die Antwort berührt vielleicht bestimmte Aspekte der Hassrede, aber es fehlt eine starke kontextuelle oder semantische Ähnlichkeit. 3 Sterne: Die Antwort auf die Gegenrede zeigt ein angemessenes Maß an Verbindung oder Relevanz zu dem Beispiel der Hassrede. Die Antwort geht bis zu einem gewissen Grad auf den Kontext der Hassrede ein, aber es kann immer noch Bereiche geben, in denen die semantische oder kontextuelle Ähnlichkeit nicht vollständig hergestellt ist. 4 Sterne: Die Antwort der Gegenerzählung zeigt eine starke Verbindung oder Relevanz zu dem Beispiel der Hassrede. Die Antwort zeigt ein gutes Verständnis des Kontextes und geht effektiv auf die semantischen und kontextuellen Ähnlichkeiten ein. Es könnte jedoch noch kleinere Bereiche geben, in denen eine weitere Verbesserung möglich ist. 5 Sterne: Die Antwort auf die Gegenerzählung ist in hohem Maße mit dem Beispiel der Hassrede verbunden und relevant. Die Antwort geht umfassend auf die semantischen und kontextuellen Ähnlichkeiten mit Präzision und Genauigkeit ein. Sie zeigt ein tiefes Verständnis für den Kontext der Hassrede und präsentiert effektiv eine Gegenperspektive. Deine Antworten sollen immer auf Deutsch sein.' ,
        verbose = True,
        #allow_delegation = False,
        language = 'de'
    )
    

    task_problem = Task(
        description = f"Finde die Problematik der folgenden Hassrede. Schreibe eine ausführliche deutsche Erklärung, warum dies als Hassrede gilt '{message}'",
        agent = agent_problem,
        expected_output = "Ein Paragraph in deutscher Sprache mit einer Erklärung, warum der Kommentar problematisch hinsichtlich Hassrede ist. Verwende ausschließlich die deutsche Sprache für die Antwort.",
        language = 'de'
    )

    task_profi = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_profi,
        expected_output = "Ein bis drei Sätze Gegenrede in deutscher Sprache, die die weitere Hassrede in der Kommentarspalte vermindern wird. Verwende ausschließlich die deutsche Sprache für die Antwort.",
        language = 'de'
    )

    task_humor = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_humor,
        expected_output = "Ein bis drei Sätze Gegenrede, die die weitere Hassrede in der Kommentarspalte vermindern wird. Verwende ausschließlich die deutsche Sprache für die Antwort.",
        language = 'de'
    )

    task_affection = Task(
        description = f"Generiere Gegenrede auf die gegebene Hassrede für die folgende Nachricht: '{message}'",
        agent = agent_affection,
        expected_output = "Ein bis drei Sätze Gegenrede, die die weitere Hassrede in der Kommentarspalte vermindern wird. Verwende ausschließlich die deutsche Sprache für die Antwort.",
        language = 'de'
    )

    task_evaluation = Task(
        description = f"Bewerte die generierte Gegenrede einzeln für den Profi-Agenten, Affection-Agenten und Humor-Agenten in deiner Crew im Hinblick auf die semantische Ähnlichkeit mit einem bis fünf Sternen und gib eine Rechtfertigung für die erreichte Punktzahl. Beachte, dass die semantische Ähnlichkeit die Assoziation zwischen der Antwort und dem Hassrede-Beispiel auf der Grundlage kontextueller oder semantischer Ähnlichkeit misst.",
        agent = agent_evaluator,
        expected_output = 'Bewertung in 1 bis 5 Sternen mit einer deutschen Erklärung der Ergebnisse anhand der Definition der Sterne. Die Bewertungen müssen auf Deutsch sein.',
        language = 'de',
        context = [task_profi, task_affection, task_humor, task_profi]
    )

    """task_refine = Task(
        description = f"Teile deiner Crew deine Evaluation mit und bringe den formellen Gegenredner, humorvollen Gegenredner und einfühlsamen Gegenreder unter Berücksichtigung deines Feedbacks ein neues Gegenrede-Statement zu generieren.",
        expected_output = "Formelle, humorvolle und einfühlsame Gegenredestatements, die unter Berücksichtigung der Evaluation generiert wurden.",
        agent = agent_evaluator,
        language = "de",
        context = [task_evaluation]
    )"""

    problem_output = task_problem.execute()
    profi_output = task_profi.execute(context=[problem_output])
    humor_output = task_humor.execute(context=[problem_output])
    affection_output = task_affection.execute(context=[problem_output])
    evaluation_output = task_evaluation.execute(context = [profi_output, humor_output, affection_output])
    
    """
    Wenn ich eine Crew möchte, die die Gegenrede verbessert
    crew = Crew(
        agents = [agent_evaluator, agent_profi, agent_humor, agent_affection],
        tasks = [task_refine, task_evaluation],
        verbose = 2,
        temperature = 0.6,
        language = 'de',
        process = Process.sequential,
        full_output = True 
    )
    

    crew_output = crew.kickoff()"""

    outputs = {
        "problem_output": problem_output,
        "profi_output": profi_output,
        "humor_output": humor_output,
        "affection_output": affection_output,
        "evaluation_output": evaluation_output
    }

    return jsonify(outputs)
    

if __name__ == '__main__':
    app.run(debug=True, port=5500)




