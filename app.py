import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# OpenAI API key (replace with the actual key)
openai.api_key = "your openAI ApiKey"

def extract_fields_values(text):
    # Send user text to GPT model to extract fields and values
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or any other model you have access to
        messages=[
            {"role": "system", "content": "You are an assistant that extracts customer details and part numbers from user input."},
            {"role": "user", "content": text}
        ],
        max_tokens=150
    )

    # Get the response content
    content = response.choices[0].message['content']
    
    # Parse content into a dictionary for easy access
    extracted_data = {}
    for line in content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            extracted_data[key.strip()] = value.strip()

    return extracted_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_input = request.form['user_input']
    extracted_data = extract_fields_values(user_input)
    
    return render_template('result.html', data=extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
