import os
from random import shuffle
from random import randint
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# --------------INIT APP----------------------------------------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bracket_builder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------MODELS----------------------------------------------------------------------------


class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    pool_size = db.Column(db.Integer, nullable=False)
    filled_out = show_bracket = db.Column(
        db.Boolean, default=False, nullable=False)
    show_bracket = db.Column(db.Boolean, default=False, nullable=False)
    pool = db.relationship("Movie", backref="bracket")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    in_bracket = db.Column(db.Boolean, default=False, nullable=False)
    bracket_order = db.Column(db.Integer, nullable=True)
    bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.id'))


# --------------ROUTES-----------------------------------------------------------------------------

    # Index route / create bracket


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bracket_theme = request.form['theme']
        bracket_size = request.form['size']
        size_of_pool = request.form['pool_size']
        new_bracket = Bracket(theme=bracket_theme,
                              pool_size=size_of_pool, size=bracket_size)
        try:
            db.session.add(new_bracket)
            db.session.commit()
            return redirect(f'/bracket/{new_bracket.id}')
        except:
            return f"Something went wrong adding {new_bracket.theme}"
    else:
        brackets = Bracket.query.order_by(Bracket.id).all()
        return render_template('index.html', brackets=brackets)

# Add movies to pool


@app.route('/bracket/pool', methods=['POST'])
def add_movies():
    pool_size = int(request.form['pool_size'])
    bracket_size = int(request.form['size'])
    bracket_id = request.form['id']
    
    for m in range(1, pool_size + 1):
        movie_title = request.form[f'movie{m}']
        movie_bracket_id = request.form['id']
        movie_votes = int(request.form[f"votes{m}"])
        new_movie = Movie(title=movie_title, votes=movie_votes,
                          bracket_id=movie_bracket_id)

        try:
            db.session.add(new_movie)
            db.session.commit()
        except:
            return f"Something went wrong adding {new_movie.title}"
    return redirect(f'/bracket/{bracket_id}')


# Fill out bracket

@app.route('/bracket/set-bracket', methods=['POST'])
def set_bracket_order():
    bracket_id = request.form['id']
    bracket = db.session.query(Bracket).filter(
        Bracket.id == bracket_id).one()
    bracket_pool = bracket.pool
    # for i in range(new_movie.votes):
    #         movie_pool.append(new_movie)

    randomized_pool = []
    for m in bracket_pool:
        for i in range(m.votes):
            randomized_pool.append(m)

    shuffle(randomized_pool)
    for m in randomized_pool:
        print(m.title)
    cnt = 1
    while cnt <= len(bracket.pool):
        idx = randint(0, len(randomized_pool)-1)
        pick = randomized_pool[idx]
        if pick.in_bracket:
            continue
        else:
            # set_movie = Movie.query.get_or_404(pick.id)
            set_movie = db.session.query(Movie).filter(
                Movie.id == pick.id).one()
            set_movie.in_bracket = True
            set_movie.bracket_order = cnt
            cnt += 1
            db.session.commit()
            set_bracket = db.session.query(Bracket).filter(
                Bracket.id == bracket_id).one()
            set_bracket.filled_out = True
            db.session.commit()

    # return redirect(f'/bracket/{new_movie.bracket_id}')
    return redirect(f'/bracket/{bracket_id}')

# Add another movie input on bracket page


@app.route('/bracket/<int:id>/add-movie', methods=['POST'])
def add_movie_input(id):
    bracket_id = request.form['id']
    set_bracket = db.session.query(Bracket).filter(
        Bracket.id == bracket_id).one()
    set_db_index = len(set_bracket.pool) + 1
    new_movie_title = request.form[f'movie{set_db_index}']
    new_movie_votes = request.form[f'votes{set_db_index}']
    set_bracket.pool_size += 1
    new_movie = Movie(title=new_movie_title, votes=new_movie_votes,
                          bracket_id=bracket_id)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(f'/bracket/{bracket_id}')
# view bracket


@app.route('/bracket/<int:id>', methods=['GET'])
def view_bracket(id):
    show_bracket = Bracket.query.get_or_404(id)
    return render_template('bracket.html', bracket=show_bracket)

# Delete Bracket


@app.route('/bracket/delete/<int:id>')
def delete_bracket(id):
    bracket_to_delete = Bracket.query.get_or_404(id)

    try:
        db.session.delete(bracket_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f"Sorry, we couldn't delete the {bracket_to_delete.theme} bracket"

# Deleting movies from the pool


@app.route('/delete/<int:id>')
def delete(id):
    movie_to_del = Movie.query.get_or_404(id)

    try:
        db.session.delete(movie_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return f"Sorry, we couldn't delete {movie_to_del.title}"

# Edit specific movie in pool


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Movie.query.get_or_404(id)
    if request.method == 'POST':
        movie.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error editing the movie"
    else:
        return render_template('update.html', movie=movie)


# --------------RUN SERVER----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

#GRAVEYARD!!!!
# {% for i in range(1, bracket.pool_size + 1) %} 