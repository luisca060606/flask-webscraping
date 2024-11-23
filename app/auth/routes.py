import requests
from flask import render_template, request, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm, ScrapyForm
from app.auth import authentication
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user
from bs4 import BeautifulSoup
from lxml import etree


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
        flash("Registration done...")
        return redirect(url_for("authentication.log_in_user"))
    
    return render_template("registration.html", form=form)

@authentication.route("/")
def index():
    return render_template("index.html")

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


@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)
