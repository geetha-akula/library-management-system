from .database import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), nullable = False, default="user")
    requests = db.relationship("Issue", backref= "user")
    feedbacks = db.relationship("Feedback")

    

class Section(db.Model):
    id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    title = db.Column(db.String(), unique = True, nullable= False)
    description = db.Column(db.String())
    n_books = db.Column(db.Integer(), default=0)
    create_date = db.Column(db.Date())
    books = db.relationship("Book", backref= "section")
    


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    title = db.Column(db.String(), unique = True, nullable= False)
    author = db.Column(db.String())
    content = db.Column(db.String())
    section_title = db.Column(db.String())
    section_id = db.Column(db.Integer(), db.ForeignKey("section.id"))
    issue = db.relationship("Issue", backref= "book")
    feedbacks = db.relationship("Feedback", backref= "book")



class Issue(db.Model):
    id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer(), db.ForeignKey("book.id"))
    book_name = db.Column(db.String())
    section_name = db.Column(db.String())
    status = db.Column(db.String(), default="requested", nullable= False)
    request_type = db.Column(db.String(), default="read")
    requested_date = db.Column(db.Date(), nullable= False)
    issue_date = db.Column(db.DateTime())
    return_date = db.Column(db.Date())


class Feedback(db.Model):
    id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer(), db.ForeignKey("book.id"))
    book_name = db.Column(db.String())
    message = db.Column(db.String())