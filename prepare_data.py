from gtts import gTTS
from playsound import playsound
import time


def read_file(file_path):
    """
    Read file Answer.txt and return list answer
    :param file_path:
    :return:
    """
    with open(file_path, mode='r', encoding='utf16') as fp:
        contents = fp.read()
        list_answers = contents.split('\n')
        return list_answers


def cvt_text_to_speech(text, lang='vi', out_file='tmp.mp3'):
    """
    Convert text -> speech and save to audio file
    :param text:
    :param lang:
    :param out_file:
    :return:
    """
    obj = gTTS(text, lang=lang)
    obj.save(out_file)


def run_audio(file_path):
    """
    Run audio file to test result
    :param file_path:
    :return:
    """
    playsound(file_path)


if __name__ == '__main__':
    answers = read_file('data/Answer.txt')
    for i, answer in enumerate(answers):
        path = f"audio_test/answer_{i}.mp3"
        cvt_text_to_speech(answer, lang='en-US', out_file=path)
        time.sleep(2.)
