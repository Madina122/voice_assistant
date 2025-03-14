import sounddevice as sd
import vosk
import sys
import queue
import json

class STT:
    def __init__(self, modelpath: str = "vosk-model", samplerate: int = 16000):
        self.__REC__ = vosk.KaldiRecognizer(vosk.Model(modelpath), samplerate)
        self.__Q__ = queue.Queue()
        self.__SAMPLERATE__ = samplerate
        self.__STREAM__=None
        self.__listening__=None
    
    def q_callback(self, indata, _, __, status):
        if status:
            print(status, file=sys.stderr)
        self.__Q__.put(bytes(indata))

    def start_listening(self, executor: callable):
        if not self.__listening__: 
            self.__STREAM__ = sd.RawInputStream(
                samplerate=self.__SAMPLERATE__,
                blocksize=8000,
                device=1,
                dtype='int16',
                channels=1,
                callback=self.q_callback
            )
            self.__STREAM__.start()
            self.__listening__ = True
            print("Start listening...")
        
        
        while self.__listening__:
            data = self.__Q__.get()
            if self.__REC__.AcceptWaveform(data):
                text = json.loads(self.__REC__.Result())["text"]
                if text.strip(): 
                    executor(text)

    def stop_listening(self):
        if self.__listening__:
            self.__STREAM__.stop()
            self.__STREAM__.close()
            self.__listening__ = False
            print("Stop listening...")