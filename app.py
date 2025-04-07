from flask import Flask, request, render_template, jsonify, session
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load API key from env file
load_dotenv("api.env")
api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'  # Required for session memory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    # Initialize session memory
    if 'chat_history' not in session:
        session['chat_history'] = []
    if 'user_name' not in session:
        session['user_name'] = None

    # Detect name from input and store
    lowered = prompt.lower()
    if "my name is" in lowered:
        name = prompt.split("my name is", 1)[1].strip().split()[0]
        session['user_name'] = name
    elif "i am" in lowered:
        name = prompt.split("i am", 1)[1].strip().split()[0]
        session['user_name'] = name

    # Add user message to history
    session['chat_history'].append({"role": "user", "content": prompt})

    # Create system message
    system_msg = "You are an AI chatbot created and maintained by Trend Hive Academy."

    messages = [
        {"role": "system", "content": system_msg}
    ] + session['chat_history']

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        session['chat_history'].append({"role": "assistant", "content": answer})
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": "An error occurred while fetching the AI response."})

@app.route("/get_memory")
def get_memory():
    chat_history = session.get('chat_history', [])
    return jsonify({"history": chat_history})

@app.route("/save_user_info", methods=["POST"])
def save_user_info():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    
    # Save into session (or database logic can go here)
    session['user_name'] = name
    session['user_email'] = email

    return jsonify({"message": "User info saved successfully."})

if __name__ == "__main__":
    app.run(debug=True)
