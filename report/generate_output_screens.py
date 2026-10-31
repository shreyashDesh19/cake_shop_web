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
    
    for el in elements:
        t = el['type']
        if t == 'rect':
            ax.add_patch(patches.Rectangle((el['x'], el['y']), el['w'], el['h'], facecolor=el.get('bg', 'white'), edgecolor=el.get('border', '#E2E8F0'), lw=el.get('lw', 1)))
        elif t == 'text':
            ax.text(el['x'], el['y'], el['text'], fontsize=el.get('size', 10), fontweight=el.get('weight', 'normal'), color=el.get('color', '#1E293B'), ha=el.get('ha', 'left'), va=el.get('va', 'center'))
            
    plt.tight_layout()
    plt.savefig(os.path.join(assets, filename))
    plt.close()

# Fig 5.1: Homepage Hero & Category Grid
make_ui_mockup('fig5_1_home.png', 'Home Page and Collections', [
    {'type': 'rect', 'x': 0.6, 'y': 3.6, 'w': 8.8, 'h': 2.3, 'bg': '#FDF2F8', 'border': '#F4A7B9', 'lw': 1.5},
    {'type': 'text', 'x': 5.0, 'y': 5.2, 'text': 'Baked with Love, Crafted for Joy', 'size': 16, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'text', 'x': 5.0, 'y': 4.6, 'text': 'Handcrafted artisan cakes, premium Belgian chocolates, and same-day delivery.', 'size': 10, 'color': '#78716C', 'ha': 'center'},
    {'type': 'rect', 'x': 3.8, 'y': 3.9, 'w': 2.4, 'h': 0.5, 'bg': '#5C3317'},
    {'type': 'text', 'x': 5.0, 'y': 4.15, 'text': 'EXPLORE ALL CAKES', 'size': 9, 'weight': 'bold', 'color': '#FFF8F0', 'ha': 'center'},
    
    # Category Pills
    {'type': 'text', 'x': 5.0, 'y': 3.1, 'text': 'Explore By Category', 'size': 12, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 0.6, 'y': 1.0, 'w': 1.6, 'h': 1.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 1.4, 'y': 1.8, 'text': 'Birthday\nCakes', 'size': 9, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 2.4, 'y': 1.0, 'w': 1.6, 'h': 1.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 3.2, 'y': 1.8, 'text': 'Chocolate\nSpecial', 'size': 9, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 4.2, 'y': 1.0, 'w': 1.6, 'h': 1.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 5.0, 'y': 1.8, 'text': 'Wedding\nTiers', 'size': 9, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 6.0, 'y': 1.0, 'w': 1.6, 'h': 1.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 6.8, 'y': 1.8, 'text': 'Black\nForest', 'size': 9, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    {'type': 'rect', 'x': 7.8, 'y': 1.0, 'w': 1.6, 'h': 1.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 8.6, 'y': 1.8, 'text': 'Custom\nCelebrations', 'size': 9, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'}
])

# Fig 5.2: Product Catalog & Dynamic Filter View
make_ui_mockup('fig5_2_catalog.png', 'Browse All Cakes', [
    {'type': 'rect', 'x': 0.6, 'y': 5.1, 'w': 5.8, 'h': 0.6, 'bg': 'white', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 0.8, 'y': 5.4, 'text': 'Search: "chocolate"... (Live Query Match)', 'size': 9, 'color': '#44403C'},
    {'type': 'rect', 'x': 6.6, 'y': 5.1, 'w': 2.8, 'h': 0.6, 'bg': 'white', 'border': '#D6D3D1'},
    {'type': 'text', 'x': 6.8, 'y': 5.4, 'text': 'Category: All Cakes [v]', 'size': 9, 'color': '#44403C'},
    
    # Card 1
    {'type': 'rect', 'x': 0.6, 'y': 1.0, 'w': 2.8, 'h': 3.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'rect', 'x': 0.6, 'y': 2.7, 'w': 2.8, 'h': 2.0, 'bg': '#FEF3C7'},
    {'type': 'text', 'x': 2.0, 'y': 3.7, 'text': '[Chocolate Truffle]', 'size': 9.5, 'color': '#92400E', 'ha': 'center'},
    {'type': 'text', 'x': 0.8, 'y': 2.3, 'text': 'Chocolate Truffle', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 0.8, 'y': 1.9, 'text': 'Rich Dutch cocoa ganache', 'size': 7.5, 'color': '#78716C'},
    {'type': 'text', 'x': 0.8, 'y': 1.4, 'text': 'Rs. 699.00', 'size': 10, 'weight': 'bold', 'color': '#5C3317'},
    
    # Card 2
    {'type': 'rect', 'x': 3.6, 'y': 1.0, 'w': 2.8, 'h': 3.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'rect', 'x': 3.6, 'y': 2.7, 'w': 2.8, 'h': 2.0, 'bg': '#FCE7F3'},
    {'type': 'text', 'x': 5.0, 'y': 3.7, 'text': '[Black Forest]', 'size': 9.5, 'color': '#9D174D', 'ha': 'center'},
    {'type': 'text', 'x': 3.8, 'y': 2.3, 'text': 'Black Forest Gateau', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 3.8, 'y': 1.9, 'text': 'Cherries, whipped cream & flakes', 'size': 7.5, 'color': '#78716C'},
    {'type': 'text', 'x': 3.8, 'y': 1.4, 'text': 'Rs. 649.00', 'size': 10, 'weight': 'bold', 'color': '#5C3317'},
    
    # Card 3
    {'type': 'rect', 'x': 6.6, 'y': 1.0, 'w': 2.8, 'h': 3.7, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'rect', 'x': 6.6, 'y': 2.7, 'w': 2.8, 'h': 2.0, 'bg': '#DCFCE7'},
    {'type': 'text', 'x': 8.0, 'y': 3.7, 'text': '[Red Velvet]', 'size': 9.5, 'color': '#166534', 'ha': 'center'},
    {'type': 'text', 'x': 6.8, 'y': 2.3, 'text': 'Red Velvet Royal', 'size': 9.5, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 6.8, 'y': 1.9, 'text': 'Cream cheese & moist crumb', 'size': 7.5, 'color': '#78716C'},
    {'type': 'text', 'x': 6.8, 'y': 1.4, 'text': 'Rs. 799.00', 'size': 10, 'weight': 'bold', 'color': '#5C3317'}
])

# Fig 5.3: Customer Order History View
make_ui_mockup('fig5_3_orders.png', 'Customer Order History and Tracking', [
    {'type': 'rect', 'x': 0.8, 'y': 1.0, 'w': 8.4, 'h': 4.8, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 1.2, 'y': 5.3, 'text': 'My Orders (Order History)', 'size': 13, 'weight': 'bold', 'color': '#5C3317'},
    # Order card 1
    {'type': 'rect', 'x': 1.2, 'y': 3.3, 'w': 7.6, 'h': 1.6, 'bg': '#FFFBF7', 'border': '#F4A7B9'},
    {'type': 'text', 'x': 1.5, 'y': 4.5, 'text': 'Order #101  |  Placed on: 31 Oct 2026', 'size': 10, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'rect', 'x': 6.8, 'y': 4.3, 'w': 1.8, 'h': 0.45, 'bg': '#FEF3C7', 'border': '#F59E0B'},
    {'type': 'text', 'x': 7.7, 'y': 4.52, 'text': 'Status: Baking', 'size': 8.5, 'weight': 'bold', 'color': '#B45309', 'ha': 'center'},
    {'type': 'text', 'x': 1.5, 'y': 3.9, 'text': 'Items: Chocolate Truffle (1kg, Dark Choc) x 1', 'size': 9, 'color': '#44403C'},
    {'type': 'text', 'x': 1.5, 'y': 3.5, 'text': 'Delivery Date: 02 Nov 2026  |  Total: Rs. 699.00 (Cash on Delivery)', 'size': 8.5, 'color': '#78716C'},
    
    # Order card 2
    {'type': 'rect', 'x': 1.2, 'y': 1.4, 'w': 7.6, 'h': 1.6, 'bg': '#FFFBF7', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 1.5, 'y': 2.6, 'text': 'Order #98  |  Placed on: 24 Oct 2026', 'size': 10, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'rect', 'x': 6.8, 'y': 2.4, 'w': 1.8, 'h': 0.45, 'bg': '#DCFCE7', 'border': '#16A34A'},
    {'type': 'text', 'x': 7.7, 'y': 2.62, 'text': 'Status: Delivered', 'size': 8.5, 'weight': 'bold', 'color': '#166534', 'ha': 'center'},
    {'type': 'text', 'x': 1.5, 'y': 2.0, 'text': 'Items: Butterscotch Supreme (0.5kg) x 1', 'size': 9, 'color': '#44403C'},
    {'type': 'text', 'x': 1.5, 'y': 1.6, 'text': 'Delivered on: 25 Oct 2026  |  Total: Rs. 499.00 (Cash on Delivery)', 'size': 8.5, 'color': '#78716C'}
])

# Fig 5.4: Admin Dashboard & Analytics
make_ui_mockup('fig5_4_admin_dashboard.png', 'Admin Dashboard and Management Portal', [
    # Top Stat Cards
    {'type': 'rect', 'x': 0.6, 'y': 4.4, 'w': 2.0, 'h': 1.4, 'bg': 'white', 'border': '#F4A7B9', 'lw': 1.5},
    {'type': 'text', 'x': 1.6, 'y': 5.4, 'text': 'Total Cakes', 'size': 8.5, 'color': '#78716C', 'ha': 'center'},
    {'type': 'text', 'x': 1.6, 'y': 4.8, 'text': '12', 'size': 18, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    
    {'type': 'rect', 'x': 2.9, 'y': 4.4, 'w': 2.0, 'h': 1.4, 'bg': 'white', 'border': '#5C3317', 'lw': 1.5},
    {'type': 'text', 'x': 3.9, 'y': 5.4, 'text': 'Customers', 'size': 8.5, 'color': '#78716C', 'ha': 'center'},
    {'type': 'text', 'x': 3.9, 'y': 4.8, 'text': '28', 'size': 18, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    
    {'type': 'rect', 'x': 5.2, 'y': 4.4, 'w': 2.0, 'h': 1.4, 'bg': 'white', 'border': '#E8739A', 'lw': 1.5},
    {'type': 'text', 'x': 6.2, 'y': 5.4, 'text': 'Total Orders', 'size': 8.5, 'color': '#78716C', 'ha': 'center'},
    {'type': 'text', 'x': 6.2, 'y': 4.8, 'text': '45', 'size': 18, 'weight': 'bold', 'color': '#5C3317', 'ha': 'center'},
    
    {'type': 'rect', 'x': 7.5, 'y': 4.4, 'w': 2.0, 'h': 1.4, 'bg': 'white', 'border': '#16A34A', 'lw': 1.5},
    {'type': 'text', 'x': 8.5, 'y': 5.4, 'text': 'Total Revenue', 'size': 8.5, 'color': '#78716C', 'ha': 'center'},
    {'type': 'text', 'x': 8.5, 'y': 4.8, 'text': 'Rs. 38,450', 'size': 14, 'weight': 'bold', 'color': '#166534', 'ha': 'center'},
    
    # Recent Orders Table
    {'type': 'rect', 'x': 0.6, 'y': 1.0, 'w': 8.8, 'h': 3.1, 'bg': 'white', 'border': '#E2E8F0'},
    {'type': 'text', 'x': 1.0, 'y': 3.7, 'text': 'Recent Customer Orders & Status Management', 'size': 11, 'weight': 'bold', 'color': '#5C3317'},
    {'type': 'text', 'x': 1.0, 'y': 3.1, 'text': '#101 | Shreyash Deshmukh | Rs. 699.00 | Date: 31-Oct-2026 | Status: [Baking v] [Update]', 'size': 8.5, 'color': '#1E293B'},
    {'type': 'text', 'x': 1.0, 'y': 2.5, 'text': '#100 | Rohan Patil      | Rs. 1,298.00 | Date: 30-Oct-2026 | Status: [Confirmed v] [Update]', 'size': 8.5, 'color': '#1E293B'},
    {'type': 'text', 'x': 1.0, 'y': 1.9, 'text': '#99  | Sneha Kulkarni   | Rs. 849.00 | Date: 29-Oct-2026 | Status: [Out for Delivery v] [Update]', 'size': 8.5, 'color': '#1E293B'},
    {'type': 'text', 'x': 1.0, 'y': 1.3, 'text': '#98  | Amit Sharma      | Rs. 499.00 | Date: 28-Oct-2026 | Status: [Delivered v] [Update]', 'size': 8.5, 'color': '#1E293B'}
])

# Fig 5.5: Mobile Responsive View
fig, ax = plt.subplots(figsize=(6, 8), dpi=200)
ax.set_xlim(0, 6)
ax.set_ylim(0, 9)
ax.axis('off')

# Phone Frame
ax.add_patch(patches.FancyBboxPatch((0.5, 0.4), 5.0, 8.2, boxstyle='round,pad=0.2', facecolor='#FFF8F0', edgecolor='#1E293B', lw=3))
ax.add_patch(patches.Rectangle((2.3, 8.3), 1.4, 0.2, facecolor='#1E293B'))

# Header
ax.add_patch(patches.Rectangle((0.5, 7.3), 5.0, 0.8, facecolor='#5C3317'))
ax.text(3.0, 7.7, 'Sweet Cravings [=]', ha='center', va='center', color='#FFF8F0', fontsize=12, fontweight='bold')

# Mobile Hero
ax.add_patch(patches.Rectangle((0.8, 5.7), 4.4, 1.4, facecolor='#FDF2F8', edgecolor='#F4A7B9'))
ax.text(3.0, 6.6, 'Delicious Cakes\nDelivered Fresh!', ha='center', va='center', color='#5C3317', fontsize=11, fontweight='bold')
ax.text(3.0, 5.95, '[ORDER ONLINE NOW]', ha='center', va='center', color='#E8739A', fontsize=9, fontweight='bold')

# Mobile Cake Card
ax.add_patch(patches.Rectangle((0.8, 3.2), 4.4, 2.3, facecolor='white', edgecolor='#E2E8F0'))
ax.text(3.0, 4.8, '[Cake Preview]', ha='center', va='center', color='#78716C', fontsize=9)
ax.text(1.1, 4.1, 'Chocolate Truffle', fontsize=10, fontweight='bold', color='#5C3317')
ax.text(1.1, 3.7, '1kg / Dark Choc - Rs. 699.00', fontsize=8.5, color='#44403C')
ax.add_patch(patches.Rectangle((3.4, 3.4), 1.6, 0.5, facecolor='#F4A7B9'))
ax.text(4.2, 3.65, 'Add to Cart', ha='center', va='center', color='#5C3317', fontsize=8, fontweight='bold')

# Mobile Bottom Nav
ax.add_patch(patches.Rectangle((0.5, 0.6), 5.0, 0.7, facecolor='white', edgecolor='#CBD5E1'))
ax.text(1.1, 0.95, 'Home', ha='center', fontsize=8, color='#5C3317')
ax.text(2.3, 0.95, 'Cakes', ha='center', fontsize=8, color='#5C3317')
ax.text(3.6, 0.95, 'Cart (1)', ha='center', fontsize=8, fontweight='bold', color='#E8739A')
ax.text(4.9, 0.95, 'Orders', ha='center', fontsize=8, color='#5C3317')

plt.tight_layout()
plt.savefig(os.path.join(assets, 'fig5_5_mobile.png'))
plt.close()

print('Output screens generated successfully')
