import time
from fuzzywuzzy import fuzz
import pyttsx3
import speech_recognition as sr


def find_question_num(ques, list_ques):
    best_score = -1.
    best_ques_num = -1.
    ques = remove_accents(ques.lower())
    for i, existed_ques in enumerate(list_ques):
        existed_ques = remove_accents(existed_ques.lower())
        score = fuzz.ratio(existed_ques, ques)
        if score > best_score:
            best_ques_num = i
            best_score = score
    if best_score >= 60:
        return best_ques_num
    else:
        return -1


def load_questions():
    with open('data/Question.txt', encoding='utf16') as fp:
        text = fp.read()
        questions = text.split('\n')
        return questions


def load_answers():
    with open('data/Answer.txt', encoding='utf16') as fp:
        text = fp.read()
        answers = text.split('\n')
        return answers

def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    input_str.encode('utf-8')
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def say(text, engine):
    engine.say(text)
    engine.runAndWait()

def run(engine,showLoading,hideLoading):
    questions = load_questions()
    answers = load_answers()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine.setProperty('rate', 175)

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
                showLoading()
                say("please wait a moment", engine)
                hideLoading()
                ques = recognizer.recognize_google(audio, language='vi')
                print("Question: ", ques)
                ques_num = find_question_num(ques, questions)
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
                next_sent = remove_accents(next.lower())
                if 'no' in next_sent:
                    say("Goodbye. have a nice day!", engine)
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
        engine.stop()
