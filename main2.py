from fuzzywuzzy import fuzz

from model_wait import TTS
from model_record import STT
from сhat_gpt import LLM

commandsList = []

def equ(text, needed):
    return fuzz.ratio(text, needed) >= 70

def execute(text: str):
    print(f"> {text}")

    if equ(text, "расскажи анекдот"):
        text = "какой то анекдот!"
        stt.stop_listening() 
        tts.text2speech(text)
        print(f"- {text}")
        stt.start_listening(execute) 
    
    elif equ(text, "что ты умеешь"):
        text = "я умею всё, чему ты мен+я науч+ил!"
        stt.stop_listening() 
        tts.text2speech(text)
        print(f"- {text}")
        stt.start_listening(execute) 
    
    elif equ(text, "выключи"):
        text = "надеюсь, я не стану про+ектом, кот+орый ты забр+осишь!"
        stt.stop_listening()  
        tts.text2speech(text)
        print(f"- {text}")
        raise SystemExit
    
    else:
        stt.stop_listening()  
        answer = llm.llm_work(text)
        tts.text2speech(answer)
        print(f"- {answer}")
        stt.start_listening(execute)  

tts = TTS()
stt = STT(modelpath="vosk-model")
llm = LLM()

print("listen...")
stt.start_listening(execute)
