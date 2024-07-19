from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load pre-trained model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Generate response
def generate_response(input_text):
    inputs = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    reply_ids = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('input')
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)