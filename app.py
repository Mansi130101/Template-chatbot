from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from env import Gemini_key as API_key

genai.configure(api_key=API_key)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

app = Flask(__name__, static_url_path='', static_folder='static')

def get_response(message):
    try:
        response = chat.send_message(message)
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Sorry, I couldn't get a response."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return send_from_directory('static', 'chatbot.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "No message received."}), 400
    reply = get_response(user_message)
    return jsonify({'response': reply})

if __name__ == "__main__":
    app.run(debug=True)
