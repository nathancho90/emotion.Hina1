import os
from flask import CORS
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import tensorflow as tf

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load OpenAI API key and Hugging Face API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
hf_api_key = os.getenv('HF_API_KEY')

# Initialize Hugging Face emotion detection model with TensorFlow
def initialize_transformer_pipeline():
    model_name = "j-hartmann/emotion-english-distilroberta"  # You can replace this model name with another if needed
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = initialize_transformer_pipeline()

def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = tf.argmax(logits, axis=-1).numpy()[0]
    emotion = model.config.id2label[predicted_class]
    return emotion

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Use Hugging Face model to predict emotion
    try:
        predicted_emotion = predict_emotion(user_message)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Call OpenAI API to get a response
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # GPT-3 model
            prompt=user_message,
            max_tokens=150
        )
        
        bot_message = response['choices'][0]['text'].strip()
        
        return jsonify({
            'emotion': predicted_emotion,
            'response': bot_message
        })
    
    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
