import speech_recognition as sr
from assistant import utils
import time
from fuzzywuzzy import fuzz
import pyttsx3


def say(text, engine):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    questions = utils.load_questions()
    answers = utils.load_answers()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # loc nhieu
        is_communicate = True
        count_failed = 0
        say("Hi, nice to meet you", engine)
        while is_communicate:
            say("what information would you like to know?", engine)
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            try:
                print('Waiting...')
                say("please wait a moment", engine)
                ques = recognizer.recognize_google(audio, language='vi')
                print("Question: ", ques)
                ques_num = utils.find_question_num(ques, questions)
                print("Question num: ", ques_num)
                if ques_num != -1:
                    print("Answer: ", answers[ques_num])
                    say(answers[ques_num], engine)
                else:
                    say("I don't know", engine)
                say('do you want any other information?', engine)
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                next = recognizer.recognize_google(audio, language='en')
                print(next)
                next = utils.remove_accents(next.lower())
                if (fuzz.ratio(next, 'no thank') >= 70 or
                    fuzz.ratio(next, 'no') >= 70 or
                    fuzz.ratio(next, "i don't") >= 70):
                    say('Goodbye, have a nice day', engine)
                    break
            except sr.RequestError:  # Service/network error
                print("API unavailable")
                count_failed += 1
            except sr.UnknownValueError:  # Can't convert speech to text
                print("Unable to recognize speech")
                say("can you repeat?", engine)
                count_failed += 1
            if count_failed >= 5:
                break
            time.sleep(0.2)
