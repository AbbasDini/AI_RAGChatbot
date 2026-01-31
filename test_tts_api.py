#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست مستقیم API TTS
"""

import requests
import json

def test_tts_api():
    """تست API TTS"""
    print("=== تست مستقیم API TTS ===")
    
    # URL سرور
    base_url = "http://localhost:5000"
    
    # تست 1: درخواست TTS
    print("\n🎵 تست 1: درخواست TTS")
    try:
        response = requests.post(
            f"{base_url}/api/tts",
            headers={'Content-Type': 'application/json'},
            json={
                'text': 'سلام، من دستیار هوشمند پزشکی هستم',
                'provider': 'avalai',
                'voice': 'alloy'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {response.headers.get('content-length')}")
        
        if response.status_code == 200:
            # ذخیره فایل صوتی
            with open('test_api_output.mp3', 'wb') as f:
                f.write(response.content)
            print("✅ فایل صوتی ذخیره شد: test_api_output.mp3")
            print(f"حجم فایل: {len(response.content)} bytes")
        else:
            print(f"❌ خطا: {response.text}")
            
    except Exception as e:
        print(f"❌ خطا در تست 1: {e}")
    
    # تست 2: دریافت صداهای موجود
    print("\n🎵 تست 2: دریافت صداهای موجود")
    try:
        response = requests.get(f"{base_url}/api/tts/voices")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            voices = response.json()
            print("✅ صداهای موجود:")
            for provider, voice_list in voices.items():
                print(f"  {provider}: {len(voice_list)} صدا")
                for voice in voice_list[:3]:  # فقط 3 صدا اول
                    print(f"    - {voice}")
        else:
            print(f"❌ خطا: {response.text}")
            
    except Exception as e:
        print(f"❌ خطا در تست 2: {e}")
    
    # تست 3: تست TTS
    print("\n🎵 تست 3: تست TTS")
    try:
        response = requests.get(f"{base_url}/api/tts/test")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print("✅ نتایج تست:")
            for provider, result in results.items():
                status = result.get('status', 'unknown')
                error = result.get('error', '')
                print(f"  {provider}: {status}")
                if error:
                    print(f"    خطا: {error}")
        else:
            print(f"❌ خطا: {response.text}")
            
    except Exception as e:
        print(f"❌ خطا در تست 3: {e}")

if __name__ == "__main__":
    test_tts_api() 