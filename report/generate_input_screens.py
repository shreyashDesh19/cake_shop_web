import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

assets = r'C:\Users\Admin\.gemini\antigravity\scratch\sweet_cravings\report\assets'
os.makedirs(assets, exist_ok=True)

def make_ui_mockup(filename, title, elements):
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Browser Window Chrome
    ax.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 6.6, facecolor='#FFF8F0', edgecolor='#5C3317', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 6.2), 9.6, 0.6, facecolor='#5C3317'))
    
    # Traffic dots
    for i, c in enumerate(['#EF4444', '#FBBF24', '#10B981']):
        ax.add_patch(plt.Circle((0.5 + i*0.25, 6.5), 0.08, color=c))
        
    ax.text(5.0, 6.5, f'Sweet Cravings - {title}', ha='center', va='center', color='#FFF8F0', fontsize=11, fontweight='bold')
    
    # Content rendering
    for el in elements:
        t = el['type']
        if t == 'rect':
            ax.add_patch(patches.Rectangle((el['x'], el['y']), el['w'], el['h'], facecolor=el.get('bg', 'white'), edgecolor=el.get('border', '#E2E8F0'), lw=el.get('lw', 1)))
        elif t == 'text':
            ax.text(el['x'], el['y'], el['text'], fontsize=el.get('size', 10), fontweight=el.get('weight', 'normal'), color=el.get('color', '#1E293B'), ha=el.get('ha', 'left'), va=el.get('va', 'center'))
            
    plt.tight_layout()
    plt.savefig(os.path.join(assets, filename))
    plt.close()

# 1. Fig 4.1: Customer Registration & Login Screen
make_ui_mockup('fig4_1_login_reg.png', 'Customer Account Portal', [
    {'type': 'rect', 'x': 2.2, 'y': 1.0, 'w': 5.6, 'h': 4.8, 'bg': 'white', 'border': '#F4A7B9', 'lw': 2},
    {'type': 'text', 'x': 5.0, 'y': 5.3, 'text': 'Welcome to Sweet Cravings', 'size': 14, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'text', 'x': 5.0, 'y': 4.8, 'text': 'Customer Login and Order Management', 'size': 9.5, 'color': '#78716C', 'ha': 'center'},
    {'type': 'rect', 'x': 2.8, 'y': 3.8, 'w': 4.4, 'h': 0.55, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 3.0, 'y': 4.07, 'text': 'Email: customer@example.com', 'size': 9, 'color': '#44403C'},
    {'type': 'rect', 'x': 2.8, 'y': 2.8, 'w': 4.4, 'h': 0.55, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 3.0, 'y': 3.07, 'text': 'Password: ************', 'size': 9, 'color': '#44403C'},
    {'type': 'rect', 'x': 2.8, 'y': 1.8, 'w': 4.4, 'h': 0.6, 'bg': '#F4A7B9', 'border': '#E8739A', 'lw': 1.5},
    {'type': 'text', 'x': 5.0, 'y': 2.1, 'text': 'LOGIN TO YOUR ACCOUNT', 'size': 10, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'text', 'x': 5.0, 'y': 1.3, 'text': "Don't have an account? Register Here", 'size': 8.5, 'color': '#5C3317', 'ha': 'center'}
])

# 2. Fig 4.2: Cake Detail & Customization Screen
make_ui_mockup('fig4_2_cake_detail.png', 'Product Detail and Customization', [
    {'type': 'rect', 'x': 0.8, 'y': 1.2, 'w': 4.0, 'h': 4.4, 'bg': '#FCE7F3', 'border': '#F4A7B9'},
    {'type': 'text', 'x': 2.8, 'y': 3.4, 'text': '[Cake Visual View]\nChocolate Truffle Cake', 'size': 12, 'color': '#5C3317', 'ha': 'center'},
    {'type': 'text', 'x': 5.3, 'y': 5.2, 'text': 'Chocolate Truffle Delight', 'size': 15, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 5.3, 'y': 4.7, 'text': 'Category: Chocolate Cakes | Rating: 4.9/5.0', 'size': 8.5, 'color': '#E8739A'},
    {'type': 'text', 'x': 5.3, 'y': 4.2, 'text': 'Rs. 699.00 onwards', 'size': 13, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 5.3, 'y': 3.6, 'text': 'Select Size: [ 0.5kg ]  [ 1kg (Selected) ]  [ 2kg ]', 'size': 9, 'color': '#44403C'},
    {'type': 'text', 'x': 5.3, 'y': 3.0, 'text': 'Select Flavour: [ Dark Chocolate ]  [ Milk Chocolate ]', 'size': 9, 'color': '#44403C'},
    {'type': 'text', 'x': 5.3, 'y': 2.4, 'text': 'Quantity:  [ - ]  1  [ + ]', 'size': 9.5, 'color': '#44403C'},
    {'type': 'rect', 'x': 5.3, 'y': 1.4, 'w': 3.8, 'h': 0.65, 'bg': '#F4A7B9', 'border': '#E8739A', 'lw': 1.5},
    {'type': 'text', 'x': 7.2, 'y': 1.72, 'text': 'ADD TO SHOPPING CART', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'}
])

# 3. Fig 4.3: Shopping Cart Management
make_ui_mockup('fig4_3_cart.png', 'Your Shopping Cart', [
    {'type': 'rect', 'x': 0.8, 'y': 1.2, 'w': 5.6, 'h': 4.4, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 1.2, 'y': 5.1, 'text': 'Item', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 3.4, 'y': 5.1, 'text': 'Size / Flavour', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 4.8, 'y': 5.1, 'text': 'Qty', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 5.8, 'y': 5.1, 'text': 'Total', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    # Item 1
    {'type': 'text', 'x': 1.2, 'y': 4.3, 'text': 'Chocolate Truffle', 'size': 9, 'color': '#1E293B'},
    {'type': 'text', 'x': 3.4, 'y': 4.3, 'text': '1kg | Dark Choc', 'size': 8.5, 'color': '#64748B'},
    {'type': 'text', 'x': 4.8, 'y': 4.3, 'text': '[ - ] 1 [ + ]', 'size': 8.5, 'color': '#1E293B'},
    {'type': 'text', 'x': 5.8, 'y': 4.3, 'text': 'Rs. 699.00', 'size': 9, 'weight': 'bold', 'color': '#5C3317'},
    # Item 2
    {'type': 'text', 'x': 1.2, 'y': 3.5, 'text': 'Red Velvet Heart', 'size': 9, 'color': '#1E293B'},
    {'type': 'text', 'x': 3.4, 'y': 3.5, 'text': '0.5kg | Cream Ch.', 'size': 8.5, 'color': '#64748B'},
    {'type': 'text', 'x': 4.8, 'y': 3.5, 'text': '[ - ] 1 [ + ]', 'size': 8.5, 'color': '#1E293B'},
    {'type': 'text', 'x': 5.8, 'y': 3.5, 'text': 'Rs. 499.00', 'size': 9, 'weight': 'bold', 'color': '#5C3317'},
    # Summary Box
    {'type': 'rect', 'x': 6.8, 'y': 1.2, 'w': 2.6, 'h': 4.4, 'bg': 'white', 'border': '#F4A7B9', 'lw': 1.5},
    {'type': 'text', 'x': 8.1, 'y': 5.1, 'text': 'Order Summary', 'size': 11, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'text', 'x': 7.1, 'y': 4.2, 'text': 'Subtotal: Rs. 1,198.00', 'size': 9, 'color': '#44403C'},
    {'type': 'text', 'x': 7.1, 'y': 3.6, 'text': 'Delivery: FREE', 'size': 9, 'color': '#16A34A'},
    {'type': 'text', 'x': 7.1, 'y': 2.9, 'text': 'Total: Rs. 1,198.00', 'size': 11, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'rect', 'x': 7.0, 'y': 1.6, 'w': 2.2, 'h': 0.6, 'bg': '#5C3317'},
    {'type': 'text', 'x': 8.1, 'y': 1.9, 'text': 'CHECKOUT', 'size': 8, 'weight': 'bold', 'color': '#FFF8F0', 'ha': 'center'}
])

# 4. Fig 4.4: Checkout & Cash on Delivery Form
make_ui_mockup('fig4_4_checkout.png', 'Checkout and Delivery Details', [
    {'type': 'rect', 'x': 1.0, 'y': 0.8, 'w': 8.0, 'h': 5.0, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 5.0, 'y': 5.4, 'text': 'Delivery and Contact Information', 'size': 13, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 1.5, 'y': 4.3, 'w': 3.3, 'h': 0.5, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 1.6, 'y': 4.55, 'text': 'Full Name: Shreyash Deshmukh', 'size': 8.5, 'color': '#44403C'},
    {'type': 'rect', 'x': 5.2, 'y': 4.3, 'w': 3.3, 'h': 0.5, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 5.3, 'y': 4.55, 'text': 'Phone: +91 9876543210', 'size': 8.5, 'color': '#44403C'},
    {'type': 'rect', 'x': 1.5, 'y': 3.4, 'w': 7.0, 'h': 0.65, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 1.6, 'y': 3.75, 'text': 'Delivery Address: Flat 402, Lotus Residency, Pune - 411014', 'size': 8.5, 'color': '#44403C'},
    {'type': 'rect', 'x': 1.5, 'y': 2.5, 'w': 3.3, 'h': 0.5, 'bg': '#FFFBF7', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 1.6, 'y': 2.75, 'text': 'Delivery Date: 2026-11-05', 'size': 8.5, 'color': '#44403C'},
    {'type': 'rect', 'x': 5.2, 'y': 2.5, 'w': 3.3, 'h': 0.5, 'bg': '#DCFCE7', 'border': '#16A34A'},
    {'type': 'text', 'x': 5.3, 'y': 2.75, 'text': 'Payment: Cash on Delivery (COD) [OK]', 'size': 8.5, 'weight': 'bold', 'color': '#166534'},
    {'type': 'rect', 'x': 2.5, 'y': 1.2, 'w': 5.0, 'h': 0.7, 'bg': '#F4A7B9', 'border': '#E8739A', 'lw': 1.5},
    {'type': 'text', 'x': 5.0, 'y': 1.55, 'text': 'PLACE ORDER (CASH ON DELIVERY)', 'size': 11, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'}
])

print('Input screens generated successfully')
