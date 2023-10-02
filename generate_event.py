import time
import random
import threading
import requests

endpoints = ("api/moderate_hb", "api/moderate_llm")
texts = ("how to sum 2 + 2", "how to learn german", "how to cook eggs")

HOST = "http://127.0.0.1:5000/"

def run():
    while True:
        try:
            target = random.choice(endpoints)
            text   = random.choice(texts)

            data = {
                'text': text,
            }

            response = requests.post(HOST + target, json=data)
            if response.status_code == 200:
                print('POST request was successful!')
                print('Response content:', response.text)
            else:
                print('POST request failed with status code:', response.status_code)

        except requests.RequestException:
            print("cannot connect", HOST)
            time.sleep(1)


if __name__ == "__main__":
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(random.randint(1, 10))
