import requests
from flask import render_template, request, flash, redirect, url_for, jsonify
from app.auth.forms import RegistrationForm, LoginForm, ScrapyForm
from app.auth import authentication
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user
from bs4 import BeautifulSoup
from lxml import etree

from app.utils.security import Security

@authentication.route("/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash("User Registered")
        return redirect(url_for("authentication.log_in_user"))
    
    return render_template("registration.html", form=form)

@authentication.route("/", methods=['GET'])
def index():
    return redirect(url_for("authentication.log_in_user"))

@authentication.route("/login", methods=["GET", "POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("You Are logged in the System")
        return redirect(url_for("authentication.homepage"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid credentials")
            return redirect(url_for("authentication.log_in_user"))
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for("authentication.homepage"))
    return render_template("login.html", form=form)

@authentication.route("/homepage")
@login_required
def homepage():
    return render_template("home.html")

@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for("authentication.log_in_user"))

@authentication.route("/scrapy_data", methods=["GET", "POST"])
@login_required
def scrapy_data():
    form = ScrapyForm()
    if form.validate_on_submit():
        search = form.search_article.data
        url = f"https://listado.mercadolibre.com.bo/{search}#D[A:{search}]"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']//li")
        list_articles = []
        for article in data_articles:
            dict_article = {}
            dict_article['title'] = article.xpath(".//h2[@class='poly-box poly-component__title']//a/text()")[0]
            dict_article['url_path'] = article.xpath(".//h2[@class='poly-box poly-component__title']//a/@href")[0]
            dict_article['currency'] = article.xpath(".//div[@class='poly-component__price']//div[@class='poly-price__current']//span[@class='andes-money-amount__currency-symbol']/text()")[0]
            dict_article['price'] = article.xpath(".//div[@class='poly-component__price']//div[@class='poly-price__current']//span[@class='andes-money-amount__fraction']/text()")[0]
            if article.xpath(".//div[@class='poly-card__portada']//img")[0].attrib.get('decoding') == 'sync':
                dict_article['url_img'] = article.xpath(".//div[@class='poly-card__portada']//img")[0].attrib.get('src')
            else:
                dict_article['url_img'] = article.xpath(".//div[@class='poly-card__portada']//img")[0].attrib.get('data-src')
            list_articles.append(dict_article)

        data = {"articles": list_articles}
        return render_template("scrapy_data.html", **data)
    return render_template("scrapy_data.html", form=form)

@authentication.route('/', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(user_email=email).first()
    if user and user.check_password(password):
        authenticated_user = login_user(user)
    else:
        authenticated_user = None
    
    if authenticated_user is not None:
        encoded_token = Security.generate_token(user)
        return jsonify({"isSuccess": True, "token": encoded_token}), 200
    else:
        return jsonify({"isSuccess": False, "message": "Incorrect password or email"}), 400

@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404

# init endpoints api rest users
@authentication.route('/api/v1/users/', methods=['GET'])
def get_users():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            users = User.query.all()
            if (len(users) > 0):
                return jsonify(users_list=[i.serialize for i in users]), 200
            else:
                return jsonify({'message': "NOT FOUND"}), 404
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401
    
@authentication.route('/api/v1/users/', methods=['POST'])
def createUser():
    data = request.json
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'isSuccess': False, 'message': 'All fields required'}), 400
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            User.create_user(
                user=data['name'],
                email=data['email'],
                password=data['password']
            )
            return jsonify({'isSuccess': True, 'message': 'Usere created'}), 200
        except Exception as e:
            print (dir(e))
            print (e.args)
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401    
    
@authentication.route('/api/v1/users/<int:pk>', methods=['GET'])
def get_user(pk):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user = User.query.filter_by(id=pk).first()
            if (user):
                return jsonify(user.serialize), 200
            else:
                return jsonify({'message': "NOT FOUND"}), 404
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401
    
@authentication.route('/api/v1/users/<int:pk>', methods=['PUT'])
def put_user(pk):
    data = request.json
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            user = User.query.filter_by(id=pk).first()
            if (user):
                return jsonify(user.serialize), 200
            else:
                return jsonify({'message': "NOT FOUND"}), 404
        except Exception as e:
            return jsonify({'message': "ERROR", 'success': False}), 400
    else:
        return jsonify({'message': 'UnAuthorized'}), 401      
# end endpoints api rest users
