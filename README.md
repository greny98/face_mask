# 1. Library
- `gtts`: Convert Text to Speech
- `SpeechRecognition`: Convert Speech to Text
- `fuzzywuzzy`: Calculate the similarity of two text
- `playsound`: Open audio file in app

# 2. Processing
## 2.1. Preparing questions and answers
- Prepare questions and corresponding answers for each question.
- **Questions** in `Question.txt` and **Answers** in `Answer.txt`
- Each question and each answer is only on one line
- We will use the library `gtts` to create a **voice file** for each answer. Moreover, We will also create voice files for greetings and goodbyes
## 2.2. Start up
- Read all questions from the file `Question.txt`. Since each question is only on one line, we will separate the content by a newline character `\n`.
- Open greetings voice file
- Start microphone and filter noise
## 2.3. Communicating with visitors
- Visitor asks and the system will record the sound through the **Microphone**
- Use library `SpeechRecognition` to convert **audio** to **text**
- For each question in the list, we use the library `fuzzywuzzy` to calculate the similarity to the visitor's question.
- Find the question with the highest similarity.
    - If this similarity is less than 70% then we will conclude that none of the questions in the list match and open audio file to say "I don't know"
    - Otherwise we will open the audio file of the corresponding answer
- Ask if the visitor wants to know any other information, otherwise will open the audio file goodbye, otherwise will return to the first step