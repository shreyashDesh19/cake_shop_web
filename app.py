"""
app.py – Main Flask Application for Sweet Cravings Cake Shop
=============================================================
This file wires together all routes (pages) with the MySQL database.
Each function handles one URL and either renders an HTML template
or redirects the user to another page.
"""

import os
import bcrypt
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from config import Config

# ── App Setup ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Connect to MySQL
mysql = MySQL(app)


# ── Helper Utilities ────────────────────────────────────────────────────────

def allowed_file(filename):
    """Check if uploaded file has an allowed image extension."""
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])


def login_required(func):
    """Decorator – redirect to login page if customer is not logged in."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """Decorator – redirect to admin login if admin is not logged in."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin login required.', 'warning')
            return redirect(url_for('admin_login'))
        return func(*args, **kwargs)
    return wrapper


def get_cart_count():
    """Return number of items in the current user's cart (for navbar badge)."""
    if 'user_id' not in session:
        return 0
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(ci.quantity), 0)
        FROM   cart c
        JOIN   cart_items ci ON ci.cart_id = c.id
        WHERE  c.user_id = %s
    """, (session['user_id'],))
    count = cur.fetchone()[0]
    cur.close()
    return int(count)


# ── Customer Routes ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page – shows featured cakes and categories."""
    cur = mysql.connection.cursor()

    # Fetch all categories
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    # Fetch featured cakes (is_featured = 1)
    cur.execute("""
        SELECT c.*, cat.name AS category_name
        FROM   cakes c
        JOIN   categories cat ON cat.id = c.category_id
        WHERE  c.is_featured = 1
        ORDER  BY c.id DESC
        LIMIT  6
    """)
    featured_cakes = cur.fetchall()

    # Total stats for "About" section
    cur.execute("SELECT COUNT(*) FROM cakes")
    total_cakes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    happy_customers = cur.fetchone()[0]

    cur.close()
    return render_template('index.html',
                           categories=categories,
                           featured_cakes=featured_cakes,
                           total_cakes=total_cakes,
                           happy_customers=happy_customers,
                           cart_count=get_cart_count())


@app.route('/cakes')
def cakes():
    """Cakes listing page with search and category filter."""
    search     = request.args.get('search', '').strip()
    cat_filter = request.args.get('category', '')

    cur = mysql.connection.cursor()

    # Build query dynamically based on filters
    query = """
        SELECT c.*, cat.name AS category_name
        FROM   cakes c
        JOIN   categories cat ON cat.id = c.category_id
        WHERE  1=1
    """
    params = []

    if search:
        query += " AND (c.name LIKE %s OR c.description LIKE %s)"
        params += [f'%{search}%', f'%{search}%']

    if cat_filter:
        query += " AND c.category_id = %s"
        params.append(cat_filter)

    query += " ORDER BY c.id DESC"
    cur.execute(query, params)
    all_cakes = cur.fetchall()

    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    cur.close()
    return render_template('cakes.html',
                           cakes=all_cakes,
                           categories=categories,
                           search=search,
                           cat_filter=cat_filter,
                           cart_count=get_cart_count())


@app.route('/cake/<int:cake_id>')
def cake_detail(cake_id):
    """Cake detail page – shows description, price, size & flavour options."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, cat.name AS category_name
        FROM   cakes c
        JOIN   categories cat ON cat.id = c.category_id
        WHERE  c.id = %s
    """, (cake_id,))
    cake = cur.fetchone()

    if not cake:
        flash('Cake not found.', 'danger')
        return redirect(url_for('cakes'))

    # Related cakes from same category
    cur.execute("""
        SELECT * FROM cakes
        WHERE category_id = %s AND id != %s
        LIMIT 4
    """, (cake[1], cake_id))  # cake[1] = category_id
    related = cur.fetchall()

    cur.close()

    # Parse size/flavour CSV strings into lists for the dropdown
    raw_sizes    = cake[6] if cake[6] else '1kg'
    raw_flavours = cake[7] if cake[7] else 'Vanilla'
    sizes    = [s.strip() for s in str(raw_sizes).split(',') if s.strip()]
    flavours = [f.strip() for f in str(raw_flavours).split(',') if f.strip()]

    return render_template('cake_detail.html',
                           cake=cake,
                           related=related,
                           sizes=sizes,
                           flavours=flavours,
                           cart_count=get_cart_count())


# ── Authentication Routes ────────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Customer registration."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        full_name = request.form['full_name'].strip()
        email     = request.form['email'].strip().lower()
        phone     = request.form['phone'].strip()
        password  = request.form['password']
        confirm   = request.form['confirm_password']

        # Basic validation
        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('register'))

        # Hash the password with bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO users (full_name, email, phone, password)
                VALUES (%s, %s, %s, %s)
            """, (full_name, email, phone, hashed.decode('utf-8')))
            mysql.connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            if 'Duplicate entry' in str(e):
                flash('An account with this email already exists.', 'danger')
            else:
                flash('Registration failed. Please try again.', 'danger')
        finally:
            cur.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            session['user_id']   = user[0]
            session['user_name'] = user[1]
            flash(f'Welcome back, {user[1]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Customer logout – clears session."""
    session.pop('user_id',   None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ── Cart Routes ─────────────────────────────────────────────────────────────

@app.route('/cart')
@login_required
def cart():
    """Show the customer's shopping cart."""
    cur = mysql.connection.cursor()

    # Get or create cart for this user
    cur.execute("SELECT id FROM cart WHERE user_id = %s", (session['user_id'],))
    cart_row = cur.fetchone()

    cart_items = []
    total      = 0

    if cart_row:
        cart_id = cart_row[0]
        cur.execute("""
            SELECT ci.id, ci.quantity, ci.size, ci.flavour,
                   ck.name, ck.price, ck.image_url, ck.id AS cake_id
            FROM   cart_items ci
            JOIN   cakes ck ON ck.id = ci.cake_id
            WHERE  ci.cart_id = %s
        """, (cart_id,))
        cart_items = cur.fetchall()
        total = sum(row[1] * row[5] for row in cart_items)  # qty * price

    cur.close()
    return render_template('cart.html',
                           cart_items=cart_items,
                           total=total,
                           cart_count=len(cart_items))


@app.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    """Add a cake to the cart."""
    cake_id  = int(request.form['cake_id'])
    quantity = int(request.form.get('quantity', 1))
    size     = request.form.get('size', '1kg')
    flavour  = request.form.get('flavour', 'Vanilla')

    cur = mysql.connection.cursor()

    # Ensure the user has a cart row
    cur.execute("SELECT id FROM cart WHERE user_id = %s", (session['user_id'],))
    cart_row = cur.fetchone()

    if not cart_row:
        cur.execute("INSERT INTO cart (user_id) VALUES (%s)", (session['user_id'],))
        mysql.connection.commit()
        cur.execute("SELECT id FROM cart WHERE user_id = %s", (session['user_id'],))
        cart_row = cur.fetchone()

    cart_id = cart_row[0]

    # If this cake+size+flavour combo is already in the cart, increment quantity
    cur.execute("""
        SELECT id, quantity FROM cart_items
        WHERE cart_id = %s AND cake_id = %s AND size = %s AND flavour = %s
    """, (cart_id, cake_id, size, flavour))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE cart_items SET quantity = quantity + %s
            WHERE id = %s
        """, (quantity, existing[0]))
    else:
        cur.execute("""
            INSERT INTO cart_items (cart_id, cake_id, quantity, size, flavour)
            VALUES (%s, %s, %s, %s, %s)
        """, (cart_id, cake_id, quantity, size, flavour))

    mysql.connection.commit()
    cur.close()
    flash('Cake added to cart! 🎂', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    """Update quantity of a cart item."""
    item_id  = int(request.form['item_id'])
    quantity = int(request.form['quantity'])

    cur = mysql.connection.cursor()
    if quantity < 1:
        cur.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
    else:
        cur.execute("UPDATE cart_items SET quantity = %s WHERE id = %s",
                    (quantity, item_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def cart_remove(item_id):
    """Remove an item from the cart."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
    mysql.connection.commit()
    cur.close()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))


# ── Checkout & Orders ────────────────────────────────────────────────────────

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page – collect delivery details and place order."""
    cur = mysql.connection.cursor()

    # Fetch cart items first
    cur.execute("SELECT id FROM cart WHERE user_id = %s", (session['user_id'],))
    cart_row = cur.fetchone()

    if not cart_row:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    cart_id = cart_row[0]
    cur.execute("""
        SELECT ci.id, ci.quantity, ci.size, ci.flavour,
               ck.name, ck.price, ck.image_url, ck.id AS cake_id
        FROM   cart_items ci
        JOIN   cakes ck ON ck.id = ci.cake_id
        WHERE  ci.cart_id = %s
    """, (cart_id,))
    cart_items = cur.fetchall()

    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    total = sum(row[1] * row[5] for row in cart_items)

    if request.method == 'POST':
        full_name     = request.form['full_name'].strip()
        phone         = request.form['phone'].strip()
        address       = request.form['address'].strip()
        delivery_date = request.form['delivery_date']

        if not all([full_name, phone, address, delivery_date]):
            flash('Please fill in all delivery details.', 'danger')
            return render_template('checkout.html',
                                   cart_items=cart_items,
                                   total=total,
                                   cart_count=get_cart_count())

        # Create the order record
        cur.execute("""
            INSERT INTO orders
                (user_id, full_name, phone, address, delivery_date, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (session['user_id'], full_name, phone, address, delivery_date, total))
        mysql.connection.commit()

        order_id = cur.lastrowid

        # Copy each cart item into order_items (price snapshot)
        for item in cart_items:
            # item: (ci.id, qty, size, flavour, cake_name, price, image_url, cake_id)
            cur.execute("""
                INSERT INTO order_items
                    (order_id, cake_id, cake_name, price, quantity, size, flavour)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (order_id, item[7], item[4], item[5], item[1], item[2], item[3]))

        # Clear the cart
        cur.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
        mysql.connection.commit()
        cur.close()

        flash('Order placed successfully! 🎉 Thank you for shopping with Sweet Cravings.', 'success')
        return redirect(url_for('orders'))

    cur.close()
    return render_template('checkout.html',
                           cart_items=cart_items,
                           total=total,
                           cart_count=get_cart_count())


@app.route('/orders')
@login_required
def orders():
    """Customer order history page."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM orders
        WHERE  user_id = %s
        ORDER  BY created_at DESC
    """, (session['user_id'],))
    all_orders = cur.fetchall()

    # Fetch items for each order
    orders_with_items = []
    for order in all_orders:
        cur.execute("""
            SELECT * FROM order_items WHERE order_id = %s
        """, (order[0],))
        items = cur.fetchall()
        orders_with_items.append({'order': order, 'items': items})

    cur.close()
    return render_template('orders.html',
                           orders=orders_with_items,
                           cart_count=get_cart_count())


# ── Admin Routes ─────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cur.fetchone()
        cur.close()

        if admin and bcrypt.checkpw(password.encode('utf-8'), admin[3].encode('utf-8')):
            session['admin_id']   = admin[0]
            session['admin_name'] = admin[1]
            flash(f'Welcome, {admin[1]}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id',   None)
    session.pop('admin_name', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with summary statistics."""
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM cakes")
    total_cakes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'Cancelled'")
    total_sales = cur.fetchone()[0]

    cur.execute("""
        SELECT o.*, u.full_name AS customer_name
        FROM   orders o
        JOIN   users u ON u.id = o.user_id
        ORDER  BY o.created_at DESC
        LIMIT  5
    """)
    recent_orders = cur.fetchall()

    cur.execute("""
        SELECT status, COUNT(*) as cnt
        FROM   orders
        GROUP  BY status
    """)
    status_counts = cur.fetchall()

    cur.close()
    return render_template('admin/dashboard.html',
                           total_cakes=total_cakes,
                           total_customers=total_customers,
                           total_orders=total_orders,
                           total_sales=total_sales,
                           recent_orders=recent_orders,
                           status_counts=status_counts)


@app.route('/admin/cakes')
@admin_required
def admin_cakes():
    """List all cakes in admin panel."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.*, cat.name AS category_name
        FROM   cakes c
        JOIN   categories cat ON cat.id = c.category_id
        ORDER  BY c.id DESC
    """)
    cakes_list = cur.fetchall()

    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    cur.close()
    return render_template('admin/cakes.html',
                           cakes=cakes_list,
                           categories=categories)


@app.route('/admin/cake/add', methods=['POST'])
@admin_required
def admin_cake_add():
    """Add a new cake from admin panel."""
    name        = request.form['name'].strip()
    category_id = request.form['category_id']
    description = request.form['description'].strip()
    price       = float(request.form['price'])
    sizes       = request.form['sizes'].strip()
    flavours    = request.form['flavours'].strip()
    is_featured = 1 if request.form.get('is_featured') else 0
    stock       = int(request.form.get('stock', 100))

    image_url = 'default_cake.jpg'
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename  = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = filename

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO cakes
            (category_id, name, description, price, image_url,
             available_sizes, available_flavours, is_featured, stock)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (category_id, name, description, price, image_url,
          sizes, flavours, is_featured, stock))
    mysql.connection.commit()
    cur.close()
    flash('New cake added successfully! 🎂', 'success')
    return redirect(url_for('admin_cakes'))


@app.route('/admin/cake/edit/<int:cake_id>', methods=['GET', 'POST'])
@admin_required
def admin_cake_edit(cake_id):
    """Edit an existing cake."""
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name        = request.form['name'].strip()
        category_id = request.form['category_id']
        description = request.form['description'].strip()
        price       = float(request.form['price'])
        sizes       = request.form['sizes'].strip()
        flavours    = request.form['flavours'].strip()
        is_featured = 1 if request.form.get('is_featured') else 0
        stock       = int(request.form.get('stock', 100))

        # Fetch current image_url
        cur.execute("SELECT image_url FROM cakes WHERE id = %s", (cake_id,))
        current = cur.fetchone()
        image_url = current[0] if current else 'default_cake.jpg'

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename  = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = filename

        cur.execute("""
            UPDATE cakes SET
                category_id=%s, name=%s, description=%s, price=%s,
                image_url=%s, available_sizes=%s, available_flavours=%s,
                is_featured=%s, stock=%s
            WHERE id=%s
        """, (category_id, name, description, price, image_url,
              sizes, flavours, is_featured, stock, cake_id))
        mysql.connection.commit()
        cur.close()
        flash('Cake updated successfully!', 'success')
        return redirect(url_for('admin_cakes'))

    cur.execute("SELECT * FROM cakes WHERE id = %s", (cake_id,))
    cake = cur.fetchone()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.close()
    return render_template('admin/edit_cake.html', cake=cake, categories=categories)


@app.route('/admin/cake/delete/<int:cake_id>', methods=['POST'])
@admin_required
def admin_cake_delete(cake_id):
    """Delete a cake from the database."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cakes WHERE id = %s", (cake_id,))
    mysql.connection.commit()
    cur.close()
    flash('Cake deleted.', 'info')
    return redirect(url_for('admin_cakes'))


@app.route('/admin/orders')
@admin_required
def admin_orders():
    """View all customer orders."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT o.*, u.full_name AS customer_name, u.email AS customer_email
        FROM   orders o
        JOIN   users u ON u.id = o.user_id
        ORDER  BY o.created_at DESC
    """)
    all_orders = cur.fetchall()

    orders_with_items = []
    for order in all_orders:
        cur.execute("SELECT * FROM order_items WHERE order_id = %s", (order[0],))
        items = cur.fetchall()
        orders_with_items.append({'order': order, 'items': items})

    cur.close()
    return render_template('admin/orders.html', orders=orders_with_items)


@app.route('/admin/order/status/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_status(order_id):
    """Update the status of an order."""
    new_status = request.form['status']
    valid = ['Pending', 'Confirmed', 'Baking', 'Out for Delivery', 'Delivered', 'Cancelled']
    if new_status not in valid:
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin_orders'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    mysql.connection.commit()
    cur.close()
    flash(f'Order #{order_id} status updated to "{new_status}".', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/admin/customers')
@admin_required
def admin_customers():
    """View all registered customers."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.*, COUNT(o.id) AS total_orders
        FROM   users u
        LEFT   JOIN orders o ON o.user_id = u.id
        GROUP  BY u.id
        ORDER  BY u.created_at DESC
    """)
    customers = cur.fetchall()
    cur.close()
    return render_template('admin/customers.html', customers=customers)


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)
