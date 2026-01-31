#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ماژول پیشرفته تبدیل متن به صدا با استفاده از بهترین مدل‌های LLM
Advanced Text-to-Speech using best LLM models for Persian
"""

import os
import requests
import json
import base64
import tempfile
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTTS:
    """کلاس پیشرفته تبدیل متن به صدا با استفاده از مدل‌های LLM"""
    
    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.cache_dir = Path("./tts_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def _load_api_keys(self) -> Dict[str, str]:
        """بارگذاری کلیدهای API از متغیرهای محیطی"""
        return {
            'openai': os.getenv('OPENAI_API_KEY'),
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY'),
            'coqui': os.getenv('COQUI_API_KEY'),
            'azure': os.getenv('AZURE_SPEECH_KEY'),
            'google': os.getenv('GOOGLE_CLOUD_API_KEY'),
            'avalai': os.getenv('AVALAI_API_KEY')
        }
    
    def text_to_speech_openai(self, text: str, voice: str = "alloy") -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از OpenAI TTS
        بهترین کیفیت برای زبان‌های مختلف
        """
        if not self.api_keys['openai']:
            logger.warning("OpenAI API key not found")
            return None
            
        try:
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {self.api_keys['openai']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "tts-1",  # یا tts-1-hd برای کیفیت بالاتر
                "input": text,
                "voice": voice,  # alloy, echo, fable, onyx, nova, shimmer
                "response_format": "mp3",
                "speed": 1.0
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            logger.info(f"OpenAI TTS successful for voice: {voice}")
            return response.content
            
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            return None
    
    def text_to_speech_elevenlabs(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از ElevenLabs
        بهترین کیفیت و صداهای طبیعی
        """
        if not self.api_keys['elevenlabs']:
            logger.warning("ElevenLabs API key not found")
            return None
            
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_keys['elevenlabs']
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",  # بهترین مدل برای چندزبانه
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            logger.info(f"ElevenLabs TTS successful for voice: {voice_id}")
            return response.content
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None
    
    def text_to_speech_azure(self, text: str, voice: str = "fa-IR-DariushNeural") -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از Azure Cognitive Services
        بهترین پشتیبانی از زبان فارسی
        """
        if not self.api_keys['azure']:
            logger.warning("Azure Speech API key not found")
            return None
            
        try:
            url = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_keys['azure'],
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
            }
            
            # SSML برای کنترل بهتر صدا
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
                   xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="fa-IR">
                <voice name="{voice}">
                    <mstts:express-as style="general" rate="0.9" pitch="0%">
                        {text}
                    </mstts:express-as>
                </voice>
            </speak>
            """
            
            response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
            response.raise_for_status()
            
            logger.info(f"Azure TTS successful for voice: {voice}")
            return response.content
            
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            return None
    
    def text_to_speech_google(self, text: str, voice: str = "fa-IR-Standard-A") -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از Google Cloud Text-to-Speech
        کیفیت بالا و پشتیبانی خوب از فارسی
        """
        if not self.api_keys['google']:
            logger.warning("Google Cloud API key not found")
            return None
            
        try:
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.api_keys['google']}"
            
            data = {
                "input": {"text": text},
                "voice": {
                    "languageCode": "fa-IR",
                    "name": voice,
                    "ssmlGender": "MALE"
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "speakingRate": 0.9,
                    "pitch": 0.0,
                    "volumeGainDb": 0.0
                }
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            # Decode base64 audio content
            audio_content = base64.b64decode(response.json()['audioContent'])
            
            logger.info(f"Google TTS successful for voice: {voice}")
            return audio_content
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None
    
    def text_to_speech_coqui(self, text: str, voice: str = "persian_female") -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از Coqui TTS
        مدل‌های متن‌باز با کیفیت بالا
        """
        try:
            # استفاده از Coqui TTS API یا مدل محلی
            url = "https://api.coqui.ai/v1/tts"
            headers = {
                "Authorization": f"Bearer {self.api_keys.get('coqui', '')}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "voice_id": voice,
                "model_id": "tts_models/multilingual/multi-dataset/xtts_v2"
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Coqui TTS successful for voice: {voice}")
            return response.content
            
        except Exception as e:
            logger.error(f"Coqui TTS error: {e}")
            return None
    
    def text_to_speech_avalai(self, text: str, voice: str = "alloy", model: str = "tts-1", instructions: str = None) -> Optional[bytes]:
        """
        تبدیل متن به صدا با استفاده از AvalAI TTS
        بهترین کیفیت و پشتیبانی از زبان فارسی
        """
        if not self.api_keys['avalai']:
            logger.warning("AvalAI API key not found")
            return None
            
        try:
            url = "https://api.avalai.ir/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {self.api_keys['avalai']}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,  # tts-1, tts-1-hd, gpt-4o-mini-tts, gemini-2.5-pro-preview-tts
                "input": text,
                "voice": voice,  # alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse
                "response_format": "mp3",
                "speed": 1.0
            }
            # اضافه کردن دستورالعمل برای مدل‌های Gemini TTS
            if model.startswith("gemini"):
                data["instructions"] = instructions or "با لهجه فارسی ایرانی و تلفظ صحیح کلمات پزشکی صحبت کنید."
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"AvalAI TTS successful for voice: {voice}, model: {model}")
            return response.content
        except Exception as e:
            logger.error(f"AvalAI TTS error: {e}")
            return None
    
    def get_best_tts_provider(self, text: str, language: str = "fa-IR") -> str:
        """انتخاب بهترین ارائه‌دهنده TTS بر اساس زبان و کیفیت"""
        
        providers = []
        
        # اولویت اول: AvalAI (سرویس داخلی ایران)
        if self.api_keys['avalai']:
            providers.append(('avalai', 15))  # بالاترین اولویت
        
        # اولویت بر اساس کیفیت و پشتیبانی از فارسی
        if self.api_keys['azure']:
            providers.append(('azure', 10))  # بهترین پشتیبانی از فارسی
        
        if self.api_keys['elevenlabs']:
            providers.append(('elevenlabs', 9))  # کیفیت بسیار بالا
        
        if self.api_keys['google']:
            providers.append(('google', 8))  # پشتیبانی خوب از فارسی
        
        if self.api_keys['openai']:
            providers.append(('openai', 7))  # کیفیت بالا
        
        if self.api_keys['coqui']:
            providers.append(('coqui', 6))  # متن‌باز
        
        # انتخاب بهترین ارائه‌دهنده
        if providers:
            providers.sort(key=lambda x: x[1], reverse=True)
            return providers[0][0]
        
        return 'browser'  # استفاده از Web Speech API مرورگر
    
    def synthesize_speech(self, text: str, provider: str = None, voice: str = None) -> Optional[bytes]:
        """
        تبدیل متن به صدا با بهترین ارائه‌دهنده
        """
        if provider == 'auto' or not provider:
            provider = self.get_best_tts_provider(text)
        
        logger.info(f"Using TTS provider: {provider}")
        
        if provider == 'avalai':
            return self.text_to_speech_avalai(text, voice or "alloy", "tts-1")
        elif provider == 'azure':
            return self.text_to_speech_azure(text, voice or "fa-IR-DariushNeural")
        elif provider == 'elevenlabs':
            return self.text_to_speech_elevenlabs(text, voice or "21m00Tcm4TlvDq8ikWAM")
        elif provider == 'google':
            return self.text_to_speech_google(text, voice or "fa-IR-Standard-A")
        elif provider == 'openai':
            return self.text_to_speech_openai(text, voice or "alloy")
        elif provider == 'coqui':
            return self.text_to_speech_coqui(text, voice or "persian_female")
        else:
            logger.warning("No TTS provider available, using browser fallback")
            return None
    
    def save_audio_file(self, audio_data: bytes, filename: str) -> str:
        """ذخیره فایل صوتی"""
        file_path = self.cache_dir / filename
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        return str(file_path)
    
    def get_available_voices(self) -> Dict[str, list]:
        """دریافت لیست صداهای موجود"""
        voices = {
            'avalai': [
                'alloy',    # مرد - طبیعی
                'ash',      # مرد - گرم
                'ballad',   # زن - ملایم
                'coral',    # زن - روشن
                'echo',     # مرد - گرم
                'fable',    # مرد - جوان
                'onyx',     # مرد - بالغ
                'nova',     # زن - طبیعی
                'sage',     # مرد - خردمند
                'shimmer',  # زن - جوان
                'verse'     # زن - شاعرانه
            ],
            'azure': [
                'fa-IR-DariushNeural',  # مرد - تهران
                'fa-IR-FaridNeural',    # مرد - تهران
                'fa-IR-SaraNeural',     # زن - تهران
                'fa-IR-YektaNeural'     # زن - تهران
            ],
            'google': [
                'fa-IR-Standard-A',     # مرد
                'fa-IR-Standard-B',     # زن
                'fa-IR-Wavenet-A',      # مرد - کیفیت بالا
                'fa-IR-Wavenet-B'       # زن - کیفیت بالا
            ],
            'openai': [
                'alloy',    # مرد - طبیعی
                'echo',     # مرد - گرم
                'fable',    # مرد - جوان
                'onyx',     # مرد - بالغ
                'nova',     # زن - طبیعی
                'shimmer'   # زن - جوان
            ],
            'elevenlabs': [
                '21m00Tcm4TlvDq8ikWAM',  # Rachel - زن
                'AZnzlk1XvdvUeBnXmlld',  # Domi - زن
                'EXAVITQu4vr4xnSDxMaL',  # Bella - زن
                'ErXwobaYiN019PkySvjV',  # Antoni - مرد
                'VR6AewLTigWG4xSOukaG',  # Josh - مرد
                'pNInz6obpgDQGcFmaJgB'    # Adam - مرد
            ]
        }
        return voices

# تست ماژول
if __name__ == "__main__":
    tts = AdvancedTTS()
    
    # تست متن فارسی
    test_text = "سلام، من دستیار هوشمند پزشکی هستم. چگونه می‌توانم به شما کمک کنم؟"
    
    # تست با AvalAI (اولویت اول)
    audio_data = tts.synthesize_speech(test_text, 'avalai')
    if audio_data:
        tts.save_audio_file(audio_data, "test_avalai.mp3")
        print("✅ AvalAI TTS test successful")
    else:
        print("❌ AvalAI TTS test failed")
    
    # تست با Azure (بهترین برای فارسی)
    audio_data = tts.synthesize_speech(test_text, 'azure')
    if audio_data:
        tts.save_audio_file(audio_data, "test_azure.mp3")
        print("✅ Azure TTS test successful")
    
    # تست با ElevenLabs
    audio_data = tts.synthesize_speech(test_text, 'elevenlabs')
    if audio_data:
        tts.save_audio_file(audio_data, "test_elevenlabs.mp3")
        print("✅ ElevenLabs TTS test successful")
    
    # نمایش صداهای موجود
    voices = tts.get_available_voices()
    print("\n📋 Available voices:")
    for provider, voice_list in voices.items():
        print(f"\n{provider.upper()}:")
        for voice in voice_list:
            print(f"  - {voice}") 