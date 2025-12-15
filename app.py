import os
import time
from openai import OpenAI
from flask import Flask, request
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

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

    current_span = trace.get_current_span()  # <-- get a reference to the current span

    try:

        data = request.json
        user_type = data.get('userType')
        question = data.get('question')

        # track the type of user that makes each request
        current_span.set_attribute("user.type", user_type)

        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "user", "content": question}
            ]
        )

        if user_type == 'bronze':
            raise SystemError
        if user_type == 'silver':
            time.sleep(2);

        return completion.choices[0].message.content

    except Exception as ex:
        current_span.set_status(Status(StatusCode.ERROR))
        current_span.record_exception(ex)

