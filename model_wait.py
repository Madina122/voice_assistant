import sounddevice as sd
import torch
import time
import re
import logging

# константы голосов, поддерживаемых в silero
SPEAKER_AIDAR   = "aidar"
SPEAKER_BAYA    = "baya"
SPEAKER_KSENIYA = "kseniya"
SPEAKER_XENIA   = "xenia"
SPEAKER_RANDOM  = "random"

# константы девайсов для работы torch
DEVICE_CPU    = "cpu"
DEVICE_CUDA   = "cuda" 
DEVICE_VULKAN = "vulkan"
DEVICE_OPENGL = "opengl"
DEVICE_OPENCL = "opencl"

logging.basicConfig(level=logging.INFO)

class TTS:
    def __init__(
            self, speaker: str = SPEAKER_BAYA, 
            device: str        = DEVICE_CPU, 
            samplerate: int    = 48_000
        ):
        
        # подгружаем модель 
        self.__MODEL__, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="ru_v3"
        )
        self.__MODEL__.to(torch.device(device))

        self.__SPEAKER__ = speaker
        self.__SAMPLERATE__ = samplerate

    def clean_text(self, text: str) -> str:
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text
    
    def text2speech(self, text: str):
        cleaned_text = self.clean_text(text)

        if not cleaned_text.strip():
            return
        try:
            audio = self.__MODEL__.apply_tts(
                text=text,               
                speaker=self.__SPEAKER__,
                sample_rate=self.__SAMPLERATE__, 
                put_accent=True,
                put_yo=True
            )

            # проигрываем то что получилось
            sd.play(audio, samplerate=self.__SAMPLERATE__)
            time.sleep((len(audio)/self.__SAMPLERATE__))
            sd.stop()
        except Exception as e:
            logging.error(f"Ошибка в TTS: {e}")