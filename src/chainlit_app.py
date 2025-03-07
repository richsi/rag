# src/chainlit_app.py
import chainlit as cl
import requests

FASTAPI_URL = "http://localhost:8001/api/ask"

@cl.on_message
async def main(message: cl.Message):

  payload = {"query": message.content}

  response = requests.post(FASTAPI_URL, json=payload, timeout=5)

  if response.ok:
    data = response.json()
    await cl.Message(
      content=f"Received: {data["answer"]}",
    ).send()
  else:
    print(response.status_code)
    await cl.Message(content="Something went wrong!").send()