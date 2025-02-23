import random
import json
import torch
from app.model import NeuralNet
import os

from app.nltk_utils import bag_of_words, tokenize
from app.weather import get_weather, get_city
from app.translator import translate_parallel, translate_en, translate_ru
from flask import Flask, request, jsonify
from waitress import serve
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Create a Flask app
app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('app/intents-ALMET.json', 'r') as f:
    intents = json.load(f)

FILE = "app/data-almet.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = translate_ru("Alita")

@app.route('/')
def home():
    return (translate_ru("Let's chat! (type stop to exit)"))

@app.route('/chat', methods=['POST'])
def chat():
    while True:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({translate_ru("error"): translate_ru("No message found")}), 400
        
        sentence = translate_en(user_input)
        print(f"translated: {sentence}")
        if sentence.lower() == "stop":
            break

        tokenized_sentence = tokenize(sentence)
        X = bag_of_words(tokenized_sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        #print(f"Predicted tag: {tag}")
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        #print(f"Probability: {prob.item()}")

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response = str(random.choice(intent['responses']))
                    # traslate the response
                    print(f"English: {response}")
                    response = translate_ru(response)
                    #print(f"{bot_name}: {response}")
                    if tag == "weather":
                        city_name = get_city(sentence)
                        response = get_weather(city_name)
        else:
            response = (f"{bot_name}: {translate_ru("I do not understand...")}")
        decoded_response = response
        response = {bot_name: decoded_response}
        return jsonify(response),200

def weather(city_name):
    get_weather(city_name)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
    #serve(app, host='