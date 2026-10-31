-- =============================================================
-- Sweet Cravings Cake Shop – Database Schema
-- Database: cake_shop_db
-- =============================================================

CREATE DATABASE IF NOT EXISTS cake_shop_db;
USE cake_shop_db;

-- ----------------------------
-- Table: admins
-- Stores admin login credentials
-- ----------------------------
CREATE TABLE IF NOT EXISTS admins (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,         -- bcrypt hashed
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Table: users
-- Stores customer accounts
-- ----------------------------
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    phone       VARCHAR(15),
    password    VARCHAR(255) NOT NULL,         -- bcrypt hashed
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Table: categories
-- Cake categories (Birthday, Wedding, etc.)
-- ----------------------------
CREATE TABLE IF NOT EXISTS categories (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL UNIQUE,
    icon  VARCHAR(50) DEFAULT 'bi-cake2'       -- Bootstrap icon name
);

-- ----------------------------
-- Table: cakes
-- Cake catalog managed by admin
-- ----------------------------
CREATE TABLE IF NOT EXISTS cakes (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    category_id   INT NOT NULL,
    name          VARCHAR(150) NOT NULL,
    description   TEXT,
    price         DECIMAL(10,2) NOT NULL,
    image_url     VARCHAR(255) DEFAULT 'default_cake.jpg',
    available_sizes   VARCHAR(200) DEFAULT '0.5kg,1kg,1.5kg,2kg',
    available_flavours VARCHAR(300) DEFAULT 'Vanilla,Chocolate,Strawberry,Butterscotch',
    is_featured   TINYINT(1) DEFAULT 0,
    stock         INT DEFAULT 100,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ----------------------------
-- Table: cart
-- One cart per logged-in user
-- ----------------------------
CREATE TABLE IF NOT EXISTS cart (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------
-- Table: cart_items
-- Individual items inside a cart
-- ----------------------------
CREATE TABLE IF NOT EXISTS cart_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    cart_id    INT NOT NULL,
    cake_id    INT NOT NULL,
    quantity   INT NOT NULL DEFAULT 1,
    size       VARCHAR(20) DEFAULT '1kg',
    flavour    VARCHAR(50) DEFAULT 'Vanilla',
    FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
    FOREIGN KEY (cake_id) REFERENCES cakes(id) ON DELETE CASCADE
);

-- ----------------------------
-- Table: orders
-- Customer orders placed at checkout
-- ----------------------------
CREATE TABLE IF NOT EXISTS orders (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    full_name       VARCHAR(100) NOT NULL,
    phone           VARCHAR(15)  NOT NULL,
    address         TEXT NOT NULL,
    delivery_date   DATE NOT NULL,
    payment_method  VARCHAR(50) DEFAULT 'Cash on Delivery',
    total_amount    DECIMAL(10,2) NOT NULL,
    status          ENUM('Pending','Confirmed','Baking','Out for Delivery','Delivered','Cancelled')
                        DEFAULT 'Pending',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------
-- Table: order_items
-- Individual cake items inside an order
-- ----------------------------
CREATE TABLE IF NOT EXISTS order_items (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    order_id    INT NOT NULL,
    cake_id     INT NOT NULL,
    cake_name   VARCHAR(150) NOT NULL,   -- snapshot at order time
    price       DECIMAL(10,2) NOT NULL,  -- snapshot at order time
    quantity    INT NOT NULL DEFAULT 1,
    size        VARCHAR(20) DEFAULT '1kg',
    flavour     VARCHAR(50) DEFAULT 'Vanilla',
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (cake_id)  REFERENCES cakes(id)  ON DELETE CASCADE
);

-- =============================================================
-- SEED DATA
-- =============================================================

-- Default admin (password: admin123)
INSERT INTO admins (username, email, password) VALUES
('admin', 'admin@sweetcravings.com',
 '$2b$12$ytY4sOf2cYCGMfNq6QI.r.Ov9LLryir9JN.5jCtOecduET6QNM2Gy');

-- Categories
INSERT INTO categories (name, icon) VALUES
('Birthday Cakes',    'bi-balloon'),
('Chocolate Cakes',   'bi-stars'),
('Wedding Cakes',     'bi-heart'),
('Black Forest',      'bi-tree'),
('Custom Cakes',      'bi-pencil-square');

-- Sample cakes
INSERT INTO cakes
    (category_id, name, description, price, image_url, is_featured, available_sizes, available_flavours)
VALUES
-- Birthday
(1, 'Rainbow Birthday Cake',
 'A vibrant multi-layered rainbow cake perfect for celebrations, covered in smooth buttercream and colourful sprinkles.',
 699.00, 'birthday1.jpg', 1,
 '0.5kg,1kg,1.5kg,2kg', 'Vanilla,Strawberry,Butterscotch'),

(1, 'Princess Dream Cake',
 'A gorgeous pink castle cake for little princesses, decorated with edible pearls and sugar flowers.',
 899.00, 'birthday2.jpg', 0,
 '0.5kg,1kg,1.5kg,2kg', 'Vanilla,Strawberry'),

(1, 'Superhero Cake',
 'Bold and fun superhero-themed cake for kids, with action-packed decorations and rich vanilla sponge.',
 749.00, 'birthday3.jpg', 0,
 '0.5kg,1kg,1.5kg,2kg', 'Vanilla,Chocolate,Butterscotch'),

-- Chocolate
(2, 'Dark Chocolate Truffle',
 'Intensely rich dark chocolate cake with silky ganache layers and chocolate curls on top.',
 799.00, 'choco1.jpg', 1,
 '0.5kg,1kg,1.5kg,2kg', 'Dark Chocolate,Milk Chocolate'),

(2, 'Belgian Chocolate Delight',
 'Premium Belgian chocolate sponge layered with praline cream and finished with glossy chocolate drizzle.',
 949.00, 'choco2.jpg', 1,
 '0.5kg,1kg,1.5kg,2kg', 'Dark Chocolate,White Chocolate'),

(2, 'Molten Lava Cake',
 'Warm mini chocolate cakes with a gooey molten centre, served with vanilla ice cream.',
 549.00, 'choco3.jpg', 0,
 '0.5kg,1kg', 'Dark Chocolate'),

-- Wedding
(3, 'Classic White Wedding Cake',
 'Elegant three-tier white fondant wedding cake decorated with delicate sugar roses and pearls.',
 2499.00, 'wedding1.jpg', 1,
 '2kg,3kg,4kg,5kg', 'Vanilla,Strawberry,Butterscotch'),

(3, 'Rustic Floral Wedding Cake',
 'Charming semi-naked wedding cake adorned with fresh flowers and a rustic buttercream finish.',
 2999.00, 'wedding2.jpg', 0,
 '2kg,3kg,4kg,5kg', 'Vanilla,Lemon'),

-- Black Forest
(4, 'Classic Black Forest',
 'Traditional Black Forest gâteau with layers of chocolate sponge, whipped cream, and Morello cherries.',
 849.00, 'bf1.jpg', 1,
 '0.5kg,1kg,1.5kg,2kg', 'Chocolate Cherry'),

(4, 'Black Forest Cheesecake',
 'A fusion of creamy New York cheesecake and classic Black Forest flavours topped with cherry compote.',
 999.00, 'bf2.jpg', 0,
 '0.5kg,1kg,1.5kg,2kg', 'Cream Cheese,Chocolate Cherry'),

-- Custom
(5, 'Photo Print Cake',
 'Personalised cake with edible photo printing on fondant. Send us your favourite memory!',
 1199.00, 'custom1.jpg', 1,
 '0.5kg,1kg,1.5kg,2kg', 'Vanilla,Chocolate,Strawberry,Butterscotch'),

(5, 'Number / Letter Cake',
 'Trendy number or letter shaped cake made of layers of pastry and cream, customised to your choice.',
 1399.00, 'custom2.jpg', 0,
 '1kg,1.5kg,2kg', 'Vanilla,Chocolate,Strawberry');
