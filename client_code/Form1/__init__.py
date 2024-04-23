from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.local=False
    self.chat_history = anvil.server.call('get_chat_history')
    self.env_description= anvil.server.call('send_description')
    print(self.env_description)
    _, self.img= anvil.server.call('set_env')
    #self.chat_history['outputs'].append(self.img)
    self.chat_history['outputs'].append("Are you running this locally? \n Reply with either Yes or No")
    self.chat_history['outputs'].append(self.env_description)
    self.refresh_chat()
    
  def handle_yes(self, qNumber):
    if qNumber == 1:
      self.local=True
    elif qNumber == 2 and not self.local:
      anvil.server.call('llm_runner')
      self.chat_history['outputs'].append("The instructions will now be processed by the robot")
    elif qNumber == 2 and self.local:
      sorted_tasks=anvil.server.call('llm_runner')
      anvil.server.call('blender_', sorted_tasks)
      self.chat_history['outputs'].append("That's the end of this demo, thank you and goodbye!")
      
  def handle_no(self, qNumber):
    if qNumber == 1:
      self.local=False
    elif qNumber == 2:
      return None
    
  def check_user_input(self, input, qNumber):
    if input.lower()=="yes":
      self.handle_yes(qNumber)
      #self.chat_history['outputs'].append("Would you like to run the demo or provide some instructions for the robot to run?\n Say Yes for demo and No to provide instructions")
    else:
      self.handle_no(qNumber)
  def refresh_chat(self):
      messages = []
      user_inputs = self.chat_history["past_user_inputs"]
      print(user_inputs)
      responses = self.chat_history["outputs"]
      for idx in range(len(responses)):
        if not user_inputs:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": "..."})
        elif len(user_inputs)==1 and user_inputs==["..."]:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": "..."})
        else:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": user_inputs[idx]})
      self.convo_box.items = messages

  def send__click(self, **event_args):
      """This method is called when the button is clicked"""
      self.chat_history = anvil.server.call('send_message', self.msg.text)
      self.check_user_input(self.msg.text)
      self.msg.text = ""
      self.refresh_chat()
      self.send_.scroll_into_view()
    
  def press_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      self.send__click()






