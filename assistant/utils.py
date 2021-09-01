from playsound import playsound
import os
from fuzzywuzzy import fuzz
from gtts import gTTS


def text_to_speech(text, lang='vi', path='tmp.mp3'):
    tts = gTTS(text, lang=lang)
    tts.save(path)


def hello():
    playsound('audio/hello.mp3')


def cant_hear():
    playsound('audio/cant_hear.mp3')


def wait():
    playsound('audio/wait.mp3')


def dont_know():
    playsound('audio/dont_know.mp3')


def knowledge():
    playsound('audio/knowledge.mp3')


def me():
    playsound('audio/me.mp3')


def good_bye():
    playsound('audio/good_bye.mp3')


def change_question():
    playsound('audio/change_question.mp3')


def answer(q_num: int):
    if os.path.exists(f'audio/answer_{q_num}.mp3'):
        playsound(f'audio/answer_{q_num}.mp3')
    else:
        dont_know()


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
