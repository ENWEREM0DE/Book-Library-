from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///all_books.db'
Bootstrap(app)
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

db.create_all()






@app.route('/', methods=['POST', 'GET'])
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        newBook = Book(title=title, author=author, rating=rating)
        db.session.add(newBook)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')

@app.route('/editBook', methods=['POST', 'GET'])
def editBook():
    if request.method == 'POST':
        newRating = request.form['newRating']
        bookId =request.form['BookId']
        BookToEdit = Book.query.get(bookId)
        BookToEdit.rating = newRating
        db.session.commit()
        return redirect(url_for('home'))
    bookID = request.args.get('id')
    requestedBook = Book.query.get(bookID)
    return render_template('editBook.html', requestedBook=requestedBook)

@app.route('/delete')
def delete():
    bookId = request.args.get('id')
    bookToDelete = Book.query.get(bookId)
    db.session.delete(bookToDelete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

