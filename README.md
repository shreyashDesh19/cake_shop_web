# 🎂 Sweet Cravings – Cake Shop Website

A full-stack cake shop website built with **Python Flask**, **MySQL**, and **Bootstrap 5**.

---

## 📁 Project Structure

```
sweet_cravings/
├── app.py               ← Main Flask application (all routes)
├── config.py            ← Database credentials & settings
├── requirements.txt     ← Python dependencies
│
├── database/
│   └── schema.sql       ← Create database + tables + seed data
│
├── static/
│   ├── css/style.css    ← Custom styles (cream/pink/brown palette)
│   ├── js/main.js       ← Client-side JavaScript
│   └── images/cakes/    ← Uploaded cake images go here
│
└── templates/
    ├── base.html         ← Shared layout (navbar + footer)
    ├── index.html        ← Home page
    ├── cakes.html        ← Browse & search cakes
    ├── cake_detail.html  ← Single cake page + add to cart
    ├── cart.html         ← Shopping cart
    ├── checkout.html     ← Delivery form + place order
    ├── orders.html       ← Customer order history
    ├── login.html        ← Customer login
    ├── register.html     ← Customer registration
    └── admin/
        ├── login.html     ← Admin login
        ├── admin_base.html← Admin layout (sidebar)
        ├── dashboard.html ← Stats & recent orders
        ├── cakes.html     ← Add / edit / delete cakes
        ├── edit_cake.html ← Edit existing cake
        ├── orders.html    ← Manage all orders & update status
        └── customers.html ← View registered customers
```

---

## ⚙️ Installation & Setup

### Step 1 – Install Python
Download Python 3.10+ from https://python.org and install it.

### Step 2 – Install MySQL
Download MySQL Community Server from https://dev.mysql.com/downloads/mysql/ and install it.

### Step 3 – Create a virtual environment
```bash
# Open a terminal in the sweet_cravings folder
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 4 – Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 5 – Create the MySQL database
Open MySQL Workbench or the MySQL command-line and run:
```bash
mysql -u root -p < database/schema.sql
```
Or paste the contents of `database/schema.sql` directly into MySQL Workbench and execute it.

### Step 6 – Configure database credentials
Open `config.py` and set your MySQL username and password:
```python
MYSQL_USER     = 'root'       # your MySQL username
MYSQL_PASSWORD = ''           # your MySQL password
```

### Step 7 – Run the website
```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## 🔑 Login Credentials

### Customer (Register yourself)
- Go to **http://localhost:5000/register**
- Fill in name, email, phone, and password
- Login at **http://localhost:5000/login**

### Admin
- URL: **http://localhost:5000/admin/login**
- Username: `admin`
- Password: `admin123`

---

## 🌟 Features

### Customer Features
| Feature | How to use |
|---|---|
| Browse cakes | Click "Cakes" in navbar |
| Search & filter | Use the search bar and category pills on the cakes page |
| Cake detail | Click any cake → choose size & flavour |
| Add to cart | Select size/flavour/quantity → "Add to Cart" |
| Checkout | Cart → "Proceed to Checkout" → fill form → "Place Order" |
| Order history | Click "My Orders" in navbar |

### Admin Features
| Feature | Where |
|---|---|
| Stats dashboard | /admin/dashboard |
| Add / edit / delete cakes | /admin/cakes |
| Upload cake image | Add Cake modal → "Cake Image" field |
| Update order status | /admin/orders → dropdown → "Update" |
| View customers | /admin/customers |

---

## 🗄️ Database Tables

| Table | Purpose |
|---|---|
| `admins` | Admin login credentials |
| `users` | Customer accounts |
| `categories` | Cake categories (Birthday, Wedding, etc.) |
| `cakes` | Cake catalog with price, stock, sizes, flavours |
| `cart` | One cart row per user |
| `cart_items` | Individual items inside a cart |
| `orders` | Placed orders with delivery info |
| `order_items` | Snapshot of each item in an order |

---

## 🎓 Viva Explanation Guide

| Question | Answer |
|---|---|
| What framework did you use? | Python Flask – a lightweight web framework |
| How is the password stored? | Bcrypt hashing – passwords are never stored in plain text |
| How does the cart work? | Each user has a `cart` row; items go in `cart_items` |
| What happens when an order is placed? | Cart items are copied to `order_items` (price snapshot), then cart is cleared |
| How does admin differ from customers? | Separate `admins` table, separate session keys (`admin_id`), separate routes protected by `@admin_required` |
| What is a decorator? | `@login_required` and `@admin_required` are Python decorators – they wrap route functions to check session before allowing access |
| How does search work? | SQL `LIKE %keyword%` on the cake name and description columns |
| What is ORM? | We use raw SQL with `flask_mysqldb` – no ORM – so students can see exact SQL queries |

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons, JavaScript
- **Backend**: Python 3, Flask 3
- **Database**: MySQL 8
- **Security**: bcrypt password hashing, Flask sessions
- **Image Upload**: Werkzeug secure_filename
