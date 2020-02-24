from flask import Flask, render_template, request, redirect, jsonify
from gevent.pywsgi import WSGIServer
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from numpy import array, argmax
from keras import models
from pickle import load
from random import choice
from playsound import playsound
from datetime import datetime
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import errno, os, stat, shutil
   
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
    # print(intentsDict[intents[idx]])
    return choice(intentsDict[classes[idx]])

def talkToMe(audio):
    "speaks audio passed as argument"
    #for line in audio.splitlines():
    #    os.system("say " + audio)
    # remove file audio.mp3 if it exists
    dirname = os.getcwd()
    
    fileext = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
    text_to_speech = gTTS(text=audio, lang='en')

    audiofile = os.path.join(dirname, 'audio'+ fileext + '.mp3')
    text_to_speech.save(audiofile)    
    try:
        playsound(audiofile)
    except:
        print("the audio file is locked.")

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      print("cannot remove readonly of mp3 file")
      #raise

def removeAudioFiles(dir_name):
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".mp3"):
            filename = os.path.join(dir_name, item)
            #shutil.rmtree(filename, ignore_errors=False, onerror=handleRemoveReadonly)
            try:
                os.remove(filename)
            except:
                print("cannot remove readonly mp3 file, let's wait...")

query = "Hi"   
reply = "Welcome to English Pronunciation Correction"

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    removeAudioFiles(os.getcwd())    
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

@app.route('/sendtext', methods=["GET", "POST"])
def sendtext():
    global query
    global reply
    query = request.form['text']  
    
    response = get_response(query) 
    #print(response)  
    talkToMe(response) 
    #reply = response
    #word = query.lower()
    result = {
        1: query, 2: response
    }
    result = {str(key): value for key, value in result.items()}
    print(result)
    return jsonify(result=result)

@app.route('/sendaudio', methods = ['GET'])
def sendaudio():
    global query
    global reply

    # def assistant(command):
    #     "if statements for executing commands"

    #     if 'open reddit' in command:
    #         reg_ex = re.search('open reddit (.*)', command)
    #         url = 'https://www.reddit.com/'
    #         if reg_ex:
    #             subreddit = reg_ex.group(1)
    #             url = url + 'r/' + subreddit
    #         webbrowser.open(url)
    #         print('Done!')

    #     elif 'open website' in command:
    #         reg_ex = re.search('open website (.+)', command)
    #         if reg_ex:
    #             domain = reg_ex.group(1)
    #             url = 'https://www.' + domain
    #             webbrowser.open(url)
    #             print('Done!')
    #         else:
    #             pass

    #     elif 'what\'s up' in command:
    #         talkToMe('Just doing my thing')
            
    #     elif 'joke' in command:
    #         res = requests.get(
    #                 'https://icanhazdadjoke.com/',
    #                 headers={"Accept":"application/json"}
    #                 )
    #         if res.status_code == 200:
    #             talkToMe(str(res.json()['joke']))
    #         else:
    #             talkToMe('oops!I ran out of jokes')
    #     elif 'email' in command:
    #         talkToMe('Who is the recipient?')
    #         recipient = myCommand()

    #         if 'John' in recipient:
    #             talkToMe('What should I say?')
    #             content = myCommand()

    #             #init gmail SMTP
    #             mail = smtplib.SMTP('smtp.gmail.com', 587)

    #             #identify to server
    #             mail.ehlo()

    #             #encrypt session
    #             mail.starttls()

    #             #login
    #             mail.login('username', 'password')

    #             #send message
    #             mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

    #             #end mail connection
    #             mail.close()

    #             talkToMe('Email sent.')

    #         else:
    #             talkToMe('I don\'t know what you mean!')

        
    #     # elif 'current weather in' in command:
    #     #     reg_ex = re.search('current weather in (.*)', command)
    #     #     if reg_ex:
    #     #         city = reg_ex.group(1)
    #     #         weather = Weather()
    #     #         location = weather.lookup_by_location(city)
    #     #         condition = location.condition()
    #     #         talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))

    #     # elif 'weather forecast in' in command:
    #     #     reg_ex = re.search('weather forecast in (.*)', command)
    #     #     if reg_ex:
    #     #         city = reg_ex.group(1)
    #     #         weather = Weather()
    #     #         location = weather.lookup_by_location(city)
    #     #         forecasts = location.forecast()
    #     #         for i in range(0,3):
    #     #             talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
    #     #                      'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))
    #     return ("I am doing my thing")

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
            command = r.recognize_google(audio)
            #print('You said: ' + command + '\n')
            response = command

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print('Your last command couldn\'t be heard')
            command = myCommand()

        return command

    query = myCommand()   
    response = get_response(query)    
    #reply = response
    talkToMe(response)
    word = query.capitalize()
    result = {
        1: word, 2: response
    }
    result = {str(key): value for key, value in result.items()}
    print(result)
    return jsonify(result=result)

if __name__ == "__main__":
    # Debug/Development
    app.run(debug=True, host="localhost", port="5000")
    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
