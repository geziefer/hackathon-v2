from flask import Flask, request
from flask_cors import CORS
from Agent import Agent


app = Flask(__name__)
CORS(app)

agent = Agent()


@app.route("/clear-chat", methods=["GET"])
def clear_chat():
    agent.reset_messages()

    return {"status": 200}


@app.route("/ask-assistant", methods=["POST"])
def ask_assistant():
    prompt = request.json["prompt"]

    _ = agent.get_response(prompt)

    return {"conversation": agent.conversation}


if __name__ == "__main__":
    app.run(port=5000)
