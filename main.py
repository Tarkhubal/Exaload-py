import os
if os.name != "nt":
    from crypt import methods

from flask import Flask, render_template, redirect, url_for, request, flash, make_response, send_from_directory, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from flaskwebgui import FlaskUI
from PIL import Image

# import flaskwebgui
import time
import requests


app = Flask(__name__)

port = 20065
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db: SQLAlchemy = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    background = db.Column(db.String(1000), default="static/assets/img/wallhaven-83ogv2.png")

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    plot = db.Column(db.String(1000))

class MoviesAdmins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    rank = db.Column(db.Integer, default=3) # 0 = viewer, 1 = editor, 2 = admin, 3 = owner


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))




def get_scrollbar_gradient(image_path: str):
    image = Image.open(image_path)

    top_right_pixel = image.getpixel((image.width - 1, 0))
    bottom_right_pixel = image.getpixel((image.width - 1, image.height - 1))
    return f"linear-gradient(to bottom, rgba{top_right_pixel}, rgba{bottom_right_pixel});"





@app.route('/faq')
def faq():
    return render_template('faq.html', title="FAQ", stylesheet='faq')


@app.route('/settings')
def settings():
    theme = request.cookies.get('theme')
    
    # Déterminer le thème par défaut si aucun cookie n'est défini
    if theme is None:
        theme = 'clair'
    
    return render_template('settings.html', title="Paramètres", stylesheet='settings', theme=theme)


@app.route('/')
def index():
    db.create_all()

    if current_user.is_authenticated:
        return render_template('connected/index.html', title="Accueil", scroll_bar_gradient=get_scrollbar_gradient(current_user.background))
    
    return render_template('not-connected/index.html', stylesheet="index", title="Accueil")

@app.route("/pricing")
def pricing():
    return render_template("not-connected/pricing.html", title="Abonnements", stylesheet="pricing")


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect("/profile")
    
    return render_template('not-connected/login.html', stylesheet="not connected/base-login", title="Connexion")

@app.route('/projets')
def projets():
    return render_template('projets.html', stylesheet="projets", title="Nos Projets")


@app.route('/login', methods=['POST'])
def login_post():
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    username = request.form.get('username')
    if "@" in username and "." in username:
        user = User.query.filter_by(email=username).first()
    else:
        user = User.query.filter_by(name=username).first()
        
    
    if not user or not check_password_hash(user.password, password):
        flash({
            "msg": 'Vérifiez vos identifiants et réessayez.',
            "title": "Identifiants invalides",
            "type": "danger"
        })
        return redirect("/login")
    
    login_user(user, remember=remember)
    return redirect("/")


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect("/profile")
    
    return render_template('not-connected/register.html', stylesheet="not connected/base-login", title="Inscription")


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    if "@" in name:
        flash({
            "msg": 'Votre nom d\'utilisateur ne peut pas contenir de "@"',
            "title": "Identifiants invalides",
            "type": "danger"
        })
        return redirect("/register")
    
    # if len(password) < 12:
    #     flash({
    #         "msg": f'Your password must have at least 12 characters (actual : {len(password)})',
    #         "type": "danger"
    #     })
    #     return redirect("/register")
    

    user = User.query.filter_by(email=email).first()
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash({
            "msg": 'Un compte avec cet email existe déjà. Essayez de vous connecter et/ou de réinitialiser votre mot de passe si vous l\'avez oublié',
            "title": "Identifiants invalides",
            "type": "danger"
        })
        return redirect("/register")
    
    if os.name == "nt":
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))
    else:
        try:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
        except:
            try:
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            except:
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # connect the user
    login_user(new_user, remember=True)
    return redirect("/")


@app.route('/logout')
@login_required
def logout():
    print(f'Logout user {current_user.name}')
    logout_user()
    return redirect("/")


@app.route('/profile')
@login_required
def profile():
    
    tomorrow = 29.183
    tomorrow_splt = str(tomorrow).split(".", 1)
    today = 34.442
    today_splt = str(today).split(".", 1)
    diff = round(today - tomorrow, 3)
    diff_splt = str(diff).split(".", 1)
    
    data = {
        "name": str(current_user.name),
        "exacoins": {
            "real": today_splt[0],
            "decimal": today_splt[1],
            "float": today
        },
        "tomorrow_ex": {
            "real": tomorrow_splt[0],
            "decimal": tomorrow_splt[1],
            "float": tomorrow
        },
        "diff": {
            "real": diff_splt[0],
            "decimal": diff_splt[1],
            "float": diff,
            "sign": "+" if diff >= 0 else "-"
        },
        "cashback": {
            "buy": {
                "movies": str(1.2),
                "serie_ep": str(4.6),
                "games": str(2.4),
                "musics": str(0.6)
            },
            "location": {
                "movies": str(1.1),
                "serie_ep": str(3.2),
                "musics": str(0.4)
            }
        },
        "winning": {
            "daily_per_ad": str(0.04),
            "per_movie_ad": str(0.01),
            "per_banner_ad": str(0.03)
        },
        "max_win_per_day": "1.24",
        "last_update": str(time.strftime("Mis à jour dernièrement le %d/%m/%Y à %H:%M:%S", time.localtime()))
    }
    return render_template('connected/profile.html', data=data, title="Profil", scroll_bar_gradient=get_scrollbar_gradient(current_user.background))



@app.route('/switch_theme', methods=['POST'])
def switch_theme():
    # Récupérer le thème sélectionné depuis la requête AJAX
    theme = request.form['theme']
    response = make_response()
    
    # Définir le cookie de thème avec une durée de vie de 30 jours
    response.set_cookie('theme', theme, max_age=30 * 24 * 60 * 60)
    return response



# Errors handlers
@app.errorhandler(404)
def page_non_trouvee(e):
    last_page = request.referrer if request.referrer not in (None, "None", "none") else "/"
    return render_template('errors/404.html', last_page=last_page), 404


# ---------------- Games ----------------
@app.route('/games/hack-card-game')
def hack_card_game():
    return send_from_directory("templates/games", "hack-card-game.html")


@app.route('/movies')
@login_required
def _movies():
    return render_template('connected/movies.html', title="Films", scroll_bar_gradient=get_scrollbar_gradient(current_user.background))

@app.route('/movies/000')
@login_required
def _movies_id():
    movie_name = "Taken 3"
    return render_template('connected/movie-info.html', title=movie_name, scroll_bar_gradient=get_scrollbar_gradient(current_user.background))







# ---------------- Creator Dashboard ----------------
@app.route('/creators')
@login_required
def _index_creators():
    return render_template('connected/creator/index.html', background=current_user.background, active_page="home")

@app.route('/creators/movies')
@login_required
def _movies_creators():
    movies = requests.get(f"http://localhost:{port}/api/v1/movies/list", params={"user_id": current_user.id}).json()
    return render_template('connected/creator/movies.html', background=current_user.background, active_page="movies", movies=movies["data"], count=movies["count"])

@app.route('/creators/movies/new')
@login_required
def _movies_new_creators():
    return render_template('connected/creator/movies/new.html', background=current_user.background, active_page="movies")

# Create a route to view a specific movie '/creators/movies/<id>'
@app.route('/creators/movies/<id>')
@login_required
def _movies_id_creators(id):
    movie = Movie.query.filter_by(id=id).first()
    return render_template('connected/creator/movies/view.html',
        background=current_user.background, active_page="movies",
        movie=movie
    )

# @app.route('/signup', methods=['POST'])
# def _signup_post():
#     email = request.form.get('email')
#     name = request.form.get('nom')
#     prenom = request.form.get('prenom')
#     phone = request.form.get('phone')

#     ip = request.remote_addr
#     user_agent = request.user_agent

#     lst = json.load(open("list.json", "r", encoding="utf-8"))
    
#     lst.append({
#         "email": str(email),
#         "nom": str(name),
#         "prenom": str(prenom),
#         "telephone": str(phone),
#         "computer": {
#             "ip": str(ip),
#             "user_agent": str(user_agent)
#         },
#         "time": time.strftime("%d/%m/%Y - %H:%M:%S", time.localtime())
#     })

#     json.dump(lst, open("list.json", "w", encoding="utf-8"), indent=4)
    
#     return redirect("/packs")



# --------------------- API ---------------------
@app.route("/api/v1")
def _api_v1():
    return {"msg": "welcome on Exaload's API !"}


@app.route("/api/v1/movies")
def _api_v1_movies():
    return {"msg": "here is the movies API, gg"}

@app.route("/api/v1/movies", methods=['POST'])
def _api_v1_movies_post():
    title = request.form.get("movie_name")
    plot = request.form.get("movie_description")
    print("New request for a movie ! Data :", request.form)
    
    f = request.files['movie_file'] 
    f.save(os.path.join("static\\assets\\movies", f.filename))
    print("Saved file", f.filename)
    
    new_movie = Movie(title=title, plot=plot)
    db.session.add(new_movie)
    db.session.commit()
    new_movie_admin = MoviesAdmins(user_id=current_user.id, movie_id=new_movie.id, rank=3)
    
    db.session.add(new_movie_admin)
    db.session.commit()
    
    return redirect("/creators/movies")

@app.route("/api/v1/movies/list", methods=['GET'])
def _api_v1_movies_list():
    limit_limit = 10000
    page = (int(request.args.get("page")) if request.args.get("page") else 1) - 1
    limit = int(request.args.get("limit")) if request.args.get("limit") else 100
    user_id = int(request.args.get("user_id")) if request.args.get("user_id") else None
    
    alert = None
    if limit > limit_limit:
        alert = f"The limit is too high, it has been set to {limit_limit}. Please, don't try to overload the server."
        limit = limit_limit
    
    def get_movie(movie: Movie, owner: MoviesAdmins):
        plot = movie.plot
        max_len = 13
        
        if len(plot) > max_len:
            plot = plot[:max_len] + "..."
        title = movie.title
        if len(title) > max_len:
            title = title[:max_len] + "..."
        return {
            "id": movie.id,
            "title": movie.title,
            "plot": plot,
            "owner": owner.user_id
        }
    
    movies = []
    count = 0
    query = Movie.query
    query.limit(limit).offset(page * limit)
    if user_id:
        for movie in query.all():
            owner = MoviesAdmins.query.filter_by(
                movie_id=movie.id,
                rank=3
            ).first()
            if owner.user_id == user_id:
                count += 1
                movies.append(get_movie(movie, owner))

    else:
        for movie in query.all():
            count += 1
            owner = MoviesAdmins.query.filter_by(
                movie_id=movie.id,
                rank=3
            ).first()
            movies.append(get_movie(movie, owner))

    return {
        "data": movies,
        "success": True,
        "msg": "Here is the list of movies",
        "count": count,
        "alert": alert
    }

@app.route("/api/v1/movies/search", methods=['GET'])
def _api_v1_movies_search():
    title = request.args.get("title")
    genres = request.args.get("genres").split(",")
    
    correct = []
    
    for movie in Movie.query.all():
        if title.lower() in movie.title.lower() and len(set(movie.genres.split(",")) & set(genres)) > 0:
            correct.append(movie)
    
    return correct

@app.route("/api/v1/account/email", methods=['GET'])
@login_required
def _api_v1_account_email():
    return {"success": True, "email": current_user.email} 

@app.route("/api/v1/movies/edit/title", methods=['POST'])
def _api_v1_movies_edit_title():
    movie_id = request.form.get("movie_id")
    new_title = request.form.get("new_title")
    
    movie = Movie.query.filter_by(id=movie_id).first()
    movie.title = new_title
    db.session.commit()
    
    if not "api" in request.referrer:
        return redirect("/creators/movies/" + movie_id)
    
    return {"success": True, "msg": "Title has been updated !"}

@app.route("/api/v1/movies/edit/plot", methods=['POST'])
def _api_v1_movies_edit_plot():
    movie_id = request.form.get("movie_id")
    new_plot = request.form.get("new_plot")
    
    movie = Movie.query.filter_by(id=movie_id).first()
    movie.plot = new_plot
    db.session.commit()
    
    if not "api" in request.referrer:
        return redirect("/creators/movies/" + movie_id)
    
    return {"success": True, "msg": "Plot has been updated !"}


# def start_flask(**server_kwargs):
#     app = server_kwargs.pop("app", None)
#     server_kwargs.pop("debug", None)

#     try:
#         import waitress

#         waitress.serve(app, **server_kwargs)
#     except:
#         app.run(**server_kwargs)



if __name__ == '__main__':
    
    # server_process = flaskwebgui.Process(target=start_flask, kwargs={"app": app, "host": "194.87.217.19"
    
    # ui = FlaskUI(app=app.wsgi_app, port=port, server="flask", fullscreen=True, server_kwargs={"host": "194.87.217.19"})
    # ui.start_browser()
    
    
    app.run(debug=True, port=port, host="0.0.0.0")
