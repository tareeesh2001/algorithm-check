# app/__init__.py
from flask import Flask, jsonify, render_template, request
import json
from app.model import ask_llama


app = Flask(__name__, template_folder="../templates")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/')
def index():
    return render_template('index.html', name="tareesh")

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        prompt = request.json['prompt']
        code = request.json['code']
        print("PROMPT", prompt)
        print("CODE", code)
        
        
        final_prompt = """**Task:** Analyze the provided code snippet and generate a response in JSON format, strictly adhering to the following structure:"\nStructure: {'Result': 'YES or NO'}\n**Instructions:**\n
            """
        final_prompt += f"1. Restrict the 'Result' field to a single word: 'YES' if the code implements the {prompt} algorithm, 'NO' otherwise.\n"

        final_prompt += f'**Code:** {code}\n\n'
        final_prompt += f'**Note:** Please refrain from adding any additional text or formatting outside of the specified JSON structure. Adhere strictly to the Response Format Requirements.'
        
        generated_text = ask_llama(final_prompt)
        print(generated_text)
        
        return {"response": generated_text}
