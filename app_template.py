from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# model


# class Movie(db.Model):
class Pool(db.Model):
    __tablename__ = 'pool'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey('pool.id'))

    def __repr__(self):
        return '<Title %r>' % self.id


class Bracket(db.Model):
    __tablename__ = 'bracket'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    pool = relationship('Pool')
# routes

# Adding movies to the pool


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_title = request.form['title']
        new_movie = Pool(title=movie_title)
        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return f"Something went wrong adding {new_movie.title}"
    else:
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


# Create bracket
@app.route('/bracket', methods=['POST', 'GET'])
def make_bracket():
    if request.method == 'POST':
        bracket_theme = request.form['theme']
        try:
            shuffle_pool = []
            for movie in pool:
                new_movie = movie.title
                print(new_movie)
                # db.session.add(new_movie)
                # db.session.commit()
            return redirect('/')
        except:
            return f"Something went wrong adding {new_movie.title}"
    else:
        movies = Pool.query.order_by(Pool.id).all()
        return render_template('index.html', movies=movies)


# run server
if __name__ == '__main__':
    app.run(debug=True)
