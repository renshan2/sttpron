# A chatBot Keras
A simple ChatBot built with Keras and Flask.

## Requirements
pip install Tensorflow, Keras, Flask, nltk
(do it one by one)

## Installation:
For Windows:
1. Install VS Code   
2. Install Anaconda Python Package   
3. pip install -r requirements.txt   
4. pip3 install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl   
(https://pypi.org/project/PyAudio/#files for your version, also looking into misc folder)


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
