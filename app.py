from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# model


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.id
# routes


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_title = request.form['title']
        new_movie = Movie(title=movie_title)
        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return f"Something went wrong adding {new_movie.title}"
    else:
        movies = Movie.query.order_by(Movie.id).all()
        return render_template('index.html', movies=movies)


@app.route('/delete/<int:id>')
def delete(id):
    movie_to_del = Movie.query.get_or_404(id)

    try:
        db.session.delete(movie_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return f"Sorry, we couldn't delete {movie_to_del.title}"


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


# run server
if __name__ == '__main__':
    app.run(debug=True)
