import anvil.server
import requests

@anvil.server.callable
def get_chat_history():
  if "chat_history" not in anvil.server.session:
      anvil.server.session["chat_history"] = {
          "past_user_inputs": ["Merry Christmas!"],
          "llm_outputs": ["Welcome"]
      }
  return anvil.server.session["chat_history"]

@anvil.server.callable
def send_message(message):
  chat_history = get_chat_history()
  model_output = query({
    "inputs": {
      "text": message,
      **chat_history
    }
  })
  anvil.server.session["chat_history"] = model_output["chat_history"]
  return model_output["chat_history"]