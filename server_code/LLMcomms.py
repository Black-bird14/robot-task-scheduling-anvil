import anvil.server

@anvil.server.callable
def get_chat_history():
  if "chat_history" not in anvil.server.session:
      anvil.server.session["chat_history"] = {
          "outputs": ["Hello and welcome to RBT!"],
          #"past_user_inputs": ["..."]
      }
  return anvil.server.session["chat_history"]

@anvil.server.callable
def send_message(message):
  chat_history = get_chat_history()
  model_output = anvil.server.call('llm_runner')
  anvil.server.session["chat_history"] = model_output["chat_history"]
  return model_output["chat_history"]