#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست وضعیت TTS و کلیدهای API
"""

import os
from dotenv import load_dotenv
from advanced_tts import AdvancedTTS

def test_tts_status():
    """تست وضعیت TTS"""
    print("=== تست وضعیت TTS ===")
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    print("\n📋 بررسی متغیرهای محیطی:")
    env_vars = {
        'AVALAI_API_KEY': os.getenv('AVALAI_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY'),
        'AZURE_SPEECH_KEY': os.getenv('AZURE_SPEECH_KEY'),
        'GOOGLE_CLOUD_API_KEY': os.getenv('GOOGLE_CLOUD_API_KEY'),
        'COQUI_API_KEY': os.getenv('COQUI_API_KEY')
    }
    
    for key, value in env_vars.items():
        status = "✅ موجود" if value else "❌ موجود نیست"
        print(f"  {key}: {status}")
    
    # Initialize TTS
    print("\n🔧 راه‌اندازی TTS:")
    try:
        tts = AdvancedTTS()
        print("  ✅ TTS با موفقیت راه‌اندازی شد")
        
        # Check API keys in TTS
        print("\n📋 کلیدهای API در TTS:")
        for provider, key in tts.api_keys.items():
            status = "✅ موجود" if key else "❌ موجود نیست"
            print(f"  {provider}: {status}")
        
        # Test basic functionality
        print("\n🧪 تست عملکرد پایه:")
        voices = tts.get_available_voices()
        print(f"  ✅ صداهای موجود: {len(voices)} ارائه‌دهنده")
        
        # Test synthesis with fallback
        test_text = "سلام، این یک تست است."
        print(f"\n🎵 تست تبدیل متن به صدا:")
        print(f"  متن: {test_text}")
        
        # Try different providers
        providers = ['avalai', 'azure', 'elevenlabs', 'google', 'openai']
        for provider in providers:
            if tts.api_keys.get(provider):
                try:
                    audio_data = tts.synthesize_speech(test_text, provider)
                    if audio_data:
                        print(f"  ✅ {provider}: موفق")
                    else:
                        print(f"  ❌ {provider}: ناموفق")
                except Exception as e:
                    print(f"  ❌ {provider}: خطا - {e}")
            else:
                print(f"  ⚠️ {provider}: کلید API موجود نیست")
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطا در راه‌اندازی TTS: {e}")
        return False

if __name__ == "__main__":
    success = test_tts_status()
    if success:
        print("\n🎉 تست TTS با موفقیت انجام شد!")
    else:
        print("\n❌ تست TTS ناموفق بود!") 