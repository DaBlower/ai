# A terminal based AI interface

import requests
import os
import json
import time


os.system('cls' if os.name == 'nt' else 'clear')
url = "https://ai.hackclub.com/chat/completions" # api url
headers = {
    "Content-Type": "application/json"
}
data = { # the dictionary which contains all messages
    "messages": [
    ]
}

while(True):
    message = input("Your message: ")

    # arguments
    if message == ".exit":
        exit(0)

    elif message == ".save": # saves the chat to a .json file
        os.makedirs('log', exist_ok=True)

        fileName = f'log/{time.strftime("%Y-%m-%d_%H.%M.%S")}-log.json'

        try:
            with open(fileName, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"Successfully saved chat log to {fileName}!")
        # if not able to save chat log, then give error
        except Exception as e:
            print(f"Failed to save chat log to {fileName}: {e}")

    elif message.startswith(".load"): # loads a previous chat from a .json file
        os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

        parts = message.strip().split(" ") # split the message into a list that can be measured

        # allowing for either the file provided in command or in a separate dialog
        if len(parts) == 1:
            file = input("What is the name of the chat log that you are trying to upload? ") # the file containing the messages
        else:
            file = parts[1]
        try:
            with open(file.strip(), 'r') as f:
                data = json.load(f)

            os.system('cls' if os.name == 'nt' else 'clear')

            for message in data["messages"]:
                if message["role"] == "user":
                    print(f'Your message: {message["content"]}\n')
                elif message["role"] == "assistant":
                    print(f'{message["content"]}\n')

        except FileNotFoundError as e: # if .json not found
            print(f"Could not find the chat log file, remember to include the .json: {e}")

        except Exception as e:
            print(f"Could not load chat log: {e}")
    
    else:
        data["messages"].append({"role": "user", "content": message})

        try:
            response = requests.post(url, headers=headers, timeout=10, json=data).json()

        except requests.JSONDecodeError as e:
            print(f"Failed to decode JSON from API: {e}")
            continue

        try:
            responseContent = response["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"Could not access dictionary properly: {e}")

        print(f"\n{responseContent}\n")
        data["messages"].append({"role": "assistant", "content": responseContent})