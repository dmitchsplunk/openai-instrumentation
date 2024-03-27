from openai import OpenAI
from flask import Flask, request
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

app = Flask(__name__)

OpenAIInstrumentor().instrument()
client = OpenAI()

@app.route("/askquestion", methods=['POST'])
def ask_question():
    current_span = trace.get_current_span()

    data = request.json
    user_type = data.get('userType')
    question = data.get('question')

    # track the type of user that makes each request
    current_span.set_attribute("user.type", user_type)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return completion.choices[0].message.content
