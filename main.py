# A terminal based AI interface

import requests
import os
import json
import time
import re
from colorama import Fore, Style


os.system('cls' if os.name == 'nt' else 'clear')

with open("prompt.txt", 'r') as f:
    prompt = f.read()

url = "https://ai.hackclub.com/chat/completions" # api url
headers = {
    "Content-Type": "application/json"
}
data = { # the dictionary which contains all messages
    "messages": [
        {"role": "system", "content": prompt}
    ],
    "model": "qwen/qwen3-32b"
}

if data["model"] == "qwen/qwen3-32b":
    while(True):
        think = input(f"{Fore.CYAN}Would you like to show thinking? Y/n {Style.RESET_ALL}")
        if "y" in think.lower():
            data["reasoning_effort"] = "default"
            break
        elif "n" in think.lower():
            data["reasoning_effort"] = "none"
            break
        else:
            continue
print(f"{Fore.BLUE}Using model {data["model"]}{Style.RESET_ALL}")
while(True):
    message = input(f"{Fore.GREEN}Your message: {Style.RESET_ALL}")

    # arguments
    if message == ".exit":
        exit(0)

    elif message.startswith(".save"): # saves the chat to a .json file
        os.makedirs('log', exist_ok=True)

        fileName = f'log/{time.strftime("%Y-%m-%d_%H.%M.%S")}-log.json'

        try:
            with open(fileName, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"Successfully saved chat log to {fileName}!")
        # if not able to save chat log, then give error
        except Exception as e:
            print(f"{Fore.RED}Failed to save chat log to {Style.RESET_ALL}{fileName}: {e}")

    elif message.startswith(".load"): # loads a previous chat from a .json file
        while(True):
            os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

            parts = message.strip().split(" ") # split the message into a list that can be measured

            # allowing for either the file provided in command or in a separate dialog
            if len(parts) == 1:
                file = input(f"{Fore.BLUE}What is the name of the chat log that you are trying to upload? {Style.RESET_ALL}") # the file containing the messages
            else:
                file = parts[1]
            try:
                with open(file.strip(), 'r') as f:
                    data = json.load(f)

                os.system('cls' if os.name == 'nt' else 'clear')
                
                print(f"{Fore.BLUE}Using model {data["model"]}{Style.RESET_ALL}")
                for message in data["messages"]:
                    if message["role"] == "user":
                        print(f'{Fore.GREEN}Your message: {Style.RESET_ALL}{message["content"]}\n')
                    elif message["role"] == "assistant":
                        print(f'{message["content"]}\n')
                break

            except FileNotFoundError as e: # if .json not found
                input(f"{Fore.RED}Could not find the chat log file, remember to include the .json and the directory:{Style.RESET_ALL} {e}")
                continue

            except Exception as e:
                print(f"{Fore.RED}Could not load chat log: {Style.RESET_ALL}{e}")
                break
    
    else:
        data["messages"].append({"role": "user", "content": message})

        try:
            response = requests.post(url, headers=headers, timeout=10, json=data).json()

        except requests.JSONDecodeError as e:
            print(f"{Fore.RED}Failed to decode JSON from API: {Style.RESET_ALL}{e}")
            continue

        try:
            responseContent = response["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"{Fore.RED}Could not access dictionary properly: {Style.RESET_ALL}{e}")
        print(f"\n{responseContent}\n")
        data["messages"].append({"role": "assistant", "content": responseContent})