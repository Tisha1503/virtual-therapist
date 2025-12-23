from openai import OpenAI

client = OpenAI(api_key="")

def load_knowledge():
    with open("knowledge.txt", "r", encoding="utf-8") as file:
        return file.read()

def virtual_therapist():
    additional_context = load_knowledge()
    
    print("Hello!! How can I assist you today? (Type 'q' to quit)") 

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'q':
            break

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": f"You are a Virtual Therapist. Use this info to help: {additional_context}"},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content
        print(f"Therapist: {answer}")

if __name__ == "__main__":
    virtual_therapist()