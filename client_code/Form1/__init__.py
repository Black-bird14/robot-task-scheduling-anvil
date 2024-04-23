from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.chat_history = anvil.server.call('get_chat_history')
    self.env_description= anvil.server.call('send_description')
    _, self.img= anvil.server.call('set_env')
    #self.chat_history['outputs'].append(self.img)
    self.chat_history['outputs'].append(self.env_description)
    
    self.refresh_chat()

  def refresh_chat(self):
      messages = []
      user_inputs = self.chat_history["past_user_inputs"]
      responses = self.chat_history["outputs"]
      for idx in range(len(user_inputs)):
          messages.append({"from": "user", "text": user_inputs[idx]})
          messages.append({"from": "robot", "text": responses[idx]})
      self.convo_box.items = messages

  def send__click(self, **event_args):
      """This method is called when the button is clicked"""
      self.chat_history = anvil.server.call('send_message', self.msg.text)
      self.msg.text = ""
      self.refresh_chat()
      self.send_.scroll_into_view()
    
  def press_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      self.send__click()






