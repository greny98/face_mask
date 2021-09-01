import speech_recognition as sr
from assistant import utils
import time
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    questions = utils.load_questions()
    answers = utils.load_answers()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # loc nhieu
        is_communicate = True
        count_failed = 0
        utils.hello()
        while is_communicate:
            utils.knowledge()
            print("Listening...")
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)
            try:
                print('Waiting...')
                utils.wait()
                ques = recognizer.recognize_google(audio, language='vi')
                print("Question: ", ques)
                ques_num = utils.find_question_num(ques, questions)
                print("Question num: ", ques_num)
                if ques_num != -1:
                    print("Answer: ", answers[ques_num])
                utils.answer(ques_num)
                utils.change_question()
                print("Listening...")
                audio = recognizer.listen(source)
                next = recognizer.recognize_google(audio, language='vi')
                next = utils.remove_accents(next.lower())
                if (fuzz.ratio(next, 'khong') >= 70 or
                    fuzz.ratio(next, 'thoi') >= 70 or
                    fuzz.ratio(next, 'toi khong nhe') >= 70):
                    utils.good_bye()
                    break
            except sr.RequestError:  # Service/network error
                print("API unavailable")
                count_failed += 1
            except sr.UnknownValueError:  # Can't convert speech to text
                print("Unable to recognize speech")
                utils.cant_hear()
                count_failed += 1
            if count_failed >= 5:
                break
            time.sleep(0.2)
