from chatbot_app.ai.ollama_api import ask_ollama

question = input("Ask : ")

print()

answer = ask_ollama(question)

print(answer)