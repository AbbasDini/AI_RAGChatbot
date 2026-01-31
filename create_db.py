from app import app
from doctorbot_models import db

with app.app_context():
    db.create_all()
    print('جداول دیتابیس با موفقیت ساخته شد.') 