from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import current_user
import flask_login
from . import model
from datetime import date, timedelta
from . import db 
from functools import wraps
from datetime import datetime
from flask.json import jsonify

bp = Blueprint("manager", __name__)

def manager_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != model.UserRole.manager:
            return redirect(url_for('auth.login', next=request.url))
        if current_user.role == model.UserRole.manager:
            return f(*args, **kwargs)
    return decorated_function

@bp.route("/schedule")
@flask_login.login_required
@manager_only
def schedule():
    projections, num_results = manager_reservations_auxiliar()
    return render_template("manager_schedule.html", packed=zip(projections, num_results), projections=projections)


@bp.route("/delete/<int:id>")
@flask_login.login_required
@manager_only
def delete(id):
    current_data = model.Projection.query.get(id)
    db.session.delete(current_data)
    db.session.commit()
    flash("You have deleted a projection", 'success')
    return redirect(url_for("manager.schedule"))


@bp.route("/edit/<int:id>")
@flask_login.login_required
@manager_only
def edit(id):
    movies = model.Movie.query.all()
    screens = model.Screen.query.all()
    current_data = model.Projection.query.get(id)
    return render_template("manager_edit.html", movies=movies, screens=screens, current_data=current_data)


@bp.route("/edit/<int:id>", methods=["POST"])
@flask_login.login_required
@manager_only
def edit_post(id):
    movie = request.form.get("movie")
    screen = request.form.get("screen")
    day = request.form.get("day")
    time = request.form.get("time")
   
    day = datetime.strptime(day, "%Y-%m-%d").date()
    time = datetime.strptime(time, "%H:%M:%S").time()

    projection = model.Projection.query.filter(model.Projection.id == id).first()
    projection.day = day
    projection.time = time
    projection.movie_id = movie
    projection.screen_id = screen 

    db.session.commit()
    flash("You have edited a projection", 'success')
    return redirect(url_for("manager.schedule"))



@bp.route("/add")
@flask_login.login_required
@manager_only
def add():
    movies = model.Movie.query.all()
    screens = model.Screen.query.all()
    current_day = date.today().strftime('%Y-%m-%d')
    return render_template("manager_add.html", movies=movies, screens=screens, current_day=current_day)

@bp.route("/add", methods=["POST"])
@flask_login.login_required
@manager_only
def add_post():
    movie = request.form.get("movie")
    screen = request.form.get("screen")
    day = request.form.get("day")
    time = request.form.get("time")
    time = time + ':00'
    day = datetime.strptime(day, "%Y-%m-%d").date()
    time = datetime.strptime(time, "%H:%M:%S").time()
    new_projection = model.Projection(day=day, time=time, movie_id=movie, screen_id=screen)
    db.session.add(new_projection)
    db.session.commit()
    return redirect(url_for("manager.schedule"))


@bp.route("/reservations")
@flask_login.login_required
@manager_only
def reservations():
    projections, num_results = manager_reservations_auxiliar()
    return render_template("manager_reservations.html", packed=zip(projections, num_results), projections=projections)


@bp.route("/manager_reservation/<int:id>")
@flask_login.login_required
@manager_only
def manager_reservation(id):
    reservations = model.Reservation.query.filter(model.Reservation.projection_id == id).order_by(model.Reservation.date_time).all()
    return render_template("manager_reservation.html", reservations=reservations)


def manager_reservations_auxiliar():
    current_day = date.today()
    future = current_day + timedelta(weeks=1) 
    past = current_day - timedelta(weeks=1)

    projections = model.Projection.query.filter(model.Projection.day <= future, model.Projection.day >= past).order_by(model.Projection.day.asc(), model.Projection.time.asc()).all()
    num_results = []
    for proj in projections:
        num_results.append(proj.screen.num_total_seats - compute_reserved_seats(proj.id))
    return projections, num_results


def compute_reserved_seats(id):
    projection = model.Projection.query.filter(model.Projection.id == id).one()
    sum_result = db.session.query(
        db.func.sum(model.Reservation.num_seats).label('reserved')
    ).filter(
        model.Reservation.projection == projection
    ).one()
    num_reserved_seats = sum_result.reserved
    if (sum_result.reserved != None):
        num_free_seats = projection.screen.num_total_seats - num_reserved_seats
    else:
        num_free_seats = projection.screen.num_total_seats 
        
    return  num_free_seats

def manager_movies_auxiliar():
    movies = model.Movie.query.all()
    num_results = []
    return movies


@bp.route('/ajax', methods=['POST', 'GET'])
def process_ajax():
    if request.method == "POST":
        projections = model.Projection.query.all()

        results = {}
        for proj in projections:
            seats = compute_reserved_seats(proj.id)
            results[proj.id] = seats
        result = results
    return jsonify(result=result)


@bp.route("/manager-add-movie")
@flask_login.login_required
@manager_only
def manager_add_movie():
    return render_template("manager_add_movie.html")


@bp.route("/movies-manager-list")
@flask_login.login_required
@manager_only
def manager_list_movies():
    movies = manager_movies_auxiliar()
    return render_template("movies_table.html",  movies=movies)


@bp.route("/add-movie", methods=["POST"])
@flask_login.login_required
@manager_only
def add_movie():
    title = request.form.get("title")
    director = request.form.get("director")
    duration = request.form.get("duration")
    main_cast = request.form.get("main_cast")
    synopsis = request.form.get("synopsis")
    img = request.form.get("img")
    new_movie = model.Movie(title=title, director=director, duration=duration, main_cast=main_cast, synopsis=synopsis, img=img)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("manager.manager_list_movies"))


@bp.route("/delete-movie/<int:id>")
@flask_login.login_required
@manager_only
def delete_movie(id):
    current_data = model.Movie.query.get(id)
    db.session.delete(current_data)
    db.session.commit()
    flash("You have deleted a movie", 'success')
    return redirect(url_for("manager.manager_list_movies"))



@bp.route("/edit-movie/<int:id>")
@flask_login.login_required
@manager_only
def edit_movie(id):
    current_data = model.Movie.query.get(id)
    return render_template("manager_edit_movie.html", current_data=current_data)


@bp.route("/edit-movie/<int:id>", methods=["POST"])
@flask_login.login_required
@manager_only
def edit_post_movie(id):
    title = request.form.get("title")
    director = request.form.get("director")
    duration = request.form.get("duration")
    main_cast = request.form.get("main_cast")
    synopsis = request.form.get("synopsis")
    img = request.form.get("img")
    
    movie = model.Movie.query.filter(model.Movie.id == id).first()
    movie.title = title
    movie.director = director
    movie.duration = duration 
    movie.main_cast = main_cast
    movie.synopsis = synopsis
    movie.img = img
    
    db.session.commit()
    flash("You have edited a movie", 'success')
    return redirect(url_for("manager.manager_list_movies"))


