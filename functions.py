import json
import requests
import os
from openai import OpenAI
from prompts import assistant_instructions

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)


# Create or load assistant
def create_assistant(client):
  assistant_file_path = 'assistant.json'

  # If there is an assistant.json file already, then load that assistant
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # If no assistant.json is present, create a new assistant using the below specifications

    # To change the knowledge document, modify the file name below to match your document
    # If you want to add multiple files, paste this function into ChatGPT and ask for it to add support for multiple files
    files = [client.files.create(file=open(file, "rb"), purpose='assistants') for file in ["Thiago Nigro (O Primo Rico)_ biografia e carreira.docx", "Método ARCA.docx", "Vídeos Primo Rico - Conhecimentos Gerais de Finanças.docx", "Do Mil Ao Milhao_ Sem Cortar o Cafezinho - Thiago Nigro.docx"]]

    file_ids = [file.id for file in files]  # Define the variable file_ids
    
    assistant = client.beta.assistants.create(
        # Change prompting in prompts.py file
        instructions=assistant_instructions,
        model="gpt-3.5-turbo-1106",
        tools=[
            {
                "type": "retrieval"  # This adds the knowledge base as a tool
            }
          ],
    file_ids=file_ids  # Use the list of file IDs
    )


    # Create a new assistant.json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
