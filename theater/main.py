from datetime import date, datetime, timedelta
import dateutil.tz

from flask import Blueprint, render_template, request, flash, url_for, redirect
import flask_login
from flask_login import current_user
from sqlalchemy import func
from . import model
from . import db


bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    current_day = date.today()
    future = current_day + timedelta(weeks=1)
    nmovies = model.Projection.query.filter(model.Projection.day > current_day, model.Projection.day <= future).order_by(model.Projection.day.asc(), model.Projection.time.asc()).all()
    tmovies = model.Projection.query.filter(model.Projection.day == current_day).order_by(model.Projection.time.asc()).all()

    movies = model.Movie.query.all()
    users = model.User.query.all() 
    return render_template("main/index.html", all_movies=movies, users=users, next_projections=nmovies, today_projections=tmovies)


@bp.route("/movie/<int:id>")
def movie(id):
    movie = model.Movie.query.get(id)
    current_day = date.today()

    projections = model.Projection.query.filter(model.Projection.movie_id == id, model.Projection.day >= current_day).order_by(model.Projection.day.asc(), model.Projection.time.asc()).all()
    return render_template("movie.html", movie=movie, projections=projections)

@bp.route("/user")
@flask_login.login_required
def user():
    current_day = date.today()
    now = []
    past = []
    now_reservations = model.Reservation.query.filter(model.Reservation.user_id == current_user.id).order_by(model.Reservation.date_time).all()
    for res in now_reservations:
        if res.projection.day >= current_day:
            now.append(res)
        else:
            past.append(res)
    return render_template('user.html', now_reservations = now, past_reservations = past)


@bp.route("/reservation/", defaults={'id': None})
@bp.route("/reservation/<int:id>")
@flask_login.login_required
def reservation(id):
    current_day = date.today()
    current_time = datetime.now()
    all_projections = model.Projection.query.filter(model.Projection.day >= current_day).order_by(model.Projection.day.asc(), model.Projection.time.asc()).all()
    if id == None:
        return render_template("reservation.html", projection=None, projections=all_projections)
    else:
        projection = model.Projection.query.get(id)
        projections = model.Projection.query.filter(model.Projection.movie_id == projection.movie_id, model.Projection.day >= current_day).order_by(model.Projection.day.asc(), model.Projection.time.asc()).all()
        return render_template("reservation.html", projection=projection, projections=projections)


@bp.route("/reservation/", methods=["POST"])
@flask_login.login_required
def reservation_post():
    choosen_projection = request.form.get("projection")  
    choosen_num_seats = request.form.get("seats")


    projection = model.Projection.query.get(choosen_projection)

    new_reservation = model.Reservation(user_id=current_user.id, projection_id=projection.id, num_seats=int(choosen_num_seats), date_time=datetime.now())
    
    db.session.add(new_reservation)
    db.session.commit()
    flash("You have bought %s tickets for %s"%(choosen_num_seats, projection.movie.title), 'success')
    return redirect(url_for("main.index"))


