import json
# from app import db
from app.auth.models import User


def test_register_user(client, user_payload):
	response = client.post(
		"/register", data=json.dumps(user_payload), content_type="application/json"
	)
	assert response.status_code == 302
	response = client.get("/register")
	assert response.status_code == 200
	assert response.request.path == "/register"

def test_login_user(client, user_payload, user_login, app):
	response = client.post(
		"/login", data=json.dumps(user_login), content_type="application/json"
	)
	assert response.location == "/homepage"	
	assert response.status_code == 302
	response = client.get("/login")
	assert response.status_code == 302
	assert response.request.path == "/login"

def test_404_not_found(client):
	response = client.get('/url_unknown')
	assert response.status_code == 404
