from ollama import chat


def ask_ollama(question):

    try:
        response = chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI College Assistant.

Answer questions about any college or university,
including courses, admission, fees, exams, departments,
subjects, scholarships, results, assignments, library,
campus, hostel, placements and student life.

Give simple and useful answers.

If the question is completely unrelated to college
or education, reply exactly:

Sorry, I can only answer college-related questions.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response["message"]["content"].strip()

    except Exception as e:
        print("Ollama Error:", e)
        return "Sorry, I am unable to answer right now."