from app.auth.models import User

def test_new_user():
	user = User(
		user_name='test',
		user_email='test@example.com',
		user_password='123456'
	)
	assert user.user_email == 'test@example.com'
	assert user.__repr__() == '<User: test@example.com>'
