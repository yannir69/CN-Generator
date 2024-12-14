import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from docx import Document
import requests
from groq import Groq
from flask import Flask, render_template, request, send_from_directory, jsonify

# Initialize the embedding model
embedding_model = SentenceTransformer('all-mpnet-base-v2')
groq_api_url = "https://api.groq.com/openai/v1/models"  # Replace with actual Groq API endpoint
model = "mixtral-8x7b-32768"
os.environ["GROQ_API_KEY"] = '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'

# these are the different strategy documents
categories = {
    0: "Altersdiskriminierung u. Adultismus.docx",
    1: "Andeutung_Dog Whistle.docx",
    2: "Antimuslimischer Rassismus.docx",
    3: "Antisemitismus.docx",
    4: "Diskriminierung aufgrund von Geschlecht und sexueller Orientierung.docx",
    5: "Diskriminierung von Menschen mit Behinderung und chronischer Erkrankung.docx",
    6: "Feindschaft gegen Obdachlose.docx",
    7: "Gewichtsdiskriminierung.docx",
    8: "Ich hab ja nichts gegen, aber.docx",
    9: "Klassismus.docx",
    10: "Personalisierte Lüge.docx",
    11: "Provokation.docx",
    12: "Pseudowissenschaft.docx",
    13: "Rassismus.docx",
    14: "Whataboutism.docx",
}

docstore = {}

app = Flask(__name__)

@app.route('/CN')
def CN():
    return render_template('CN.html')

@app.route('/hateInput')
def hate_input():
    return render_template('hateInput.html')

@app.route('/')
def index():
    return render_template('index.html')

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY"),
)

# Function to call the Groq-hosted LLM
def get_llm_answer(query, document, hate_message, wordLimit):
    # Send the query and retrieved document texts to the LLM hosted by Groq
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Dies ist der Kommentar: " + hate_message + ". " + query + ". ",
        },
        {
            "role": "system",
            "content": "Antworte ausschließlich auf Deutsch und schreibe ungefähr " +  wordLimit + "Wörter. Nutze den folgenden Text als Quelle deiner Information " + document,
        }
    ],
    model=model,
    temperature=0.2,
    
    )
    return chat_completion.choices[0].message.content

# Extract text from DOCX documents
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

# Embed any text using the Sentence Transformer model
def embed_text(text, embedding_model):
    embedding = embedding_model.encode([text], convert_to_tensor=True)
    return embedding.cpu().numpy()  # Convert tensor to numpy array

# Add document embeddings to a FAISS index
def add_doc_to_faiss_index(doc_path, index, embedding_model):
    # Initialize FAISS index (L2 distance)
    
    text = extract_text_from_docx(doc_path)
    paragraphs = text.split('\n')
    valid_index = 0

    #split text into paragraphs and embed them individually
    for i, para in enumerate(paragraphs):
        if para.strip():  # Skip empty lines
            embedding = embed_text(para, embedding_model)
            index.add(embedding)
            docstore[valid_index] = para  # Store paragraph with index as key
            print(f"Added to docstore: Key {valid_index} -> {para[:100]}...")
            valid_index += 1

    return paragraphs

# Search FAISS index for the nearest documents
def search_documents(query, index, embedding_model, top_k=5):
    query_embedding = embed_text(query, embedding_model)
    _, indices = index.search(query_embedding, top_k)  # Search top K nearest docs
    print("FAISS indices: ", indices.flatten())
    print("Docstore: ", docstore.keys())
    return indices

# Get the paragraphs that have been stored in the docstore
def get_retrieved_texts(indices, docstore):
    print("Docstore: ", docstore.keys())
    retrieved_texts = [docstore[int(i)] for i in indices.flatten()]
    return " ".join(retrieved_texts)



#Suchhilfe is a document that helps categorizing a hate speech comment to choose the right document for strategy help
doc_path_Suchhilfe = "D:\Documents\FU Berlin\Masterarbeit\Civic.Net\Datensätze\Pre-Processed Manuskripte\Suchhilfe.docx"

#This document is just general counterspeech help. I haven't used this yet
doc_path_Counterspeech = "D:/Documents/FU Berlin/Masterarbeit/Civic.Net/Datensätze/Manuskripte/Tips_Counterspeech.docx"


@app.route('/generateCN', methods=['POST'])
def generate():
    print("I am here")
    receivedData = request.get_json()
    message = receivedData.get('text')
    wordLimit = receivedData.get('wordLimit')

    print(type(wordLimit), "value: ", wordLimit)

    d = 768  # Embedding dimension for the 'paraphrase-MiniLM-L6-v2' model
    faiss_index = faiss.IndexFlatL2(d)
    docstore.clear()

    # Add document to the FAISS index
    add_doc_to_faiss_index(doc_path_Suchhilfe, faiss_index, embedding_model)

    # Query for categorizing the comment in Suchhilfe.docx
    query_Category = "Finde den Paragraphen, der die Kernaussage und den Stil dieses Hasskommentars am besten beschreibt. Achte auf die inhaltlichen Merkmale und die Formulierungen des Kommentars, um die richtige Kategorie zu identifizieren. Kommentar: " + message
    #path for the strategy document
    docpath_strategy = "D:\Documents\FU Berlin\Masterarbeit\Civic.Net\Datensätze\Pre-Processed Manuskripte\\" + categories[int(search_documents(query_Category, faiss_index, embedding_model, 1))]
    #debug
    #print(categories[int(search_documents(query_Category, faiss_index, embedding_model, 5))])

    #now, embed the strategy document
    query_strategy = "Finde Informationen, die bei der Generierung von Gegenrede auf Hasskommentare helfen können"

    query_base = (
    """
        Anweisung: Generiere eine Gegenrede zu dem gegebenen problematischen Kommentar. Orientiere dich dabei an den Strategien im eingebundenen Dokument zur Gegenrede.

        Schreibe ohne: Begrüßungen, Verabschiedungen, allgemeine Appelle zum Miteinander, zusammenfassende Hinweise oder abschließende Phrasen.
        Vermeide: das Wort "Hassrede", Aufforderungen zur Zusammenarbeit (z. B. "Lass uns...", "Wir sollten...") und Formulierungen wie "Es ist wichtig zu verstehen, ...".
        Beende die Antwort unmittelbar nach der Richtigstellung oder Klärung des Problems.
    """
    )

    queryCN_formal = (
    """
        Du bist ein formeller Moderator in einem Online-Forum. Verzichte auf Emotionen und konzentriere dich darauf, den Kommentar zu deeskalieren, klarzustellen, was problematisch ist, und dabei höflich zu bleiben. Achte auf präzise und korrekte Sprache.
    """
    )

    queryCN_humor = (
    """
        Du bist ein humorvoller Moderator in einem Online-Forum. Antworte mit Humor und bleibe freundlich. Nutze Smileys und Emojis um deinen Stil zu unterstützen.
    """
    )

    queryCN_konfrontativ = (
    """
       Du bist ein konfrontativer Moderator in einem Online-Forum. Stelle unbedingt Gegenfragen und antworte kritisch dem Verfassers des Kommentars gegenüber.
    """
    )

    queryCN_einfühlsam = (
    """
        Du bist ein einfühlsamer in einem Online-Forum. Gehe verständnisvoll und respektvoll auf die zugrunde liegenden Emotionen oder Meinungen ein und versuche, eine Brücke zu bauen. Sei freundlich und deeskalierend, während du gleichzeitig verdeutlichst, warum der Kommentar problematisch ist.
    """
    )


    query_problem = "Schreibe ausschließlich auf Deutsch. Beschreibe das Problem des Hasskommentars ausführlich basierend auf den Informationen des Dokuments. "

    #clear the docstore and faiss index that is still filled with categories
    docstore.clear()
    faiss_index.reset()
    add_doc_to_faiss_index(docpath_strategy, faiss_index, embedding_model)
    document_text_strategy = get_retrieved_texts(search_documents(query_strategy, faiss_index, embedding_model, 5), docstore)

    print(message)
    CN_formell = get_llm_answer(queryCN_formal + "\n" + query_base, document_text_strategy, message, wordLimit)
    CN_humor = get_llm_answer(queryCN_humor + "\n" + query_base, document_text_strategy, message, wordLimit)
    CN_konfrontativ = get_llm_answer(queryCN_konfrontativ + "\n" + query_base, document_text_strategy, message, wordLimit)
    CN_einfühlsam = get_llm_answer(queryCN_einfühlsam + "\n" + query_base, document_text_strategy, message, wordLimit)
    problem = get_llm_answer(query_problem, document_text_strategy, message, '500')

    outputs = {
        "CN_formell": CN_formell,
        "CN_humor" : CN_humor,
        "CN_konfrontativ": CN_konfrontativ,
        "CN_einfühlsam": CN_einfühlsam,
        "problem" : problem
    }
    return jsonify(outputs)

if __name__ == '__main__':
    app.run(debug=True, port=5500)

