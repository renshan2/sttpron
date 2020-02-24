# A chatBot Keras
A simple ChatBot built with Keras and Flask.

## Requirements
1) Tensorflow
2) Keras
3) flask
4) nltk

## Installation:
For Windows:
Install VS Code
Install Anaconda Python Package
pip install -r requirements.txt
pip3 install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
(https://pypi.org/project/PyAudio/#files)

## Setup and Usage
Create a folder named trainedModel.
Edit the intents.json file as per need.
Run the following to train the bot using the intents.json file.
python trainBot.py 
Run the following to launch the ChatBot server
python server.py

Head over to the url in the output which will be http://127.0.0.1:5000 in a browser and start conversing

#### References:
More on stemming: https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html
