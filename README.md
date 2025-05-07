# 📚 BLook – Book Review and Discovery Platform

BLook is a Django-powered web application that allows users to discover, rate, and review books. The platform features trending and top-rated books, reviewer rankings, and categorized book collections including novels, comics, manga, and webcomics.

Design: https://www.figma.com/design/n8lcs4YWfxKZn4lJAknK5y/BLook?node-id=0-1&p=f&t=IRl6WET8y8ZOsZnK-0

## 🚀 Features

- 🔍 **Book Search**: Search by title or author.
- 📝 **Review System**: Authenticated users can write and read reviews.
- 🌟 **Top-Rated & Trending**: Showcases books based on user ratings and recent popularity.
- 🎨 **Book Spotlight**: Featured book of the week with synopsis and details.
- 🧑‍💻 **Top Reviewers**: Highlights the most active and helpful reviewers.
- 📚 **Categories Carousel**: Novels, Comics, Manga+, and WebComics.

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **Styling**: Custom CSS with Google Fonts

## 📷 Screenshots

*Coming soon – include screenshots of the homepage, search view, and review submission page.*

## 📦 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Pal-C/BLook.git
   cd BLook

2. **Create a Virtual Environment**
   python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
3. **Install Dependencies**
     ```bash
    pip install -r requirements.txt

4. **Apply Migrations**
     ```bash
    python manage.py migrate

5. **Create a Superuser**
     ```bash
    python manage.py createsuperuser

6. **Run the Development Server**
     ```bash
    python manage.py runserver

7. **Access the App**
  Visit http://127.0.0.1:8000/core/auth in your browser.

## 📁 Project Structure
![image](https://github.com/user-attachments/assets/2d8293fb-700a-438d-a2ba-06545e10f30a)
