# -----------------------------------------------
# config.py – Database & App Configuration
# -----------------------------------------------
# Edit the values below to match your MySQL setup.

class Config:
    # Flask secret key – change this to a long random string in production
    SECRET_KEY = 'sweet_cravings_secret_2024'

    # ---- MySQL connection settings ----
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'       # your MySQL username
    MYSQL_PASSWORD = 'Root@123'           # your MySQL password
    MYSQL_DB       = 'cake_shop_db'

    # Folder where uploaded cake images are stored
    UPLOAD_FOLDER  = 'static/images/cakes'

    # Allowed image file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
