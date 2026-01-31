from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DoctorBotSettings(db.Model):
    __tablename__ = 'doctorbot_settings'
    id = db.Column(db.Integer, primary_key=True)
    llm_model = db.Column(db.String(100))
    tts_model = db.Column(db.String(100))
    stt_model = db.Column(db.String(100))
    embedding_model = db.Column(db.String(100))
    api_key = db.Column(db.String(200))
    # سایر تنظیمات مورد نیاز

class MedicalDocument(db.Model):
    __tablename__ = 'medical_documents'
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200))
    content = db.Column(db.Text)
    embedding = db.Column(db.PickleType)
    # سایر فیلدهای مورد نیاز 