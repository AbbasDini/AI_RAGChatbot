#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست اختصاصی TTS آولای
"""

import os
from dotenv import load_dotenv
from advanced_tts import AdvancedTTS

def test_avalai_tts():
    """تست TTS آولای"""
    print("=== تست TTS آولای ===")
    
    # Load environment variables
    load_dotenv()
    
    # Check AvalAI API key
    avalai_key = os.getenv('AVALAI_API_KEY')
    if not avalai_key:
        print("❌ کلید API آولای یافت نشد!")
        print("لطفاً AVALAI_API_KEY را در فایل .env تنظیم کنید.")
        return False
    
    print(f"✅ کلید API آولای موجود است: {avalai_key[:10]}...")
    
    # Initialize TTS
    try:
        tts = AdvancedTTS()
        print("✅ TTS با موفقیت راه‌اندازی شد")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی TTS: {e}")
        return False
    
    # Test different models and voices
    test_text = "سلام، من دستیار هوشمند پزشکی هستم. چگونه می‌توانم به شما کمک کنم؟"
    
    models = [
        ("tts-1", "alloy"),
        ("tts-1-hd", "nova"),
        ("gpt-4o-mini-tts", "echo"),
        ("gemini-2.5-pro-preview-tts", "shimmer")
    ]
    
    voices = [
        "alloy", "ash", "ballad", "coral", "echo", 
        "fable", "onyx", "nova", "sage", "shimmer", "verse"
    ]
    
    print(f"\n🎵 تست مدل‌های مختلف:")
    for model, voice in models:
        try:
            print(f"  تست مدل {model} با صدا {voice}...")
            audio_data = tts.text_to_speech_avalai(test_text, voice, model)
            if audio_data:
                filename = f"test_avalai_{model}_{voice}.mp3"
                tts.save_audio_file(audio_data, filename)
                print(f"    ✅ موفق - فایل ذخیره شد: {filename}")
            else:
                print(f"    ❌ ناموفق")
        except Exception as e:
            print(f"    ❌ خطا: {e}")
    
    print(f"\n🎵 تست صداهای مختلف:")
    for voice in voices[:3]:  # فقط 3 صدا اول
        try:
            print(f"  تست صدا {voice}...")
            audio_data = tts.text_to_speech_avalai(test_text, voice, "tts-1")
            if audio_data:
                filename = f"test_avalai_voice_{voice}.mp3"
                tts.save_audio_file(audio_data, filename)
                print(f"    ✅ موفق - فایل ذخیره شد: {filename}")
            else:
                print(f"    ❌ ناموفق")
        except Exception as e:
            print(f"    ❌ خطا: {e}")
    
    # Test with Persian medical text
    medical_text = "بیمار باید روزانه دو بار قرص آسپرین 100 میلی‌گرمی مصرف کند."
    print(f"\n🏥 تست متن پزشکی:")
    try:
        audio_data = tts.text_to_speech_avalai(medical_text, "alloy", "tts-1")
        if audio_data:
            filename = "test_avalai_medical.mp3"
            tts.save_audio_file(audio_data, filename)
            print(f"  ✅ موفق - فایل ذخیره شد: {filename}")
        else:
            print(f"  ❌ ناموفق")
    except Exception as e:
        print(f"  ❌ خطا: {e}")
    
    # Test auto provider selection
    print(f"\n🤖 تست انتخاب خودکار ارائه‌دهنده:")
    try:
        audio_data = tts.synthesize_speech(test_text)  # بدون مشخص کردن provider
        if audio_data:
            filename = "test_avalai_auto.mp3"
            tts.save_audio_file(audio_data, filename)
            print(f"  ✅ موفق - فایل ذخیره شد: {filename}")
        else:
            print(f"  ❌ ناموفق")
    except Exception as e:
        print(f"  ❌ خطا: {e}")
    
    return True

if __name__ == "__main__":
    success = test_avalai_tts()
    if success:
        print("\n🎉 تست TTS آولای با موفقیت انجام شد!")
        print("فایل‌های صوتی در پوشه tts_cache ذخیره شده‌اند.")
    else:
        print("\n❌ تست TTS آولای ناموفق بود!") 