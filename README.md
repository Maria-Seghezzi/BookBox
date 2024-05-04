# BookBox

#### Video Demo: https://youtu.be/xkgCZJbec7M

#### Description:

BookBox is an online place to keep track of all of your books, whether you're reading them, have already finished them or would like to read them in the future.  
This website was made using Flask, JavaScript, HTML, and CSS. The styling is mainly made using the [Bootstrap](https://getbootstrap.com/) library. The book covers for all the pages in the website are provided by the [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers).

## Website pages and templates

### Sign in

**href:** `/sign-in`  
**Template:** [`sign_in.html` ](website/templates/sign_in.html)

Allows users to create an account. Once all the information has been checked the account will be created, and the user will be logged in and redirected to the [homepage](#home).

### Login

**href:** `/login`  
**Template:** [`login.html` ](website/templates/login.html)

Allows users that already created an account to log into the site. After checking that both username and password match, the user will be redirected to the [homepage](#home).

### Profile

**href:** `/profile`  
**Template:** [`profile.html` ](website/templates/profile.html)

This page allows the user to view and change the data associated with his profile. In particular the user will be able to change the username, the email and the password. This page also displays a button that leads to the [delete account](#delete-account) page.

### Delete account

**href:** `/delete_account`  
**Template:** [`delete_account.html` ](website/templates/delete_account.html)

This page allows the user to delete the account, and can be accessed from the profile page. Once on the page the user will have to insert username and password, and once the data provided is checked the account will be deleted, along with all the books in the user's library and the user's reviews, the user will then be redirected to the [sign in](#sign-in) page.

### Home

**href:** `/`  
**Template:** [`index.html` ](website/templates/index.html)

This is the main page, where users can view the books they currently have in their library. It's composed by three sections, one for books saved as "currently reading", one for books saved as "read" and one for books saved as "want to read". If the user hasn't saved any books yet, a message will appear suggesting to add books to the library to be able so see them in the homepage, and a button will redirect to the [search](#search) page.
Each book in the homepage has two buttons linked to it, one which leads the user to the [book info](#book-info) page for that book and one that allows the user to delete the book from the library.

### Book info

**href:** `/book_info`  
**Template:** [`book_info.html` ](website/templates/book_info.html)

This page contains all the information about the given book. It displays the cover image, some relvant information, a description of the book and the reviews made by other users who have read the book. If the user has not added the book to their library, a select menu will be displayed, allowing to choose the status of the book and to add it to the user's library. If the user's library already contains the book, the user will have the possibility to change the reading dates or to delete the book from the library, and if the book is marked as "read" a form to post a review will also be displayed.

### Search

**href:** `/search`  
**Template:** [`search.html` ](website/templates/search.html)

This page allows users to search through the book database. The user can search by title, author or ISBN, and the results will be displayed below the search box, each with a button that will redirect the user on the [book info](#book-info) page for that book. If there is no result a message will appear asking to add the book to the database, along with a button that will redirect to the [add book](#add-book) page.

### Reviews

**href:** `/reviews`  
**Template:** [`reviews.html` ](website/templates/reviews.html)

This page displays all the reviews written by the current user, each with a button that allows to delete it.

### Add book

**href:** `/add_book`  
**Template:** [`add_book.html` ](website/templates/add_book.html)

This page allows the user to add a book to the database, the page contains a form that the user will be asked to fill with the book's information. If the form is correctly filled the book will be added to the database.  
This page can be accessed only after searching for a book that isn't in the database, in this case a message will appear asking to add the book to the database, along with a button that will redirect to this page.

## Files and folders

### /static

This folder contains two static files: [`styles.css`](website/static/styles.css) and [`index.js`](website/static/index.js).

##### `styles.css`

This file contains the CSS used to style the website in addition to the Bootstrap library. In particular it contains rules to make the website responsive and easy to use even on mobiles.

##### `index.js`

This file contains the javascript code to handle the [delete account](#delete-account) page. In particular it contains code that will be executed after the "Edit Profile" button is clicked.

### /templates

This folder contains all the html templates that will be rendered by the website. All the templates mentioned above extend [`layout.html`](website/templates/layout.html), which is the base template, in which the navbar, the alerts and the footer are defined.

### `__init__.py`

This file contains the function to create the flask app and the [database](#database) and to initialize the flask login manager.

### `models.py`

This file contains the [database](#database)'s models for:

- User
- Book
- UserBooks
- Review

### `auth.py`

This file contains all the site's routes linked to authentication, in particular:

- `/sign_in`
- `/login`
- `/logout`: logs user out.
- `/delete_account`
- `/profile`

### `views.py`

This file contains all the other website's routes:

- `/`
- `/search`
- `/book_info`
- `/change_date`: receives and handles post requests to change the date when the user started and finished the book.
- `/post_review`: receives and handles post requests to post books' reviews.
- `/remove_from_library`: receives and handles post requests to delete a book from the user's library.
- `/add_book`
- `/reviews`

### `main.py`

This file imports the function defined in [`__init__.py`](website/__init__.py) and actually creates and runs the app.

## Database

The database for this project is handled with the [SQLAlchemy](https://www.sqlalchemy.org/) library.
The database contains three tables: user, book, review and user_books.

### user

- _id_: primary key of the table.
- _email:_ user's email.
- _username_: user's username
- _password_: user's password, stored as hash.

### book

- _id_: primary key of the table.
- _title_: book's title.
- _author_: book's author.
- _category_: book's category.
- _description_: book's description.
- _page_number_: number of pages.
- _language_: language in which the book is written.
- _publisher_: book's publisher.
- _isbn_: book's ISBN.

### user_books

- _id_: primary key of the table.
- _person_id_: id of the user who added the book to their library.
- _book_id_: id of the book that has been added.
- _status_: status of the book, can be "reading", "read" or "want_to_read".
- _date_started_: date when the user started to read the book.
- _date_finished_: date when the user finished the book.

### review

- _id_: primary key of the table.
- _book_id_: id of the book the review is about.
- _person_id_: id of the user that wrote the review.
- _person_username_: username of the user that wrote the review.
- _text_: text of the review.
- _stars_: number of stars (between 1 and 5) the user assigned to the book.
- _date_: date when the review was posted.
