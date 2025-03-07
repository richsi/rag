# src/util/helpers.py

def inference(user_query: str):
  try:
    from openai import OpenAI
    from src.config import OPENAI_API_KEY
  except:
    raise ImportError("Import error from src/util/helpers inference")

  client = OpenAI(api_key=OPENAI_API_KEY)

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a helpful assistant. Be clear and concise in your responses."},
      # {"role": "system", "content": "You are a helpful assistant. If your response includes LateX equations, you must enclose the formulas in double '$' signs. Be concise."},
      {
        "role": "user",
        "content": f"{user_query}"
      }
    ]
  )

  return completion.choices[0].message.content