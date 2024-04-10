from openai import OpenAI
from flask import Flask, request

app = Flask(__name__)

# use this config for the real OpenAI API
client = OpenAI()

@app.route("/askquestion", methods=['POST'])
def ask_question():
    data = request.json
    user_type = data.get('userType')
    question = data.get('question')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return completion.choices[0].message.content
