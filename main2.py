from fuzzywuzzy import fuzz

from model_wait import TTS
from model_record import STT

commandsList = []

def equ(text, needed):
    return fuzz.ratio(text, needed) >= 70

def execute(text: str):
    print(f"> {text}")
    
    if equ(text, "расскажи анекдот"):
        text = "какой то анекдот!"
        tts.text2speech(text)
        print(f"- {text}")
    
    elif equ(text, "что ты умеешь"):
        text = "я умею всё, чему ты мен+я науч+ил!"
        tts.text2speech(text)
        print(f"- {text}")
    
    elif equ(text, "выключи"):
        text = "надеюсь, я не стану про+ектом, кот+орый ты забр+осишь!"
        tts.text2speech(text)
        print(f"- {text}")
        raise SystemExit

tts = TTS()
stt = STT(modelpath="vosk-model")

print("listen...")
stt.listen(execute)