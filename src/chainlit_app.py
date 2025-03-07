# src/chainlit_app.py
import chainlit as cl
import requests

FASTAPI_URL = "http://localhost:8001/api/query"

@cl.on_message
async def main(msg: cl.Message):

  payload = {"query": msg.content}

  response = requests.post(FASTAPI_URL, json=payload, timeout=5)

  if response.ok:
    data = response.json()
    await cl.Message(
      content=f"Received: {data["response"]}",
    ).send()
  else:
    print(response.status_code)
    await cl.Message(content="Something went wrong!").send()