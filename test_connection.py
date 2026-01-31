#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت تست اتصال به Hugging Face و ارائه راه‌حل‌های جایگزین
"""

import os
import sys
import requests
import subprocess
from pathlib import Path

def test_basic_connection():
    """تست اتصال پایه به Hugging Face"""
    print("🔍 تست اتصال به Hugging Face...")
    
    try:
        response = requests.get('https://huggingface.co', timeout=10)
        if response.status_code == 200:
            print("✅ اتصال به Hugging Face موفق است")
            return True
        else:
            print(f"❌ خطای HTTP: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ خطای اتصال: {e}")
        return False
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        return False

def test_dns_resolution():
    """تست حل DNS"""
    print("\n🔍 تست حل DNS...")
    
    try:
        import socket
        ip = socket.gethostbyname('huggingface.co')
        print(f"✅ DNS حل شد: {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ خطای DNS: {e}")
        return False

def check_cache_directory():
    """بررسی پوشه cache"""
    print("\n📁 بررسی پوشه cache...")
    
    cache_path = Path.home() / '.cache' / 'huggingface'
    if cache_path.exists():
        print(f"✅ پوشه cache موجود: {cache_path}")
        
        # بررسی مدل‌های موجود
        hub_path = cache_path / 'hub'
        if hub_path.exists():
            models = list(hub_path.glob('*'))
            print(f"📦 تعداد مدل‌های موجود: {len(models)}")
            for model in models[:5]:  # نمایش 5 مدل اول
                print(f"   - {model.name}")
        return True
    else:
        print(f"❌ پوشه cache موجود نیست: {cache_path}")
        return False

def test_alternative_models():
    """تست مدل‌های جایگزین"""
    print("\n🔧 تست مدل‌های جایگزین...")
    
    alternative_models = [
        "paraphrase-multilingual-MiniLM-L12-v2",
        "distiluse-base-multilingual-cased-v2",
        "sentence-transformers/all-mpnet-base-v2",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ]
    
    working_models = []
    
    for model_name in alternative_models:
        try:
            print(f"  تست {model_name}...")
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(model_name)
            print(f"  ✅ {model_name} کار می‌کند")
            working_models.append(model_name)
        except Exception as e:
            print(f"  ❌ {model_name}: {str(e)[:50]}...")
    
    return working_models

def suggest_solutions():
    """پیشنهاد راه‌حل‌ها"""
    print("\n💡 راه‌حل‌های پیشنهادی:")
    
    solutions = [
        "1. استفاده از VPN معتبر",
        "2. تغییر DNS به 8.8.8.8 و 8.8.4.4",
        "3. دانلود دستی مدل از Hugging Face",
        "4. استفاده از مدل‌های جایگزین موجود",
        "5. تنظیم proxy (اگر در دسترس است)",
        "6. استفاده از mirror sites",
        "7. انتظار برای حل مشکل شبکه"
    ]
    
    for solution in solutions:
        print(f"   {solution}")

def create_offline_config():
    """ایجاد تنظیمات آفلاین"""
    print("\n⚙️ ایجاد تنظیمات آفلاین...")
    
    config_content = """
# تنظیمات آفلاین برای Hugging Face
import os

# تنظیم حالت آفلاین
os.environ['HF_OFFLINE'] = '1'

# تنظیم مسیر cache
os.environ['HF_HOME'] = './models'

# تنظیم timeout بیشتر
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'
"""
    
    config_file = Path('offline_config.py')
    config_file.write_text(config_content, encoding='utf-8')
    print(f"✅ فایل تنظیمات آفلاین ایجاد شد: {config_file}")

def main():
    """تابع اصلی"""
    print("🚀 شروع تست اتصال Hugging Face")
    print("=" * 50)
    
    # تست‌های مختلف
    connection_ok = test_basic_connection()
    dns_ok = test_dns_resolution()
    cache_ok = check_cache_directory()
    
    print("\n" + "=" * 50)
    print("📊 خلاصه نتایج:")
    print(f"   اتصال پایه: {'✅' if connection_ok else '❌'}")
    print(f"   حل DNS: {'✅' if dns_ok else '❌'}")
    print(f"   پوشه cache: {'✅' if cache_ok else '❌'}")
    
    if not connection_ok:
        print("\n❌ مشکل اتصال شناسایی شد!")
        suggest_solutions()
        
        # تست مدل‌های جایگزین
        working_models = test_alternative_models()
        if working_models:
            print(f"\n✅ مدل‌های جایگزین کار می‌کنند: {working_models}")
        else:
            print("\n❌ هیچ مدل جایگزینی کار نمی‌کند")
        
        # ایجاد تنظیمات آفلاین
        create_offline_config()
        
        print("\n🔧 برای استفاده از تنظیمات آفلاین:")
        print("   در ابتدای کد خود این خط را اضافه کنید:")
        print("   from offline_config import *")
        
    else:
        print("\n✅ همه چیز درست کار می‌کند!")
        print("   می‌توانید از مدل all-MiniLM-L6-v2 استفاده کنید")

if __name__ == "__main__":
    main() 