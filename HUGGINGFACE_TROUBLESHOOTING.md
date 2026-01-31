# راهنمای حل مشکل اتصال به Hugging Face

## مشکل
خطای اتصال به Hugging Face هنگام دانلود مدل `all-MiniLM-L6-v2`:
```
requests.exceptions.ConnectionError: (MaxRetryError('HTTPSConnectionPool(host='huggingface.co', port=443): Max retries exceeded with url: /api/models/sentence-transformers/all-MiniLM-L6-v2/tree/main/additional_chat_templates?recursive=False&expand=False (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x000001A01DFF6210>: Failed to resolve 'huggingface.co' ([Errno 11001] getaddrinfo failed)"))'), '(Request ID: 6f959cc4-ce98-40e5-bc89-affc797b264d)')
```

## راه‌حل‌های پیشنهادی

### 1. استفاده از VPN
- از VPN معتبر استفاده کنید
- مطمئن شوید که VPN به درستی کار می‌کند
- آدرس‌های IP مختلف را امتحان کنید

### 2. تغییر DNS
```bash
# در Windows
# تنظیمات شبکه -> تغییر آداپتور -> Properties -> IPv4 -> Properties
# DNS: 8.8.8.8 و 8.8.4.4

# در Linux/Mac
sudo nano /etc/resolv.conf
# اضافه کردن:
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### 3. دانلود دستی مدل
```bash
# نصب git-lfs
git lfs install

# کلون کردن repository
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# کپی کردن مدل به پوشه cache
# Windows:
copy all-MiniLM-L6-v2 C:\Users\[USERNAME]\.cache\huggingface\hub\

# Linux/Mac:
cp -r all-MiniLM-L6-v2 ~/.cache/huggingface/hub/
```

### 4. استفاده از مدل‌های جایگزین
کد اصلاح شده در `app.py` حالا مدل‌های جایگزین را امتحان می‌کند:
- `paraphrase-multilingual-MiniLM-L12-v2`
- `distiluse-base-multilingual-cased-v2`
- `sentence-transformers/all-mpnet-base-v2`

### 5. تنظیم Proxy
```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy:port'
os.environ['HTTPS_PROXY'] = 'http://proxy:port'
```

### 6. استفاده از Mirror Sites
```python
# تنظیم mirror site
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

### 7. دانلود آفلاین
```bash
# دانلود مدل با wget یا curl
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/pytorch_model.bin
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/config.json
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer.json
```

### 8. استفاده از مدل‌های محلی
اگر مدل‌های دیگر در سیستم موجود هستند:
```python
# بررسی مدل‌های موجود
from sentence_transformers import SentenceTransformer
available_models = SentenceTransformer.list_models()
print(available_models)
```

## تست اتصال
```python
import requests
try:
    response = requests.get('https://huggingface.co', timeout=10)
    print("اتصال موفق")
except Exception as e:
    print(f"خطای اتصال: {e}")
```

## نکات مهم
1. **Cache**: مدل‌های دانلود شده در `~/.cache/huggingface/` ذخیره می‌شوند
2. **Offline Mode**: می‌توانید از حالت آفلاین استفاده کنید
3. **Alternative Models**: مدل‌های جایگزین ممکن است عملکرد مشابهی داشته باشند
4. **Network Issues**: مشکلات شبکه موقت ممکن است حل شوند

## درخواست کمک
اگر هیچ‌کدام از راه‌حل‌ها کار نکرد:
1. وضعیت شبکه خود را بررسی کنید
2. از VPN معتبر استفاده کنید
3. با پشتیبانی شبکه تماس بگیرید
4. از مدل‌های جایگزین استفاده کنید 