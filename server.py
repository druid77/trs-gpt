import socket
import os
import json
import openai

OPENAI_MODEL = "gpt-3.5-turbo"
openai.api_key = "<REDACTED>"
conversation = []

def do_open_ai_query(chat_input):
    try:

        # Make a call to the OpenAI API to get the chat GPT response
        completion = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content":  chat_input
                }
            ])

        return completion.choices[0].message.content

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def chat_with_gpt3(messages):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages
    )
    return response.choices[0].message['content']


def handle_client(client_socket):
    user_input = client_socket.recv(1024).decode()
    print(f"Received data from client: {user_input}")

    conversation.append({"role": "user", "content": user_input})

    response = chat_with_gpt3(conversation)

    conversation.append({"role": "assistant", "content": response})

    client_socket.send(response.encode())
    client_socket.close()

def main():
    host = '0.0.0.0'
    port = 43

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on port {port}")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Accepted connection from {client_addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    main()
