# Comments SPA – Backend

### 👉 Description

Backend API for the commenting SPA written on DRF.

The project implements a commenting system with support for nested replies, file uploads, and server-side validation.

### 🎥 Demo Video

Watch a short demo of the application:

https://www.loom.com/share/fe0f1c61ff6d4adfa1d67296441009fd

### 👉 Tech Stack

- Python 3
- Django  
- Django REST Framework
- Django Channels
- Daphne
- SQLite  
- Docker  
- Docker Compose  
- Pillow  
- Bleach  
- django-simple-captcha  

### 👉 Features

* Adding comments
* Nested comments
* Comment sorting
* Pagination (25 comments per page)
* Text file uploading (TXT)
* CAPTCHA verification
* Comment preview without reloading the page
* XSS protection
* SQL injection protection

### 👉 File requirements
#### 👉 Images

* formats: JPG, PNG, GIF
* maximum size: 320x240
* Images are automatically resized when uploaded

#### 👉 Text files

* format: TXT
* maximum size: 100 KB

### 👉 Allowed HTML tags

The user can use the following HTML tags:
```
<a href="" title=""></a>
<code></code>
<i></i>
<strong></strong>
```
All other HTML tags are removed on the server.

### 👉 API
#### 👉 Base URL

```
http://localhost:8000/api/
http://127.0.0.1:8000/api/
```

#### 👉 Get a list of comments
GET
```
/api/comments/
```
Sorting:
```
/api/comments/?sort=username
/api/comments/?sort=email
/api/comments/?sort=date
```

#### 👉 Create a comment
POST
```
/api/comments/
```

Request fields:  
-- username  
-- email  
-- homepage (optional)  
-- text  
-- parent (optional)  
-- image (optional)  
-- text_file (optional)  
-- captcha

#### 👉 Preview comment
POST
```
/api/preview/
```

#### 👉 Get CAPTCHA
GET
```
/api/captcha/
```

### 👉 Database structure
Comment:
-- id  
-- username  
-- email  
-- homepage  
-- text   
-- parent_id  
-- image  
-- text_file  
-- created_at

Comments support a tree structure.

### 👉 Database Schema

* schema.mwb — model for MySQL Workbench  
* schema.png — database schema image

Comments support a tree structure.

### ✨ How to use it

> Download the code 

```bash
git clone https://github.com/VladimirDolhyi/comments-spa.git
cd comments-spa
```

#### 👉 Set Up

> Install modules via `VENV`  

```bash
python -m venv venv
source venv/bin/activate (on macOS)
venv\Scripts\activate (on Windows)
pip install -r requirements.txt
```

> Perform migrations:

```bash
python manage.py migrate
```
> Run the server

```bash
python manage.py runserver
```

> The server will be available at:
```
http://127.0.0.1:8000
```

### 👉 Run with docker

Docker should be installed

> Clone the repository
```bash
git clone https://github.com/VladimirDolhyi/comments-spa.git
cd comments-spa
```

```bash
docker compose build
docker compose up
```
or
```bash
docker compose --build
```

> Perform migrations:

In the new terminal:
```bash
docker compose exec backend python manage.py migrate
```

> Open project
```
http://localhost:8000
```

> Stop project
```bash
docker compose down
```

### 👉 Security
#### 👉The project includes:
* XSS protection via bleach
* SQL injection protection via Django ORM
* server-side data validation
* CAPTCHA to protect against spam

### 👉 Comments List
![Comments List](images/Comments List.png)

### 👉 Comment Create
![Comment Create](images/Comment Create.png)

### 👉 Comment Preview
![Comment Preview](images/Comment Preview.png)

### 👉 Captcha
![Captcha](images/Captcha.png)
