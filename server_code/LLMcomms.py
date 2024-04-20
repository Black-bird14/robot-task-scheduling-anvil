import anvil.server
import requests

@anvil.server.callable
def get_chat_history():
  if "chat_history" not in anvil.server.session:
      anvil.server.session["chat_history"] = {
          "outputs": ["Welcome to RBT, do you want to see the demo? Say No if you would rather submit instructions yourself."],
          "past_user_inputs": [""]
      }
  return anvil.server.session["chat_history"]

@anvil.server.callable
def send_message(message):
  chat_history = get_chat_history()
  model_output = 
  anvil.server.session["chat_history"] = model_output["chat_history"]
  return model_output["chat_history"]