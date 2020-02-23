from flask import Flask, render_template, request, redirect, jsonify
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from numpy import array, argmax
from keras import models
from pickle import load
from random import choice

from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests

   
def getQueryFeatures(query):
    queryTokens = word_tokenize(query)
    queryStems = sorted(list(set([stemmer.stem(w.lower()) for w in queryTokens if w not in ignored])))
    queryBag = []
    for w in vocabulary:
        queryBag.append(1) if w in queryStems else queryBag.append(0)
    queryBag = array(queryBag)
    return queryBag.reshape(1, len(vocabulary))

with open('trainedModel/vars.pkl', 'rb') as f:
    vocabulary, classes, ignored, intents = load(f)
intentsDict = {i['tag']: i['responses'] for i in intents['intents']}
model = models.load_model('trainedModel/FAQbot_model.h5')
stemmer = LancasterStemmer()

def get_response(query):
    queryBag = getQueryFeatures(query)
    model.predict(queryBag)
    idx = argmax(model.predict(queryBag))
    return choice(intentsDict[classes[idx]])

query = "This is me"
reply = "Hello there"

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('preproc.html', questionAsked=query, response=reply)

@app.route('/signup', methods = ['POST'])
def signup():
    global query
    global reply
    query = request.form['question']    
    response = get_response(query)
    print(response)
    reply = response
    return redirect('/')

@app.route('/lower', methods=["GET", "POST"])
def lower_case():
    global query
    global reply
    query = request.form['text']    
    response = get_response(query)
    print(response)
    reply = response
    word = query.lower()
    result = {
        "query": word,
        "response": response
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/sendaudio', methods = ['GET'])
def sendaudio():
    global query
    global reply

    def assistant(command):
        "if statements for executing commands"

        if 'open reddit' in command:
            reg_ex = re.search('open reddit (.*)', command)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            print('Done!')

        elif 'open website' in command:
            reg_ex = re.search('open website (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
                print('Done!')
            else:
                pass

        elif 'what\'s up' in command:
            talkToMe('Just doing my thing')
            
        elif 'joke' in command:
            res = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"}
                    )
            if res.status_code == 200:
                talkToMe(str(res.json()['joke']))
            else:
                talkToMe('oops!I ran out of jokes')
        elif 'email' in command:
            talkToMe('Who is the recipient?')
            recipient = myCommand()

            if 'John' in recipient:
                talkToMe('What should I say?')
                content = myCommand()

                #init gmail SMTP
                mail = smtplib.SMTP('smtp.gmail.com', 587)

                #identify to server
                mail.ehlo()

                #encrypt session
                mail.starttls()

                #login
                mail.login('username', 'password')

                #send message
                mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

                #end mail connection
                mail.close()

                talkToMe('Email sent.')

            else:
                talkToMe('I don\'t know what you mean!')

        
        # elif 'current weather in' in command:
        #     reg_ex = re.search('current weather in (.*)', command)
        #     if reg_ex:
        #         city = reg_ex.group(1)
        #         weather = Weather()
        #         location = weather.lookup_by_location(city)
        #         condition = location.condition()
        #         talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))

        # elif 'weather forecast in' in command:
        #     reg_ex = re.search('weather forecast in (.*)', command)
        #     if reg_ex:
        #         city = reg_ex.group(1)
        #         weather = Weather()
        #         location = weather.lookup_by_location(city)
        #         forecasts = location.forecast()
        #         for i in range(0,3):
        #             talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
        #                      'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))
        return ("I am doing my thing")

    def myCommand():
        "listens for commands"

        r = sr.Recognizer()

        with sr.Microphone() as source:
            global query
            global response
            print('Ready...')
            query = 'Ready...'
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
            response = command

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Your last command couldn\'t be heard')
            command = myCommand()

        return command

    def talkToMe(audio):
        "speaks audio passed as argument"
        for line in audio.splitlines():
            os.system("say " + audio)

        #  use the system's inbuilt say command instead of mpg123
        #  text_to_speech = gTTS(text=audio, lang='en')
        #  text_to_speech.save('audio.mp3')
        #  os.system('mpg123 audio.mp3')

    query = myCommand()   
    response = get_response(query)
    print(response)
    reply = response
    word = query.lower()
    result = {
        "query": word,
        "response": response
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(debug=True)
