from gtts import gTTS

if __name__ == '__main__':
    text = "Bạn có thể nhắc lại không?"
    tts = gTTS(text, lang='vi')
    tts.save("repeat.mp3")
