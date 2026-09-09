from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY is missing!")
else:
    print("Groq API key loaded successfully.")

# Create Groq client
client = Groq(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and friendly AI chatbot."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("GROQ API ERROR:", repr(e))
        return jsonify({
            "reply": "Sorry, something went wrong. Check the terminal."
        })


if __name__ == "__main__":
    app.run(debug=True)