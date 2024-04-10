import os
from openai import OpenAI
from flask import Flask, request
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace

app = Flask(__name__)

OpenAIInstrumentor().instrument()

# use this config for the real OpenAI API
#  client = OpenAI()

# use this config for the Mock GPT API
client = OpenAI(
    api_key=os.environ.get("MOCK_GPT_API_KEY"),
    base_url="https://mockgpt.wiremockapi.cloud/v1"
)
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
