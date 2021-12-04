import time
from fuzzywuzzy import fuzz
import speech_recognition as sr
from playsound import playsound


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
    with open('data/QuestionV2.txt') as fp:
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


def loop_check(source, recognizer):
    i = 0
    while i < 3:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language='vi')
            return text
        except sr.RequestError:
            break
        except sr.UnknownValueError:
            playsound("data/audio_data/repeat.mp3")
            i += 1


def run(engine, showLoading, hideLoading):
    questions = load_questions()
    # answers = load_answers()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine.setProperty('rate', 175)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # loc nhieu
        is_communicate = True
        count_failed = 0
        playsound("data/audio_data/greeting.mp3")
        while is_communicate:
            playsound("data/audio_data/open.mp3")
            # audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            try:
                # showLoading()
                # say("please wait a moment", engine)
                # hideLoading()
                ques = loop_check(source, recognizer)
                playsound("data/audio_data/wait.mp3")
                print('Waiting...')
                if ques is None:
                    break
                print("Question: ", ques)
                ques_num = find_question_num(ques, questions)
                print("Question num: ", ques_num)
                if ques_num != -1:
                    playsound(f'data/audio_data/{ques_num + 1}.m4a')
                else:
                    playsound("data/audio_data/dont_know.mp3")
                playsound("data/audio_data/continue.mp3")
                # audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                next_sent = loop_check(source, recognizer)
                if next_sent is None:
                    break
                print(next_sent)
                next_sent = next_sent.lower()
                if 'không' in next_sent:
                    playsound("data/audio_data/bye.mp3")
                    break
            except sr.RequestError:  # Service/network error
                print("API unavailable")
                count_failed += 1
            except sr.UnknownValueError:  # Can't convert speech to text
                print("Unable to recognize speech")
                playsound("data/audio_data/repeat.mp3")
                count_failed += 1
            if count_failed >= 5:
                break
            time.sleep(0.2)
        engine.stop()
