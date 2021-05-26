import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests, webbrowser
from bs4 import BeautifulSoup

listener = sr.Recognizer()
listener.energy_threshold = 4000
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# print(len(voices))
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen_bg():
    with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source, duration=0.2)
            voice = listener.listen(source)
            print('Listened...')
            try:
                command = listener.recognize_google(voice)
                print('Recognized...')
                command = command.lower()
                print(command)
                if 'hello anu' in command:
                    print(command)
                    return 'hello anu'
                else:
                    return command
            except:
                return 'none'

def take_command():
    try:
        res = listen_bg()
        if(res != "none"):
            return res
        else: 
            talk("sorry, could not recognise")
    except:
        return ""
    return ""


def run_anu():
    talk("Hello there i am anu, How may i help you")
    c = 0
    while True:
        if(c==1):
            break 
        command = take_command()
        print(command)
        if 'play' in command and 'song' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'search' in command or 'google' in command:
            user_search = command.replace('google','')
            user_search = user_search.replace('search','')
            google_search = requests.get('https://www.google.com/search?q='+user_search)

            soup = BeautifulSoup(google_search.text,'html.parser')

            search_results = soup.select('.kCrYT a')
            search_text = ''

            for links in search_results:
                if ('/url' in links.get('href') and 'BNeawe UPmit AP7Wnd' in str(links)):
                    # search_text += str(links) + '\n'
                    if(c == 1):
                        break
                    search_url = links.get('href')
                    search_text = links.get('href')[15:]
                    search_text = search_text[:search_text.find('/')]
                    print(search_text)
                    talk(search_text)
                    talk('Do you want to visit this link')
                    while(True):
                        yes_no = listen_bg()
                        if('yes' in yes_no):
                            webbrowser.open_new_tab('https://google.com/'+search_url)
                            c=1
                            break
                        elif('no' in yes_no):
                            break
                        else:
                            continue
                if(c==1):
                    break   
        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 3)
            print(info)
            talk(info)
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif "stop" in command or c == 1:
            break
        elif "exit" in command:
            exit(0)
        else:
            talk('Please say the command again.')


while True:
    res = listen_bg()
    if(res == "hello anu"):
        run_anu()

