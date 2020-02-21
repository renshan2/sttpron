# FAQ Bot Keras
A simple FAQ Bot built with Keras and Flask.

## Requirements
1) Tensorflow
2) Keras
3) flask
4) nltk

## Setup and Usage
Create a folder named trainedModel.
Edit the FAQ_db.json file as per need.
Run the following to train the bot using the FAQ_db.json file.
```python
trainBot.py
```
Run the following to launch the FAQ Bot server
```python
python server.py
```
Head over to the url in the output which will be http://127.0.0.1:5000 in a browser and start conversing

#### References:
More on stemming: https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html
