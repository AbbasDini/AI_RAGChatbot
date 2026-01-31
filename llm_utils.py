import os
from dotenv import load_dotenv
from doctorbot_models import DoctorBotSettings

load_dotenv()

AVALAI_API_KEY = os.getenv("AVALAI_API_KEY")
AVALAI_BASE_URL = os.getenv("AVALAI_BASE_URL", "https://api.avalai.ir/v1")
AVALAI_MODEL_NAME = os.getenv("AVALAI_MODEL_NAME", "gpt-4.1")

def get_llm():
    settings = DoctorBotSettings.query.first()
    api_key = (settings.api_key or '').strip() if settings else ''
    model_name = (settings.llm_model or '').strip() if settings else ''
    api_key = api_key or AVALAI_API_KEY
    model_name = model_name or AVALAI_MODEL_NAME
    base_url = AVALAI_BASE_URL
    from langchain_openai import OpenAI
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        temperature=0.7
    ) 