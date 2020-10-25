import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# --------------INIT APP----------------------------------------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bracekt_builder.db'
db = SQLAlchemy(app)

# --------------MODELS----------------------------------------------------------------------------


class Bracket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    pool = relationship("Pool", uselist=False, back_populates="bracket")


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(200), nullable=False)
    bracket_id = Column(Integer, ForeignKey('bracket.id'))
    bracket = relationship("Bracket", back_populates="pool")
# --------------ROUTES----------------------------------------------------------------------------

# Index route / add movies to pool
# NEED TO FIGURE OUT HOW TO CONNECT THE DB'S AND IN WHAT ORDER
# SOMETHING TO DO WITH SESSION???


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_title = request.form['movie']
        new_movie = Pool(movie=movie_title)
        try:
            Pool.session.add(new_movie)
            Pool.session.commit()
            return redirect('/')
        except:
            return f"Something went wrong adding {new_movie.movie}"
    else:
        # movies = Bracket.query(Bracket.pool).all()
        # movies = Bracket.query.order_by(Bracket.pool.id).all()
        movies = Pool.query.order_by(Pool.id).all()
        return render_template('index.html', movies=movies)

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
