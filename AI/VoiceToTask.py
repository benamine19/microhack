import json
from openai import OpenAI
from dotenv import load_dotenv
import os

def VoiceToTask(audio_path):
    client = OpenAI(api_key=os.getenv("API_KEY"))

    audio_file = open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )

    Cretarias = {
        "Task" : "abstract the task from the managers message",
        "Specialites": [    "Builder",
                            "Electrician",
                            "Plumber",
                            "Painter",
                            "Carpenter",
                            "Mason",
                            "Architect",
                            "Engineer"],
        "Importance": [ "High",
                        "Medium",
                        "Low",],
        "Duration": "estimate the duration to complete this task in this format dd:hh:mm",
        "Names":"give me a list of the names of the workers that was listed in the managers message",
    }




    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {
            "role": "user",
            "content": [
            {"type": "text", "text": "this is a message from a manager :" + transcription+"  the Criterias are : " + str(Cretarias) + " Return one of the values for each cretarias.devide it and respond in this json format {\"Criteria\": results}"},
        ],
        },
    ]
    )
    json_data = json.loads(response.choices[0].message.content)

    return json_data


fdf = VoiceToTask("Audio/Audio.m4a")
print(fdf)