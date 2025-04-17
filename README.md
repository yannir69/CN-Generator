# CN-Generator
 Masters Thesis Project

## Git Setup
1. Clone the repository:  

    `git clone https://github.com/yannir69/CN-Generator.git`  
    `cd CN-Generator`    

2. Create a virtual environment: 

    `python -m venv venv`    
    `venv\Scripts\activate`            

3. Install Dependencies:  

    `pip install -r requirements.txt`  

## 🔐 API Key Setup

This app uses the Groq API to generate responses. To run it, you'll need a personal API key. 

### Steps:

1. Go to https://console.groq.com and log in or sign up.  
2. Create an API key.
3. In the root folder of this project, open the .env file and paste your API key:  

    `GROQ_API_KEY=your_key_here`     

4. Start the app as usual:   

    `python cnGenerator.py`  

The server will now run at http://localhost:5500  

Created by Yannik Rohrschneider as part of a Master's Thesis at Freie Universität Berlin.  