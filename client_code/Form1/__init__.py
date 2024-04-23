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
    self.qNumber=0
    #self.chat_history['outputs'].append(self.img)
    self.chat_history['outputs'].append("Are you running this locally? \n Reply with either Yes or No")
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
      good_instructions="Move all the blocks to the top left corner, Put the yellow block in the middle"
      complex_instructions="Group all the red objects together, Stack all the blocks in the bottom right corner"
      self.chat_history['outputs'].append("Here is a list of objects present in the simulated environment" + self.env_description) 
      self.chat_history['outputs'].append("Before you start, here are the types of instructions that the model handles well:\n"+good_instructions)
      self.chat_history['outputs'].append("It is hard for the LLM to handle instructions with the verb stack. Also the coordinate extraction has issues handling objects with similar colours.\n Here are examples of complex instructions:\n"+complex_instructions)
      self.chat_history['outputs'].append("Enter instructions in a list, separate them by commas, like in the examples.\n When you are done, press the ENTER key")
  
  def check_user_input(self, input, qNumber):
    if input.lower()=="yes":
      self.handle_yes(qNumber)
      #self.chat_history['outputs'].append("Would you like to run the demo or provide some instructions for the robot to run?\n Say Yes for demo and No to provide instructions")
    elif input.lower()=="no":
      self.handle_no(qNumber)
    else:
      sorted_tasks=anvil.server.call('llm_runner', self.env_description, input)
      anvil.server.call('blender_', sorted_tasks)
      self.chat_history['outputs'].append("That's the end of this demo, thank you and goodbye!")

  
  def refresh_chat(self):
      messages = []
      user_inputs = self.chat_history["past_user_inputs"]
      print(user_inputs)
      responses = self.chat_history["outputs"]
      for idx in range(len(responses)):
        if not user_inputs:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": "..."})
        elif len(user_inputs)<:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": "..."})
        else:
          messages.append({"from": "robot", "text": responses[idx]})
          messages.append({"from": "user", "text": user_inputs[idx]})
      self.convo_box.items = messages

  def send__click(self, **event_args):
    """This method is called when the button is clicked"""
    self.qNumber+=1
    self.chat_history = anvil.server.call('send_message', self.msg.text)
    self.check_user_input(self.msg.text)
    self.msg.text = ""
    self.refresh_chat()
    self.send_.scroll_into_view()
    
  def press_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.send__click()






