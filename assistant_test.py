from assistant import process
import pyttsx3

engine = pyttsx3.init()

if __name__ == '__main__':
    process.run(engine)
