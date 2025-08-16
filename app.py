'''
Голосовой ассистент "Соната" - помощник в управлении Яндекс.Музыкой

Требуется:
pip install vosk
pip install sounddevice
pip install scikit-learn
pip install pyttsx3
Языковая модель vosk (уже есть в проекте)
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk
import json
import queue
import words
from skills import *
import pyttsx3	

q = queue.Queue()

model = vosk.Model('vosk_model_small')                                          #голосовую модель vosk из папка с файлами проекта

device = sd.default.device                                                      # устройство вывода (микрофон)
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])    # частота микрофона

 # Отвечает за распознование речи
def callback(indata, frames, time, status):
    q.put(bytes(indata))

# Отвечает за воспроизведение голоса Сонаты
def speaker(text):
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say(text)
	engine.runAndWait()

# Отвечает за анализ распознанной речи
def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS.intersection(data.split())                 # проверяем есть ли имя бота в data, если нет, то return
    if not trg:
        return

    data.replace(list(trg)[0], '')                                  # удаляем имя асистента из полученного текста
    text_vector = vectorizer.transform([data]).toarray()[0]         # получаем вектор полученного текста
    answer = clf.predict([text_vector])[0]                          # сравниваем с вариантами, получая наиболее подходящий ответ
    func_name = answer.split()[0]                                   # получение имени функции из ответа из модели data_set
    speaker(answer.replace(func_name, ''))                          # озвучка ответа Сонаты из модели data_set
    exec(func_name + '()')                                          # запуск функции из skills


# Отвечает за обучение и анализ распознанной речи
def main():

    vectorizer = CountVectorizer()                                   # обучение матрицы на data_set модели
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))
    
    del words.data_set

    
    
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',channels=1, callback=callback):   # постоянно слушаем микрофон
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
    


if __name__ == '__main__':
    main()

