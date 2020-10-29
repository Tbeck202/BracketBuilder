import os
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
    pool = db.relationship("Pool", backref="bracket")


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(200), nullable=False)
    bracket_id = db.Column(db.Integer, db.ForeignKey('bracket.id'))
# --------------ROUTES-----------------------------------------------------------------------------

# Index route / create bracket


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        bracket_theme = request.form['theme']
        bracket_size = request.form['size']
        new_bracket = Bracket(theme=bracket_theme, size=bracket_size)
        try:
            db.session.add(new_bracket)
            db.session.commit()
            return redirect(f'/bracket/{new_bracket.id}')
        except:
            return f"Something went wrong adding {new_bracket.theme}"
    else:
        brackets = Bracket.query.order_by(Bracket.id).all()
        return render_template('index.html', brackets=brackets)

# Add movie to pool


@app.route('/bracket/pool', methods=['POST'])
def add_movie():
    movie = request.form['movie']
    movie_bracket_id = request.form['id']
    new_movie = Pool(movie=movie, bracket_id=movie_bracket_id)

    try:
        db.session.add(new_movie)
        db.session.commit()
        return redirect(f'/bracket/{new_movie.bracket_id}')
    except:
        return f"Something went wrong adding {new_movie.theme}"

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
    movie_to_del = Pool.query.get_or_404(id)

    try:
        db.session.delete(movie_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return f"Sorry, we couldn't delete {movie_to_del.title}"

# Edit specific movie in pool


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Pool.query.get_or_404(id)
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
