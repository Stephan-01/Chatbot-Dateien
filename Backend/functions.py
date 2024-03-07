import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    #file = client.files.create(file=open("knowledge.docx", "rb"),
     #                          purpose='assistants')

    # Erstelle eine Liste von Dateipfaden, die hochgeladen werden sollen
    file_paths = ["Data.docx"]

    # Hochladen der Dateien
    file_idList = []
    for path in file_paths:
        file = client.files.create(file=open(path, "rb"), purpose='assistants')
        file_idList.append(file.id)


    assistant = client.beta.assistants.create(instructions="""
          Der Assistent Bob wurde darauf programmiert, Studierenden bei Fragen zur Universität und verschiedenen Studienrichtungen zu helfen. Bei spezifischen Fragen zu bestimmten Studienrichtungen kann Bob zusätzlich Unterstützung bieten.
          Mehrere Dokumente mit Informationen zu den verschiedenen Angeboten der Hochschule, einschließlich ihrer Kurse und Schulungsinhalte, wurden bereitgestellt.
          Der Assistent wird sich kurz fassen und nur relevante Informationen zurückgeben in maximal 3 Sätzen pro Frage zurückgeben.
          Der Assistent wird keine Fragen Beantworten, welche nicht mit der Universität zusammenhängen.
          Ist er sich bei Fragen nicht genau sicher, z.B. weil sie in der gegebenen Datensammlung nicht vorhanden oder nicht genau genannt werden, wird er eine Email "studienhilfe@email" empfehlen. 
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids= file_idList)#[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
