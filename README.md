# CN-Generator
 Masters Thesis Project

## Git Setup
1. Clone the repository:  
git clone https://github.com/yannir69/CN-Generator.git  
cd CN-Generator  

2. Create a virtual environment:
    python -m venv venv  
    venv\Scripts\activate           # Windows  

3. Install Dependencies (Make sure you have Python 3.8 or later installed):
    pip install -r requirements.txt 

## 🔐 API Key Setup

This app uses the Groq API to generate responses. To run it, you'll need a personal API key.

### Steps:

1. Go to https://console.groq.com and log in or sign up.  
2. Create an API key.
3. In the root folder of this project, copy the file `.env.example` to a new file called `.env`:  
    copy .env.example .env  
4. Open the new .env file and paste your API key:  
    GROQ_API_KEY=your_actual_key_here  
5. Start the app as usual:   
    python app.py  

The server will now run at http://localhost:5500  

Have fun!  

Created by Yannik Rohrschneider as part of a Master's Thesis at Freie Universität Berlin.  
