from app import create_app, db
from app.auth.models import User


flask_scraty_app = create_app("prod")
with flask_scraty_app.app_context():
    db.create_all()
    if not User.query.filter_by(user_name='test').first():
        User.create_user(
            user='test',
            email='test@example.com',
            password='123456'
        )

flask_scraty_app.run()