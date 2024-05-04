from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from .models import User, UserBooks, Book, Review
from . import db
from datetime import datetime, date

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    # id_books_read is now a list containing ids of books read
    id_books_read = list(
        map(
            lambda x: x.book_id,
            (UserBooks.query.filter_by(person_id=current_user.id, status="read").all()),
        )
    )
    start_date_books_read = list(
        map(
            lambda x: str(x.date_started),
            (UserBooks.query.filter_by(person_id=current_user.id, status="read").all()),
        )
    )
    finish_date_books_read = list(
        map(
            lambda x: str(x.date_finished),
            (UserBooks.query.filter_by(person_id=current_user.id, status="read").all()),
        )
    )
    # books_read is a list of Book objects and dates (Book, date_started, date_finished)
    books_read = (
        list(
            zip(
                Book.query.filter(Book.id.in_(id_books_read)).all(),
                start_date_books_read,
                finish_date_books_read,
            )
        )
        if id_books_read
        else []
    )

    id_books_reading = list(
        map(
            (lambda x: x.book_id),
            (
                UserBooks.query.filter_by(
                    person_id=current_user.id, status="reading"
                ).all()
            ),
        )
    )
    start_date_books_reading = list(
        map(
            lambda x: str(x.date_started),
            (
                UserBooks.query.filter_by(
                    person_id=current_user.id, status="reading"
                ).all()
            ),
        )
    )
    # books_reading is a list of Book objects and dates (Book, date_started)
    books_reading = (
        list(
            zip(
                Book.query.filter(Book.id.in_(id_books_reading)).all(),
                start_date_books_reading,
            )
        )
        if id_books_reading
        else []
    )
    id_books_want_read = list(
        map(
            lambda x: x.book_id,
            (
                UserBooks.query.filter_by(
                    person_id=current_user.id, status="want_to_read"
                ).all()
            ),
        )
    )
    books_want_read = (
        Book.query.filter(Book.id.in_(id_books_want_read)).all()
        if id_books_want_read
        else []
    )
    return render_template(
        "index.html",
        user=current_user,
        books_read=books_read,
        books_reading=books_reading,
        books_want_read=books_want_read,
    )


@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html", user=current_user, books=False)

    books = []
    search = request.form.get("search")
    if not search:
        return redirect("/search")
    if search.isdigit():
        books = Book.query.filter(Book.isbn.like(f"%{search}%")).limit(200).all()
        return render_template("search.html", books=books, user=current_user)
    else:
        books = Book.query.filter(Book.title.like(f"%{search}%")).limit(100).all()
        books += Book.query.filter(Book.author.like(f"%{search}%")).limit(100).all()
        return render_template("search.html", books=books, user=current_user)


@views.route("/book_info", methods=["GET", "POST"])
@login_required
def book_info():
    if request.method == "GET":
        today_date = date.today()
        user_book = None
        current_book_id = request.args.get("id")
        user_book = UserBooks.query.filter_by(
            person_id=current_user.id, book_id=current_book_id
        ).first()
        book = Book.query.filter_by(id=current_book_id).first()
        return render_template(
            "book_info.html",
            book=book,
            user=current_user,
            user_book=user_book,
            today_date=today_date,
        )

    book_id = request.form.get("id")
    status = request.form.get("status")
    if not status or status not in ["reading", "read", "want_to_read"]:
        flash("Please select the status", category="error")
        return redirect(f"/book_info?id={book_id}")
    if status == "reading":
        date_started = date.today()
    else:
        date_started = None
    new_user_book = UserBooks(
        book_id=book_id,
        person_id=current_user.id,
        status=status,
        date_started=date_started,
    )
    db.session.add(new_user_book)
    db.session.commit()
    return redirect(f"/book_info?id={book_id}")


@views.route("/change_date", methods=["POST"])
def change_date():
    form_date_started = request.form.get("date_started")
    form_date_finished = request.form.get("date_finished")
    this_book_id = request.form.get("id")
    if not form_date_started and not form_date_finished:
        return redirect(f"/book_info?id={this_book_id}")
    form_date_started = (
        datetime.strptime(form_date_started, f"%Y-%m-%d") if form_date_started else None
    )
    form_date_finished = (
        datetime.strptime(form_date_finished, f"%Y-%m-%d")
        if form_date_finished
        else None
    )
    if (
        form_date_finished
        and form_date_started
        and form_date_finished < form_date_started
    ):
        flash("You can't finish a book before starting it!", category="error")
        return redirect(f"/book_info?id={this_book_id}")
    status = (
        UserBooks.query.filter_by(book_id=this_book_id, person_id=current_user.id)
        .first()
        .status
    )
    if form_date_finished:
        status = "read"
    elif form_date_started and not form_date_finished:
        status = "reading"
    current_book = UserBooks.query.filter_by(
        book_id=this_book_id, person_id=current_user.id
    ).first()
    current_book.date_started = form_date_started
    current_book.date_finished = form_date_finished
    current_book.status = status
    db.session.commit()
    return redirect(f"/book_info?id={this_book_id}")


@views.route("/post_review", methods=["POST"])
def post_review():
    text = request.form.get("review")
    stars = request.form.get("stars")
    book_id = request.form.get("id")
    if not text or not stars:
        flash("Please fill all the fields", category="error")
        return redirect(f"/book_info?id={book_id}")
    elif int(stars) not in [1, 2, 3, 4, 5]:
        return redirect(f"/book_info?id={book_id}")
    new_review = Review(
        text=text,
        stars=int(stars),
        book_id=book_id,
        date=date.today(),
        person_id=current_user.id,
        person_username=current_user.username,
    )
    db.session.add(new_review)
    db.session.commit()
    flash("Review posted!", category="success")
    return redirect(f"/book_info?id={book_id}")


@views.route("/remove_from_library", methods=["POST"])
def remove_from_library():
    page = request.form.get("page")
    print(page)
    book_id = request.form.get("id")
    person_id = current_user.id
    db.session.query(UserBooks).filter_by(book_id=book_id, person_id=person_id).delete()
    db.session.commit()
    if page == "home":
        return redirect("/")
    else:
        return redirect(f"/book_info?id={book_id}")


@views.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "GET":
        return render_template("add_book.html", user=current_user)

    title = request.form.get("title")
    author = request.form.get("author")
    pages = request.form.get("pages")
    isbn = request.form.get("isbn")
    category = request.form.get("category")
    language = request.form.get("language")
    publisher = request.form.get("publisher")
    description = request.form.get("description")
    if (
        not title
        or not author
        or not pages
        or not isbn
        or not category
        or not language
        or not publisher
        or not description
    ):
        flash("please fill all the fields", category="error")
    elif not isbn.isdigit() or len(isbn) != 13:
        flash("Invalid ISBN", category="error")
    else:
        new_book = Book(
            title=title,
            author=author,
            page_number=pages,
            isbn=isbn,
            category=category,
            language=language,
            publisher=publisher,
            description=description,
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect("/search")
    return redirect("/add_book")


@views.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    if request.method == "GET":
        user_reviews = current_user.reviews
        books_id = list(map(lambda x: x.book_id, current_user.reviews))
        # reviews is a list of touple, each with a book and a review object -> (Book, Review)
        reviews = list(zip(books_id, user_reviews))
        reviews = list(map(lambda x: (Book.query.get(x[0]), x[1]), reviews))
        return render_template("reviews.html", user=current_user, reviews=reviews)

    id = int(request.form.get("id"))
    db.session.query(Review).filter_by(id=id).delete()
    db.session.commit()
    return redirect("/reviews")
