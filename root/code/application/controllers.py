from flask import Flask, render_template, redirect, request
from flask import current_app as app
from .models import *
from datetime import datetime, timedelta
from sqlalchemy import or_
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')

#home page
@app.route('/')
def home():
    return render_template("home.html")
    

#login and registration
@app.route('/adminlogin', methods= ['GET','POST'])
def admin_login():
    if request.method == 'POST':
        a_name = request.form.get("username")
        pwd = request.form.get("pwd")
        admin = User.query.filter_by(username = a_name, role = "admin").first()
        if admin:
            if admin.password == pwd:         
                return redirect("/librarian_dash")
            return redirect("/adminlogin")
        return redirect("/adminlogin")
    return render_template('admin_login.html')


@app.route('/userlogin', methods= ['GET','POST'])
def user_login():
   if request.method == 'POST':
        u_name = request.form.get("username")
        pwd = request.form.get("pwd")
        user = User.query.filter_by(username = u_name, role = "user").first()
        if user:
            if user.password == pwd:
                return redirect(f'/user/{user.id}')
            return redirect('/userlogin')
        return redirect('/userlogin')

   return render_template('user_login.html')



@app.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        u_name = request.form.get("username")
        pwd = request.form.get("pwd")
        user = User.query.filter_by(username = u_name).first() 
        if user:
            return ("user already exists")
        else:
            new_user = User(username= u_name, password= pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('register.html')


#librarian dashboard
@app.route('/librarian_dash', methods=['GET', 'POST'])
def librarian_dashboard():
    search_word = request.form.get('search_word', None)
    sections = None
    if search_word:
        sections = Section.query.filter(or_(
            Section.title.ilike(f'%{search_word}%'),
            Section.create_date.ilike(f'%{search_word}%'),
        )).all()
    else:
        sections = Section.query.all()
        for section in sections:
            books = Book.query.filter_by(section_id=section.id).all()
            n_books = len(books)
            Section.query.filter_by(id=section.id).update({Section.n_books: n_books})
            db.session.commit()
    return render_template('lib_dash.html', sections=sections)



#CRUD for Sections
@app.route('/add_section', methods= ['GET','POST'])
def add_section():
    if request.method == 'POST':
        title = request.form.get("title")
        c_date = datetime.now()
        description = request.form.get("description")
        section = Section(title= title, description= description, create_date= c_date)
        db.session.add(section)
        db.session.commit()
        return redirect('/librarian_dash')
    return render_template('add_section.html')


@app.route('/delete_section/<int:id>')
def delete_section(id):
    section = Section.query.filter_by(id = id).first()
    db.session.delete(section)
    db.session.commit()
    return redirect('/librarian_dash')



@app.route('/update_section/<int:id>', methods= ['GET','POST'])
def update_section(id):
    section = Section.query.filter_by(id = id).first()
    if request.method == 'POST':
        section.title = request.form.get("title")
        section.description = request.form.get("description")
        db.session.commit()
        return redirect('/librarian_dash')
    return render_template('update_section.html', section = section)


# librarian dashboard books
@app.route('/section/<int:id>', methods= ['GET','POST'])
def section(id):
    search_word = request.form.get('search_word', None)
    books = None
    if search_word:
        section = Section.query.filter_by(id = id).first()
        books = Book.query.filter_by(section_id = id).all()
        for book in books:
            books = book.query.filter(or_(
                    Book.title.ilike(f'%{search_word}%'),
                    Book.author.ilike(f'%{search_word}%'),
                    )).all()
    else:  
        section = Section.query.filter_by(id = id).first()
        books = Book.query.filter_by(section_id = id).all()
    return render_template('lib_books.html', section = section, books = books)



#CRUD for Books
@app.route('/section/<int:id>/add_book', methods= ['GET','POST'])
def add_book(id):
    section = Section.query.filter_by(id = id).first()
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        section.title = request.form.get("section_title")
        section.n_books = section.n_books + 1
        book = Book(title= title, author= author, section_title= section.title ,section_id= id, content= content)
        db.session.add(book)
        db.session.commit()
        return redirect(f'/section/{id}')
    return render_template('add_book.html',section = section)



@app.route('/update_book/<int:id>', methods= ['GET','POST'])
def update_book(id):
    book = Book.query.filter_by(id = id).first()
    if request.method == 'POST':
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.content = request.form.get("content")
        book.section_title = request.form.get("section_title")
        section_id = Section.query.filter_by(title = book.section_title).first().id
        book.section_id = section_id
        db.session.commit()
        return redirect(f'/section/{book.section_id}')
    return render_template('update_book.html', book = book)



@app.route('/delete_book/<int:id>')
def delete_book(id):
    book = Book.query.filter_by(id = id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(f'/section/{book.section_id}')


# librarian view book
@app.route('/librarian/view_book/<int:id>')
def book(id):
    book = Book.query.filter_by(id = id).first()
    content = book.content
    return render_template('lib_viewbook.html', book = book, content = content)



# librarian dashboard requests
@app.route('/librarian_dash/requests', methods= ['GET','POST'])
def requests():
    
    search_word = request.form.get('search_word', None)
    books = None
    if search_word:
            issues = Issue.query.filter(or_(
            Issue.book_name.ilike(f'%{search_word}%'),
            Issue.section_name.ilike(f'%{search_word}%'),
            Issue.user.has(User.username.ilike(f'%{search_word}%')),
            Issue.book.has(Book.title.ilike(f'%{search_word}%')),
            Issue.book.has(Book.author.ilike(f'%{search_word}%')),
            )).all()
    else:
        issues = Issue.query.all()

    return render_template('lib_requests.html', issues = issues)


@app.route('/grant/<int:issue_id>')
def grant(issue_id):
    issue = Issue.query.filter_by(id = issue_id).first()
    issue.status = "granted"
    issue.issue_date = datetime.now()
    db.session.commit()
    return redirect('/librarian_dash/requests')


@app.route('/reject/<int:issue_id>')
def reject(issue_id):
    issue = Issue.query.filter_by(id = issue_id).first()
    issue.status = "rejected"
    db.session.commit()
    return redirect('/librarian_dash/requests')


@app.route('/revoke/<int:issue_id>')
def revoke(issue_id):
    issue = Issue.query.filter_by(id = issue_id).first()
    issue.status = "returned"
    issue.return_date = datetime.now()
    db.session.commit()
    return redirect('/librarian_dash/requests')


# librarian dashboard user details
@app.route('/user_details/<int:issue_id>')
def user_details(issue_id):
    issue = Issue.query.filter_by(id = issue_id).first()
    return render_template('lib_user_details.html', issue = issue)



# librarian dashboard stats
@app.route('/stats')
def stats():
    issues = Issue.query.all()
    status = []
    for issue in issues:
        status.append(issue.status)
    plt.clf()
    plt.hist(status)
    plt.savefig('static/status.png')
        
    books = Book.query.all()
    section_books = []
    for book in books:
        section_books.append(book.section_title)
    plt.clf()
    plt.hist(section_books)
    plt.savefig('static/section_books.png')

    return render_template('lib_stats.html')


# user dashboard
@app.route('/user/<int:user_id>', methods= ['GET','POST'])
def user_dashboard(user_id):
    user = User.query.filter_by(id = user_id, role= "user").first()
    search_word = request.form.get('search_word', None)
    books = None
    if search_word:
        books = Book.query.filter(or_(
            Book.title.ilike(f'%{search_word}%'),
            Book.author.ilike(f'%{search_word}%'),
            Book.section.has(Section.title.ilike(f'%{search_word}%'))
        )).all()
    else:
        user = User.query.filter_by(id = user_id, role= "user").first()
        books = Book.query.all()
    return render_template('user_dash.html', user = user, books = books)



# user dashboard requests
@app.route('/user/<int:user_id>/requests/<int:book_id>', methods= ['GET','POST'])
def book_request(user_id,book_id):
    count = Issue.query.filter(Issue.user_id == user_id, 
                                  or_(Issue.status == "granted", Issue.status == "requested")).all()
    if len(count) >= 5:
        return ("Book request limit exceeded")
    else:
        user = User.query.filter_by(id = user_id).first()
        book = Book.query.filter_by(id = book_id).first()
        date = datetime.now()
        issue = Issue(user_id= user_id, book_id= book_id, book_name= book.title, section_name= book.section.title, status= "requested", requested_date=date)
        db.session.add(issue)
        db.session.commit()
        return ("Book requested successfully")
        return redirect(f'/user/{user_id}')


# user dashboard my_books
@app.route('/user/<int:user_id>/my_books', methods= ['GET','POST'])
def my_books(user_id):
        issues = Issue.query.filter_by(user_id = user_id, status = 'granted').all()
        for issue in issues:
            issued_date = issue.issue_date
            difference = (datetime.now() - timedelta(days=7))
            if issued_date < difference:
                issue.return_date = datetime.now()
                issue.status = 'returned'
                db.session.commit()

        user = User.query.filter_by(id = user_id).first()
        issue = Issue.query.filter_by(user_id = user_id).all()

        search_word = request.form.get('search_word', None)
        books = None
        if search_word:
            for issue in issue:
                books = issue.query.filter(or_(
                Issue.book_name.ilike(f'%{search_word}%'),
                Issue.section_name.ilike(f'%{search_word}%'),
                Issue.book.has(Book.author.ilike(f'%{search_word}%'))
                )).all()
        else: 
            books = user.requests
        return render_template('user_mybooks.html', user = user, issue = issue, books= books)


@app.route('/user/<int:user_id>/cancel/<int:issue_id>', methods= ['GET','POST'])
def cancel(user_id,issue_id):
    issue = Issue.query.filter_by(id = issue_id).first()
    db.session.delete(issue)
    db.session.commit()
    return redirect(f'/user/{user_id}/my_books')



# user view book
@app.route('/user/<int:user_id>/view/<int:book_id>')
def view_book(user_id,book_id):
    user = User.query.filter_by(id = user_id, role= "user").first()
    book = Issue.query.filter_by(id = book_id, user_id = user_id, status = "granted").first()
    return render_template('user_viewbook.html', user = user, book = book)



@app.route('/user/<int:user_id>/return/<int:issue_id>')
def return_book(user_id,issue_id):
    user = User.query.filter_by(id = user_id).first()
    issue = Issue.query.filter_by(id = issue_id).first()
    issue.status = "returned"
    issue.return_date = datetime.now()
    db.session.commit()
    return redirect(f'/user/{user.id}/my_books')



@app.route('/user/<int:user_id>/feedback/<int:book_id>', methods= ['GET','POST'])
def feedback(user_id,book_id):
    user = User.query.filter_by(id = user_id).first()
    book = Book.query.filter_by(id = book_id).first()
    if request.method == 'POST':
        message = request.form.get("message")
        feedback = Feedback(user_id= user_id, book_id= book_id, book_name= book.title, message= message)
        db.session.add(feedback)
        db.session.commit()
        issue = Issue.query.filter_by(user_id = user_id, book_id = book_id, status = "returned").first()
        issue.status = "feedback given"
        db.session.commit()
        return redirect(f'/user/{user_id}/my_books')
    return render_template('feedback.html', user = user, book = book)


