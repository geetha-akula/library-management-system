# 📚 Library Management System (LMS)
> MAD-1 Project | IIT Madras | Built with Flask & SQLAlchemy

A full-stack **Library Management System** web application built as part of the Modern Application Development 1 (MAD-1) course at IIT Madras. The system allows librarians and students to manage books, sections, and borrowing activity through a clean, role-based web interface.

---

## 🚀 Features

- 🔐 **User Authentication** – Secure login and registration system
- 📖 **Book Management** – Add, edit, delete, and search books
- 🗂️ **Section Management** – Organize books into sections/categories
- 📋 **Borrow & Return** – Track book issues and returns
- 📊 **Dashboard** – Overview of library stats and activity
- 👤 **Role-Based Access** – Separate views for Admin and Student roles

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite, Flask-SQLAlchemy |
| Frontend | HTML, CSS (Jinja2 Templates) |
| ORM | SQLAlchemy |

---

## 📁 Project Structure

```
root/
└── code/
    ├── application/
    │   ├── controllers.py     # Route handlers and view logic
    │   ├── database.py        # DB initialization and config
    │   └── models.py          # SQLAlchemy models
    ├── instance/
    │   └── lms.sqlite3        # SQLite database (auto-generated)
    ├── static/
    │   ├── book.css
    │   ├── dashboard.css
    │   ├── home.css
    │   ├── lib_form.css
    │   ├── login.css
    │   ├── section_books.png
    │   └── status.png
    ├── templates/             # Jinja2 HTML templates
    ├── app.py                 # Application entry point
    ├── requirements.txt       # Python dependencies
    └── wireframe.png          # UI wireframe design
    docs/
    ├── project_report.pdf
    README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/geetha-akula/library-management-system.git
cd library-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Virtual Environment

**Windows:**
```bash
env\Scripts\activate
```

**macOS/Linux:**
```bash
source env/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask
pip install Flask-SQLAlchemy
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

### 6. Deactivate Virtual Environment (when done)

```bash
deactivate
```

---


## 📌 Routes Overview

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/dashboard` | GET | Admin/User dashboard |
| `/books` | GET | View all books |
| `/books/add` | GET, POST | Add a new book |
| `/sections` | GET | View all sections |

---

## 🗃️ Database Models

- **User** – Stores user credentials and roles
- **Book** – Book details (title, author, section, availability)
- **Section** – Book categories/sections
- **Issue** – Borrow records linking users and books

---

## 📄 License

This project was developed as part of the **IIT Madras BSc in Data Science and Programming** curriculum (MAD-1 Course).

---

## 👩‍💻 Author

**Akula Geetha Maheswari**  
IIT Madras — BSc in Data Science and Programming  
📧 geethaakula123@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/geetha-akula) | [GitHub](https://github.com/geetha-akula)
