import requests


class Chat:
    def __init__(self, base, prompt):
        self.base = base
        self.messages = [{
            "role": "system",
            "content": prompt
        }]

    def send_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

        response = requests.post(f"{self.base}v1/chat/completions", json={
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }).json()['choices'][0]['message']

        self.messages.append(response)
        return response["content"]
