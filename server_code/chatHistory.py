import anvil.server

@anvil.server.callable
def get_chat_history():
  if "chat_history" not in anvil.server.session:
      anvil.server.session["chat_history"] = {
          "outputs": ["Hello and welcome to RBT!"],
      }
  return anvil.server.session["chat_history"]
