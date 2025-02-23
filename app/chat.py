import random
import json
import torch
from model import NeuralNet

from nltk_utils import bag_of_words, tokenize
from weather import get_weather, get_city
from translator import translate_parallel, translate_en, translate_ru
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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
print(translate_ru("Let's chat! (type stop to exit)"))
while True:
    sentence = input(f"{translate_ru("You")}: ")
    sentence = translate_en(sentence)
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
                print(f"{bot_name}: {response}")
                if tag == "weather":
                    city_name = get_city(sentence)
                    get_weather(city_name)
    else:
        print(f"{bot_name}: {translate_ru("I do not understand...")}")

def weather(city_name):
    get_weather(city_name)