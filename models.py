from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChatbotSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # --- LLM Settings ---
    llm_model = db.Column(db.String(50), default='gpt-4o')
    llm_temperature = db.Column(db.Float, default=0.7)
    llm_max_tokens = db.Column(db.Integer, default=1024)
    llm_top_p = db.Column(db.Float, default=1.0)
    llm_streaming = db.Column(db.Boolean, default=True)
    system_prompt = db.Column(db.Text, default='')
    # --- Persona Settings ---
    persona = db.Column(db.String(50), default='default')
    banned_words = db.Column(db.Text, default='')
    response_delay = db.Column(db.Float, default=0.5)
    # --- TTS Settings ---
    tts_provider = db.Column(db.String(50), default='openai')
    tts_model = db.Column(db.String(50), default='gpt-4o-mini-tts')
    tts_voice = db.Column(db.String(50), default='shimmer')
    tts_speed = db.Column(db.Float, default=1.0)
    tts_accent = db.Column(db.String(50), default='تهرانی')
    tts_pitch = db.Column(db.Float, default=0.0)
    tts_autoplay = db.Column(db.Boolean, default=False)
    tts_instructions = db.Column(db.Text, default='')
    # --- General Bot Info ---
    bot_name = db.Column(db.String(100), default='چت‌بات آکسایا')
    bot_description = db.Column(db.Text, default='دستیار هوشمند مشاوره پزشکی')
    # --- API/Webhook ---
    api_key = db.Column(db.String(100), default='')
    webhook_url = db.Column(db.String(200), default='')
    # --- UI/Theme ---
    ui_theme = db.Column(db.String(20), default='light')
    welcome_message = db.Column(db.String(200), default='خوش آمدید!')
    # --- Security ---
    enable_2fa = db.Column(db.Boolean, default=False)
    rate_limit = db.Column(db.Integer, default=60)
