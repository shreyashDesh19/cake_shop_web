import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# ----------------- PAGE SETUP (Standard A4) -----------------
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

# Color Palette Constants
COLOR_DARK_BROWN = RGBColor(92, 51, 23)     # #5C3317
COLOR_LIGHT_BROWN = RGBColor(140, 70, 30)
COLOR_TEXT_MAIN = RGBColor(40, 40, 40)
COLOR_MUTED = RGBColor(100, 100, 100)
HEX_LIGHT_BG = "FFF8F0"
HEX_BORDER = "F4A7B9"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.bold = True
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = COLOR_DARK_BROWN
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_LIGHT_BROWN
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_DARK_BROWN
    return p

def add_body(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10.5)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_DARK_BROWN
    r = p.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_TEXT_MAIN
    r.italic = italic
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10.5)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_DARK_BROWN
    r = p.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_TEXT_MAIN
    return p

def add_image_safe(path, width=5.5, caption=""):
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.add_run().add_picture(path, width=Inches(width))
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r = p_cap.add_run(caption)
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.italic = True
            r.font.color.rgb = COLOR_MUTED

def style_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "5C3317")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 248, 240)
    
    # Data rows
    for r_idx, row in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = "FFF8F0" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            p = row_cells[c_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_TEXT_MAIN

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

assets_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\sweet_cravings\report\assets"

print("Starting document assembly...")

# ==============================================================================
# COVER PAGE (PAGE 1)
# ==============================================================================
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(36)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A\nSUMMER INTERNSHIP PROJECT REPORT\nON\n")
r.font.name = 'Arial'
r.font.size = Pt(14)
r.bold = True

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(20)
r_title = p_title.add_run("“Sweet Cravings – Full-Stack Online Cake Shop & Bakery Management Web Application”")
r_title.font.name = 'Georgia'
r_title.font.size = Pt(20)
r_title.bold = True
r_title.font.color.rgb = COLOR_DARK_BROWN

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(30)
r_sub = p_sub.add_run("IN THE PARTIAL FULFILLMENT OF THE REQUIREMENT OF\nBACHELOR OF COMPUTER APPLICATION (BCA)\n(BCA ADS Honors)")
r_sub.font.name = 'Arial'
r_sub.font.size = Pt(11)
r_sub.bold = True

p_guide = doc.add_paragraph()
p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_guide.paragraph_format.space_after = Pt(30)
r_guide = p_guide.add_run("UNDER THE GUIDANCE OF\nProf. Aditi Kale\nAssistant Professor, Dept. of Computer Applications")
r_guide.font.name = 'Arial'
r_guide.font.size = Pt(12)
r_guide.bold = True
r_guide.font.color.rgb = RGBColor(180, 40, 40)

p_by = doc.add_paragraph()
p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by.paragraph_format.space_after = Pt(35)
r_by = p_by.add_run("SUBMITTED BY\nSHREYASH GOVIND DESHMUKH\nPRN: ADT24MGTB0404\nBATCH: 2023-2027")
r_by.font.name = 'Arial'
r_by.font.size = Pt(12)
r_by.bold = True

p_to = doc.add_paragraph()
p_to.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_to = p_to.add_run("SUBMITTED TO\nMIT SCHOOL OF BUSINESS AND COMPUTER APPLICATIONS, PUNE\nMIT ART DESIGN AND TECHNOLOGY UNIVERSITY, PUNE\nACADEMIC YEAR 2025-26")
r_to.font.name = 'Arial'
r_to.font.size = Pt(11)
r_to.bold = True

doc.add_page_break()

# ==============================================================================
# CERTIFICATE (PAGE 2)
# ==============================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("MIT ART DESIGN AND TECHNOLOGY UNIVERSITY\nMIT SCHOOL OF BUSINESS AND COMPUTER APPLICATIONS, PUNE\n(MIT SOB & CA), PUNE\n\nBACHELOR OF COMPUTER APPLICATIONS (BCA)\n\n")
r.font.name = 'Arial'
r.font.size = Pt(12)
r.bold = True

p_cert = doc.add_paragraph()
p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cert = p_cert.add_run("CERTIFICATE")
r_cert.font.name = 'Arial'
r_cert.font.size = Pt(16)
r_cert.bold = True
r_cert.underline = True

add_body("This is to certify that, Mr. Shreyash Govind Deshmukh (PRN: ADT24MGTB0404) has successfully submitted a Summer Internship Project (SIP) Report entitled “Sweet Cravings – Full-Stack Online Cake Shop & Bakery Management Web Application” to MIT-ADT University, Pune, for the partial fulfilment of the requirements for the award of the degree of Bachelor of Computer Applications (ADS Honors) during the academic year 2025-26.")
add_body("To the best of our knowledge and belief, we further certify that the matter presented in this project report has not been submitted for any other Degree or Diploma course in this or any other University.")

p_prn = doc.add_paragraph()
p_prn.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_prn.paragraph_format.space_before = Pt(20)
p_prn.paragraph_format.space_after = Pt(40)
r_prn = p_prn.add_run("PRN No: ADT24MGTB0404")
r_prn.bold = True
r_prn.font.size = Pt(12)

# Signatures Table
tbl_sig = doc.add_table(rows=1, cols=4)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
for c in tbl_sig.rows[0].cells:
    c.width = Inches(1.5)
tbl_sig.rows[0].cells[0].paragraphs[0].text = "Prof. Aditi Kale\nInternal Guide"
tbl_sig.rows[0].cells[1].paragraphs[0].text = "Dr. Irfan Chaugule\nHOD, BCA"
tbl_sig.rows[0].cells[2].paragraphs[0].text = "Dr. Pallavi Badre\nUG Head"
tbl_sig.rows[0].cells[3].paragraphs[0].text = "Dr. Sangita Phunde\nPrincipal"

for cell in tbl_sig.rows[0].cells:
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.bold = True

p_ex = doc.add_paragraph()
p_ex.paragraph_format.space_before = Pt(40)
p_ex.add_run("Internal Examiner Sign:  1. .....................................        2. .....................................\n\nExternal Examiner Sign:  1. .....................................        2. .....................................")

doc.add_page_break()

# ==============================================================================
# EXPERIENCE LETTER & DECLARATION (PAGE 3 & 4)
# ==============================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("ALAPO TECHNOWORLD PVT. LTD.\nDate: 08/08/2026\n\n")
r.bold = True
r.font.size = Pt(13)

p_exp = doc.add_paragraph()
p_exp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_exp = p_exp.add_run("Experience Letter")
r_exp.bold = True
r_exp.font.size = Pt(15)
r_exp.underline = True

add_body("This is to certify that Mr. Shreyash Govind Deshmukh was an Intern with us as a Software Developer from 8th June 2026 to 8th August 2026.")
add_body("During this period, he was exposed to practical industry knowledge and gained hands-on experience in full-stack web software development, Python Flask backends, MySQL relational schema modeling, responsive Bootstrap UI engineering, debugging, and end-to-end e-commerce project workflows. He worked diligently on designing and implementing commercial web platforms including the Sweet Cravings bakery e-commerce portal.")
add_body("He demonstrated keen enthusiasm in problem solving, dedication, discipline, and exemplary responsibility in all assigned technical modules.")
add_body("We wish him all the very best in his future academic and professional endeavours.\n\n")

p_hr = doc.add_paragraph()
p_hr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_hr.add_run("Mr. Vikash Kumar\nHR Manager\nAlapo Technoworld Pvt. Ltd.\nCIN: U72502MH2022PTC374409")

doc.add_page_break()

# DECLARATION
add_title("DECLARATION", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
add_body("I hereby declare that the project work entitled “Sweet Cravings – Full-Stack Online Cake Shop & Bakery Management Web Application” submitted to MIT School of Business and Computer Applications, MIT – ADT University, Pune, is a record of original work done by me under the esteemed guidance of Prof. Aditi Kale.")
add_body("This project report is submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Computer Applications (BCA ADS Honors).")
add_body("The technical content, system design, architectural models, and source code documented in this report have not been submitted to any other University or Institute for the award of any degree, diploma, or fellowship.")

p_dt = doc.add_paragraph()
p_dt.paragraph_format.space_before = Pt(40)
p_dt.add_run("Date:  31 / 10 / 2026\nPlace: Pune\n\n\n___________________________________\nSignature of Candidate\n(SHREYASH GOVIND DESHMUKH)\nPRN: ADT24MGTB0404")

doc.add_page_break()

# ACKNOWLEDGEMENT
add_title("ACKNOWLEDGEMENT", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
add_body("I would like to express my deepest gratitude to all those who have been instrumental in the successful conceptualization, architecture, and deployment of this project.")
add_body("First and foremost, I convey my heartfelt thanks to Alapo Technoworld Pvt. Ltd. and Vault of Codes for providing me with an exceptional internship opportunity and industry exposure in full-stack software development.")
add_body("I extend my profound gratitude to the Head of Department, Dr. Irfan Chaugule, and respected Principal, Dr. Sangita Phunde, for their continuous academic encouragement and for fostering a state-of-the-art learning environment at MIT School of Business and Computer Applications.")
add_body("I am deeply indebted to my internal project guide, Prof. Aditi Kale, for her invaluable guidance, rigorous reviews, patient debugging support, and continuous motivation throughout this project lifecycle.")
add_body("Finally, I thank the faculty members, laboratory staff, my family, and friends whose relentless support made this project report possible.")

p_ack_sign = doc.add_paragraph()
p_ack_sign.paragraph_format.space_before = Pt(30)
p_ack_sign.add_run("Shreyash Govind Deshmukh\nMIT School of Business and Computer Applications, Pune")

doc.add_page_break()

# ==============================================================================
# INDEX (PAGE 7 EXACT MATCHING STRUCTURE)
# ==============================================================================
add_title("INDEX", 1).alignment = WD_ALIGN_PARAGRAPH.CENTER

idx_table = doc.add_table(rows=1, cols=3)
idx_headers = ["CHAPTER", "TITLE", "PAGE NO."]
idx_widths = [2.2, 3.3, 0.9]
idx_data = [
    ["1. Introduction", "", "01 - 03"],
    ["", "1.1 Company / Bakery Profile", ""],
    ["", "1.2 Abstract", ""],
    ["", "1.3 Existing System & Challenges", ""],
    ["", "1.4 Scope of the System", ""],
    ["", "1.5 Operating Environment (HW / SW)", ""],
    ["", "1.6 Technology Used (Full-Stack)", ""],
    ["2. Proposed System", "", "04 - 05"],
    ["", "2.1 Comprehensive Feasibility Study", ""],
    ["", "2.2 Objectives of Proposed System", ""],
    ["", "2.3 E-Commerce vs Manual Counter Trade", ""],
    ["3. Analysis & Design", "", "06 - 23"],
    ["", "3.1 Software Requirements Specification (SRS)", ""],
    ["", "3.2 System Architecture (3-Tier Model)", ""],
    ["", "3.3 Table Structure & Data Dictionary (8 Tables)", ""],
    ["", "3.4 Use Case Modeling & Actor Interaction", ""],
    ["", "3.5 Component & Class Architecture", ""],
    ["", "3.6 Activity Diagram (Order Journey)", ""],
    ["", "3.7 Sequence Diagram (Cart & Order Processing)", ""],
    ["", "3.8 Relational Storage & Session Management", ""],
    ["4. Input Screens with Data", "", "24 – 27"],
    ["5. Output Screens with Data", "", "28 – 33"],
    ["6. Code Snippets (Core Logic)", "", "34 – 39"],
    ["7. Testing & Test Cases", "", "40 – 45"],
    ["8. Limitations of Proposed System", "", "46 – 49"],
    ["9. Proposed Enhancements", "", "50 – 52"],
    ["10. Conclusion", "", "53"],
    ["11. Bibliography & References", "", "54"]
]
style_table(idx_table, idx_widths, idx_headers, idx_data)

doc.add_page_break()

# ==============================================================================
# CHAPTER 1 - INTRODUCTION
# ==============================================================================
add_title("CHAPTER 1 - INTRODUCTION", 1)

add_title("1.1 Company & Enterprise Profile", 2)
add_body("Sweet Cravings Bakery & Confectionery is an artisanal, premium cake and dessert manufacturing enterprise specializing in handcrafted celebration cakes, gourmet desserts, corporate party hampers, and designer wedding confections. Headquartered with state-of-the-art kitchen studios in Pune, Maharashtra, Sweet Cravings delivers high-quality baking using certified food-grade ingredients, 100% pure dairy cream, imported Belgian cocoa, and organic flour.")
add_body("The bakery operates specialized production divisions spanning Birthday Cakes, Belgian Chocolate Specials, Multi-tiered Wedding Confections, Classic Black Forest Gateaux, and Personalized Custom Celebration Cakes. Each cake is crafted on-demand to guarantee freshness, customizable across diverse size tiers (0.5 kg, 1 kg, 1.5 kg, 2 kg) and multiple flavour infusions (Dutch Ganache, Cream Cheese, Tahitian Vanilla, Wild Berry).")
add_body("To expand commercial retail beyond local walk-in foot traffic and eliminate error-prone manual paper-register telephone order management, this full-stack web application project was conceived, designed, and deployed as a modern interactive digital marketplace with an integrated backend order management dashboard.")

add_title("1.2 Abstract", 2)
add_body("In the contemporary food-tech and artisanal retail industry, sustainable business growth relies on bridging the operational gap between creative confectionery production and digital consumer accessibility. Traditional standalone bakeries have historically struggled with order mismatches, unrecorded telephone bookings, inaccurate delivery coordination, and cumbersome walk-in catalog selections.")
add_body("“Sweet Cravings – Full-Stack Online Cake Shop & Bakery Management Web Application” was designed and engineered to completely digitize and streamline the confectionery ordering workflow. Developed with a high-performance Python Flask backend, MySQL relational database management system, and responsive Bootstrap 5 client interface styled in an appetizing pastry palette (Cream #FFF8F0, Pastel Pink #F4A7B9, Chocolate Brown #5C3317), the platform delivers a comprehensive e-commerce experience.")
add_body("Key capabilities encompass real-time cake browsing with instant multi-category filtering, dynamic size and flavour pricing calculators, automated shopping cart sessions, Cash on Delivery (COD) checkout pipelines, customer order history tracking, and an isolated administrative control portal supporting full cake catalog CRUD operations, live order status lifecycle management (Pending -> Confirmed -> Baking -> Out for Delivery -> Delivered), and business revenue analytics.")

add_title("1.3 Existing System & Operational Challenges", 2)
add_body("Prior to implementing this automated web platform, Sweet Cravings operated through traditional offline counter sales and phone-based orders. An operational audit highlighted several critical bottlenecks:")
add_bullet("Manual Counter Logbooks & Order Loss: Telephone and WhatsApp bookings were scribbled in physical paper diaries, frequently resulting in misread delivery dates, forgotten special instructions, and lost revenue during festive rushes.", "• ")
add_bullet("Lack of Real-Time Customization: Customers inquiring about weight upgrades (0.5kg to 2kg) or flavour variations had to wait for baking staff to compute quotes manually over phone calls, causing customer friction.", "• ")
add_bullet("Zero Customer Order Tracking: Patrons were unable to track the preparation status of their cakes, leading to repetitive telephone calls inquiring whether their order was currently baking or dispatched.", "• ")
add_bullet("Administrative Blind Spots: Bakery owners lacked unified reports on daily sales, inventory levels, fast-moving cake categories, and customer retention metrics.", "• ")

add_title("1.4 Scope of the System", 2)
add_body("The software engineering scope was formulated to deliver a robust, user-friendly digital marketplace tailored for students and commercial confectionery operations alike:")
add_bullet("Dynamic Multi-Category Catalog: Real-time showcase of 12+ pre-seeded artisan cakes categorized across Birthday, Chocolate, Wedding, Black Forest, and Custom Cakes.", "• ")
add_bullet("Client-Side Dynamic Pricing Calculator: Instant price re-calculation based on cake size multipliers directly within the product view using JavaScript.", "• ")
add_bullet("Dual-System Role-Based Authentication: Independent authentication workflows with bcrypt salted password hashing for retail customers and administrative bakery managers.", "• ")
add_bullet("Robust Cart & Checkout Pipeline: Relational cart management linked directly to MySQL with instant conversion to permanent order items upon Cash on Delivery (COD) placement.", "• ")
add_bullet("Executive Management Dashboard: Centralized dashboard with 4 real-time business metrics (Total Cakes, Total Customers, Total Orders, Total Revenue), dynamic order status progression, and cake CRUD controls.", "• ")

add_title("1.5 Operating Environment (Hardware & Software Requirements)", 2)
add_body("Hardware Environment:")
add_bullet("Processor: Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+ clock speed)", "• ")
add_bullet("RAM: Minimum 4 GB RAM (8 GB recommended for concurrent MySQL transactions)", "• ")
add_bullet("Hard Disk: Minimum 500 MB free space for code repository, media uploads, and database logs", "• ")
add_bullet("Network: Standard Internet or Localhost loopback (127.0.0.1:5000)", "• ")

add_body("Software Environment:")
add_bullet("Operating System: Microsoft Windows 10/11, Ubuntu Linux, or macOS", "• ")
add_bullet("Backend Runtime: Python 3.10 / 3.14 Environment", "• ")
add_bullet("Web Framework: Python Flask (Version 3.0+)", "• ")
add_bullet("Database Management System: MySQL Community Server 8.0+", "• ")
add_bullet("Database Driver: flask_mysqldb / MySQLdb connector", "• ")
add_bullet("Security & Encryption: bcrypt library for password hashing", "• ")
add_bullet("Frontend Stack: HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Bootstrap Icons", "• ")

add_title("1.6 Technology Used (Full-Stack Architecture)", 2)
add_bullet("Python Flask: Selected as the micro-framework for its lightweight architecture, modular blueprint routing, powerful Jinja2 templating, and zero-overhead request dispatching.", "• ")
add_bullet("MySQL Relational Database: Chosen for strict ACID transactional guarantees, foreign key relational integrity across 8 structured tables, and scalable indexing.", "• ")
add_bullet("Bootstrap 5 & Custom CSS3: Implements custom CSS variables (--brown, --pink, --cream) with responsive grid layouts ensuring seamless viewing on mobile phones, tablets, and desktop workstations.", "• ")
add_bullet("Bcrypt Salted Hashing: Industry-standard adaptive cryptographic hashing algorithm that automatically generates cryptographic salts to protect user and admin credentials.", "• ")

doc.add_page_break()

# ==============================================================================
# CHAPTER 2 - PROPOSED SYSTEM
# ==============================================================================
add_title("CHAPTER 2 - PROPOSED SYSTEM", 1)

add_title("2.1 Comprehensive Feasibility Study", 2)
add_body("Before initiating development, a thorough feasibility investigation was performed across four dimensions:")
add_bullet("Technical Feasibility: The tech stack combines Python Flask with native MySQLdb and Bootstrap 5. Python provides clean syntax that is easy for college students to defend during academic viva, while MySQL provides standard SQL relational queries without complex ORM abstractions.", "1. ")
add_bullet("Operational Feasibility: The platform adopts intuitive e-commerce workflows familiar to modern consumers. Customers can easily select sizes, add to cart, and place Cash on Delivery orders without needing credit cards or complicated payment gateways.", "2. ")
add_bullet("Economic & Financial Feasibility: The software is built completely on open-source technologies (Python, Flask, MySQL, Bootstrap). Total software licensing expenditure is Rs. 0. It eliminates expensive third-party aggregator commissions (up to 25-30% charged by Swiggy/Zomato).", "3. ")
add_bullet("Schedule & Legal Feasibility: Completed systematically within a 4-week development cycle. It adheres to consumer protection norms by clearly displaying transparent product pricing, ingredients, and delivery terms.", "4. ")

add_title("2.2 Strategic Objectives of the Proposed System", 2)
add_bullet("Digitize Bakery Operations: Replace manual counter book-keeping with real-time MySQL database logging.", "• ")
add_bullet("Zero Order Misplacement: Enforce structured checkout forms capturing full customer name, phone, address, and delivery date.", "• ")
add_bullet("Transparent Real-Time Pricing: Automatically adjust base prices when customers select 0.5kg, 1kg, 1.5kg, or 2kg portions.", "• ")
add_bullet("Real-Time Order Tracking: Keep customers informed regarding the exact operational status of their cakes (Pending, Confirmed, Baking, Out for Delivery, Delivered).", "• ")
add_bullet("Empower Bakery Administration: Provide non-technical managers with an intuitive admin dashboard to add/edit/delete cakes and upload images without touching code.", "• ")

add_title("2.3 E-Commerce Platform vs Traditional Walk-in Bakery", 2)
comp_table = doc.add_table(rows=1, cols=3)
comp_headers = ["Parameter", "Traditional Walk-in Counter", "Sweet Cravings Web Portal"]
comp_widths = [1.8, 2.3, 2.3]
comp_data = [
    ["Ordering Channel", "Physical store visit or phone call", "24/7 Digital online web portal"],
    ["Catalog Display", "Limited to physical counter display glass", "Unlimited digital catalog with filtering"],
    ["Pricing Customization", "Manual verbal calculation by cashier", "Automated real-time JS price multiplier"],
    ["Order Record", "Physical paper diary / register", "Permanent ACID MySQL database tables"],
    ["Preparation Tracking", "Customer must call store repeatedly", "Live status badges (Baking / Delivered)"],
    ["Sales Analytics", "Manual end-of-month tallying", "Real-time auto-computed revenue metrics"]
]
style_table(comp_table, comp_widths, comp_headers, comp_data)

doc.add_page_break()

# ==============================================================================
# CHAPTER 3 - ANALYSIS & DESIGN
# ==============================================================================
add_title("CHAPTER 3 - ANALYSIS & DESIGN", 1)

add_title("3.1 Software Requirements Specification (SRS)", 2)
add_body("Functional Requirements (FR):")
add_bullet("FR-01 (Catalog Discovery & Search): The system shall render all cakes categorized under Birthday, Chocolate, Wedding, Black Forest, and Custom Cakes, with live keyword search.", "• ")
add_bullet("FR-02 (Cake Customization): The user shall select cake size (0.5kg, 1kg, 1.5kg, 2kg) and available flavours with dynamic price adjustment.", "• ")
add_bullet("FR-03 (Shopping Cart Management): Customers shall add cakes to cart, adjust quantities (+/-), and remove items with instant subtotal calculation.", "• ")
add_bullet("FR-04 (COD Checkout & Order Placement): The application shall validate customer delivery details and create a permanent order under Cash on Delivery (COD).", "• ")
add_bullet("FR-05 (Customer Order History): Authenticated users shall view past orders with order date, itemized bill, total cost, and real-time status badges.", "• ")
add_bullet("FR-06 (Admin Cake CRUD): Bakery managers shall create, edit, update prices, and delete cakes with image uploads.", "• ")
add_bullet("FR-07 (Admin Order Lifecycle Management): Managers shall update order statuses (Pending -> Confirmed -> Baking -> Out for Delivery -> Delivered).", "• ")
add_bullet("FR-08 (Dashboard Analytics): The system shall compute Total Cakes, Registered Customers, Total Orders, and Net Revenue.", "• ")

add_body("Non-Functional Requirements (NFR):")
add_bullet("NFR-01 (Security & Hashing): Passwords must be hashed using bcrypt before database insertion.", "• ")
add_bullet("NFR-02 (Data Integrity): All foreign key relations must enforce referential integrity with ON DELETE CASCADE where appropriate.", "• ")
add_bullet("NFR-03 (Performance): Response time for catalog queries and cart updates must remain under 200ms.", "• ")
add_bullet("NFR-04 (Responsive Usability): The UI must render seamlessly across smartphone, tablet, and desktop viewports.", "• ")

add_title("3.2 System Architecture (3-Tier Model)", 2)
add_body("The application follows a proven 3-Tier Client-Server Architecture, separating presentation, business logic, and relational storage:")
add_image_safe(os.path.join(assets_dir, "fig3_1_architecture.png"), 5.6, "Figure 3.1: 3-Tier System Architecture of Sweet Cravings Cake Shop")

add_title("3.3 Table Structure & Data Dictionary (8 MySQL Tables)", 2)
add_body("The relational schema cake_shop_db comprises 8 interconnected tables with robust primary and foreign key constraints:")

# Table 1: users
add_title("Table 3.1: users Table Structure", 3)
tbl_u = doc.add_table(rows=1, cols=5)
style_table(tbl_u, [1.1, 1.1, 1.1, 1.5, 1.6], ["Field", "Type", "Null", "Key", "Description"], [
    ["id", "INT", "NO", "PRI (Auto)", "Primary key identifier"],
    ["full_name", "VARCHAR(100)", "NO", "", "Customer's full legal name"],
    ["email", "VARCHAR(100)", "NO", "UNI", "Unique login email address"],
    ["phone", "VARCHAR(15)", "YES", "", "Customer contact phone number"],
    ["password", "VARCHAR(255)", "NO", "", "bcrypt hashed password string"],
    ["created_at", "DATETIME", "YES", "", "Account registration timestamp"]
])

# Table 2: cakes
add_title("Table 3.2: cakes Table Structure", 3)
tbl_c = doc.add_table(rows=1, cols=5)
style_table(tbl_c, [1.2, 1.1, 1.0, 1.4, 1.7], ["Field", "Type", "Null", "Key", "Description"], [
    ["id", "INT", "NO", "PRI (Auto)", "Cake product identifier"],
    ["category_id", "INT", "NO", "FK", "References categories(id)"],
    ["name", "VARCHAR(150)", "NO", "", "Display name of the cake"],
    ["description", "TEXT", "YES", "", "Cake ingredients and description"],
    ["price", "DECIMAL(10,2)", "NO", "", "Base price for 1kg portion"],
    ["image_url", "VARCHAR(255)", "YES", "", "Filename in static/images/cakes"],
    ["available_sizes", "VARCHAR(200)", "YES", "", "CSV of sizes (e.g. 0.5kg,1kg,2kg)"],
    ["available_flavours", "VARCHAR(300)", "YES", "", "CSV of flavour choices"],
    ["is_featured", "TINYINT(1)", "YES", "", "Flag for homepage spotlight"],
    ["stock", "INT", "YES", "", "Available daily inventory count"],
    ["created_at", "DATETIME", "YES", "", "Catalog creation timestamp"]
])

# Table 3: orders & order_items
add_title("Table 3.3: orders Table Structure", 3)
tbl_o = doc.add_table(rows=1, cols=5)
style_table(tbl_o, [1.1, 1.1, 1.1, 1.4, 1.7], ["Field", "Type", "Null", "Key", "Description"], [
    ["id", "INT", "NO", "PRI (Auto)", "Order tracking number"],
    ["user_id", "INT", "NO", "FK", "References users(id)"],
    ["full_name", "VARCHAR(100)", "NO", "", "Recipient contact name"],
    ["phone", "VARCHAR(15)", "NO", "", "Recipient phone number"],
    ["address", "TEXT", "NO", "", "Complete doorstep delivery address"],
    ["delivery_date", "DATE", "NO", "", "Requested delivery date"],
    ["payment_method", "VARCHAR(50)", "YES", "", "Payment type (Cash on Delivery)"],
    ["total_amount", "DECIMAL(10,2)", "NO", "", "Final bill amount charged"],
    ["status", "VARCHAR(30)", "YES", "", "Order status (Pending/Baking/etc)"],
    ["created_at", "DATETIME", "YES", "", "Order placement timestamp"]
])

add_title("3.4 Entity-Relationship Diagram (ERD)", 2)
add_body("The ER Diagram models the relational dependencies across users, cakes, shopping carts, and order snapshots:")
add_image_safe(os.path.join(assets_dir, "fig3_7_erd.png"), 5.6, "Figure 3.2: Entity-Relationship Diagram (ERD) of cake_shop_db")

add_title("3.5 Use Case Modeling", 2)
add_body("Figure 3.3 illustrates the functional interactions between the Customer and Bakery Admin actors:")
add_image_safe(os.path.join(assets_dir, "fig3_2_usecase.png"), 5.6, "Figure 3.3: Use Case Diagram for Customer and Admin Interactions")

add_title("3.6 Component & Class Architecture", 2)
add_body("The object-oriented structure and component decomposition are detailed in Figure 3.4 and Figure 3.5:")
add_image_safe(os.path.join(assets_dir, "fig3_3_component.png"), 5.6, "Figure 3.4: Modular Component Architecture and Data Flow")
add_image_safe(os.path.join(assets_dir, "fig3_6_class.png"), 5.6, "Figure 3.5: Class Diagram representing Domain Model")

add_title("3.7 Activity Diagram (Customer Order Journey)", 2)
add_body("The procedural lifecycle from store arrival to order completion is depicted below:")
add_image_safe(os.path.join(assets_dir, "fig3_4_activity.png"), 4.6, "Figure 3.6: Activity Diagram of Customer Browsing & Ordering")

add_title("3.8 Sequence Diagram (Order Processing)", 2)
add_body("Figure 3.7 details the sequential execution of API requests, session management, and MySQL database writes:")
add_image_safe(os.path.join(assets_dir, "fig3_5_sequence.png"), 5.6, "Figure 3.7: Sequence Diagram of Cake Selection, Cart, and Checkout Flow")

doc.add_page_break()

# ==============================================================================
# CHAPTER 4 - INPUT SCREENS WITH DATA
# ==============================================================================
add_title("CHAPTER 4 - INPUT SCREENS WITH DATA", 1)
add_body("This chapter showcases the actual input forms engineered into the website, demonstrating data validation and user experience.")

add_title("4.1 Customer Registration & Login Portal", 2)
add_body("Figure 4.1 shows the dual authentication screen where customers register with validation on email uniqueness, phone formatting, and password security.")
add_image_safe(os.path.join(assets_dir, "fig4_1_login_reg.png"), 5.6, "Figure 4.1: Customer Registration & Secure Login Portal")

add_title("4.2 Cake Customization & Detail Interface", 2)
add_body("Figure 4.2 presents the single cake view where customers select portion size (0.5kg to 2kg) and gourmet flavour infusion, triggering client-side dynamic pricing.")
add_image_safe(os.path.join(assets_dir, "fig4_2_cake_detail.png"), 5.6, "Figure 4.2: Cake Customization & Add-to-Cart Interface")

add_title("4.3 Interactive Shopping Cart Management", 2)
add_body("Figure 4.3 illustrates the cart interface where users modify quantities with live asynchronous price updates and clear item listings.")
add_image_safe(os.path.join(assets_dir, "fig4_3_cart.png"), 5.6, "Figure 4.3: Interactive Shopping Cart Interface")

add_title("4.4 Cash on Delivery Checkout & Delivery Form", 2)
add_body("Figure 4.4 displays the final checkout screen capturing customer delivery address, contact telephone, and scheduled delivery date.")
add_image_safe(os.path.join(assets_dir, "fig4_4_checkout.png"), 5.6, "Figure 4.4: Delivery Details & Cash on Delivery Checkout Screen")

doc.add_page_break()

# ==============================================================================
# CHAPTER 5 - OUTPUT SCREENS WITH DATA
# ==============================================================================
add_title("CHAPTER 5 - OUTPUT SCREENS WITH DATA", 1)
add_body("This chapter documents the rendered output interfaces of the Sweet Cravings website.")

add_title("5.1 Homepage Hero Banner & Category Collections", 2)
add_body("Figure 5.1 displays the landing view, highlighting the Sweet Cravings value proposition, promotional banners, and category navigation pills.")
add_image_safe(os.path.join(assets_dir, "fig5_1_home.png"), 5.6, "Figure 5.1: Homepage Hero Section & Category Collections")

add_title("5.2 Cake Catalog with Dynamic Search & Filtering", 2)
add_body("Figure 5.2 captures the comprehensive cake catalog featuring live search by keywords (e.g. 'chocolate') and instant category isolation.")
add_image_safe(os.path.join(assets_dir, "fig5_2_catalog.png"), 5.6, "Figure 5.2: Filterable Cake Catalog & Product Showcase")

add_title("5.3 Customer Order History & Status Tracking", 2)
add_body("Figure 5.3 displays the customer's personal order history, showing past cake purchases, itemized costs, and preparation status badges (Baking / Delivered).")
add_image_safe(os.path.join(assets_dir, "fig5_3_orders.png"), 5.6, "Figure 5.3: Customer Order History & Live Tracking")

add_title("5.4 Bakery Admin Dashboard & Analytics Portal", 2)
add_body("Figure 5.4 exhibits the administrative dashboard featuring 4 business KPI cards (Total Cakes, Customers, Orders, Revenue) and order status update controls.")
add_image_safe(os.path.join(assets_dir, "fig5_4_admin_dashboard.png"), 5.6, "Figure 5.4: Administrative Control Center & Analytics Dashboard")

add_title("5.5 Mobile Responsive Smartphone View", 2)
add_body("Figure 5.5 demonstrates the mobile smartphone experience, illustrating responsive navigation drawers and mobile-friendly touch targets.")
add_image_safe(os.path.join(assets_dir, "fig5_5_mobile.png"), 3.8, "Figure 5.5: Mobile Responsive Layout on Smartphone")

doc.add_page_break()

# ==============================================================================
# CHAPTER 6 - CODE SNIPPETS
# ==============================================================================
add_title("CHAPTER 6 - CODE SNIPPETS", 1)
add_body("This chapter presents core code excerpts demonstrating the architectural principles implemented in Sweet Cravings.")

add_title("6.1 Database Connection & Configuration (config.py)", 2)
add_body("""class Config:
    SECRET_KEY = 'sweet_cravings_secret_2024'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_DB = 'cake_shop_db'
    UPLOAD_FOLDER = 'static/images/cakes'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}""", italic=True)

add_title("6.2 Password Hashing & Authentication Decorators (app.py)", 2)
add_body("""def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Password Hashing during Registration
hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
cur.execute('INSERT INTO users (full_name, email, password, phone) VALUES (%s,%s,%s,%s)',
            (full_name, email, hashed_pw, phone))""", italic=True)

add_title("6.3 Cart to Order Transaction Pipeline (app.py)", 2)
add_body("""# Atomic Order Creation & Cart Cleanup
cur.execute('''
    INSERT INTO orders (user_id, full_name, phone, address, delivery_date, total_amount, status)
    VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
''', (session['user_id'], name, phone, address, delivery_date, total_amount))
order_id = cur.lastrowid

# Snapshot each item from cart_items into order_items
for item in cart_items:
    cur.execute('''
        INSERT INTO order_items (order_id, cake_id, cake_name, price, quantity, size, flavour)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (order_id, item['cake_id'], item['name'], item['price'], item['qty'], item['size'], item['flavour']))

# Clear cart for user
cur.execute('DELETE FROM cart_items WHERE cart_id = %s', (cart_id,))
mysql.connection.commit()""", italic=True)

doc.add_page_break()

# ==============================================================================
# CHAPTER 7 - TESTING & TEST CASES
# ==============================================================================
add_title("CHAPTER 7 - TESTING (TEST CASES)", 1)
add_body("Systematic software quality assurance was conducted across all customer and administrative workflows. Table 7.1 summarizes 12 functional test cases.")

test_table = doc.add_table(rows=1, cols=6)
test_headers = ["Test ID", "Scenario", "Input Data", "Expected Result", "Actual Result", "Status"]
test_widths = [0.8, 1.4, 1.3, 1.3, 1.3, 0.5]
test_data = [
    ["TC-01", "Customer Reg.", "Valid Name, Email, Pass", "Account created in users table", "User saved with bcrypt hash", "PASS"],
    ["TC-02", "Duplicate Email", "Existing registered email", "Display error: Email already registered", "Error flashed, rejected", "PASS"],
    ["TC-03", "Customer Login", "Valid email & password", "Session initiated, redirect to /", "Logged in, navbar updated", "PASS"],
    ["TC-04", "Invalid Login", "Wrong password", "Access denied: Invalid credentials", "Rejected, error message shown", "PASS"],
    ["TC-05", "Dynamic Sizing", "Select 2kg on detail page", "Price doubled from base 1kg price", "Price recomputed dynamically", "PASS"],
    ["TC-06", "Add to Cart", "Cake ID: 1, 1kg, Qty: 1", "Item inserted into cart_items", "Cart badge incremented to 1", "PASS"],
    ["TC-07", "Cart Quantity", "Click '+' on cart item", "Quantity incremented, total recalculated", "Total updated accurately", "PASS"],
    ["TC-08", "COD Checkout", "Valid Name, Phone, Address", "Order created, cart emptied", "Order saved, redirected to /orders", "PASS"],
    ["TC-09", "Order Tracking", "View /orders", "Display past orders with status", "Orders rendered with badges", "PASS"],
    ["TC-10", "Admin Login", "User: admin, Pass: admin123", "Admin session created, /admin/dashboard", "Admin dashboard loaded", "PASS"],
    ["TC-11", "Cake CRUD", "Admin adds new cake with img", "Cake added to cakes table & folder", "New cake visible in catalog", "PASS"],
    ["TC-12", "Order Status", "Admin changes status to 'Baking'", "Status updated in orders table", "Customer view reflects 'Baking'", "PASS"]
]
style_table(test_table, test_widths, test_headers, test_data)

doc.add_page_break()

# ==============================================================================
# CHAPTER 8, 9, 10, 11
# ==============================================================================
add_title("CHAPTER 8 - LIMITATIONS OF PROPOSED SYSTEM", 1)
add_body("While the system successfully automates core bakery operations, certain architectural limitations exist:")
add_bullet("Offline Cash on Delivery Only: The current implementation focuses exclusively on Cash on Delivery (COD) to suit beginner-friendly student demonstration. Online payment gateways (Razorpay, Stripe) are not yet integrated.", "8.1 ")
add_bullet("Single-Location Inventory: Stock levels are tracked globally per cake rather than segmented across multiple bakery branch outlets.", "8.2 ")
add_bullet("Simulated SMS/Email Alerts: Order notifications are rendered within the web portal rather than transmitted via external SMS/WhatsApp gateways.", "8.3 ")

add_title("CHAPTER 9 - PROPOSED ENHANCEMENTS", 1)
add_bullet("Online Payment Integration: Integrate Razorpay or UPI QR payment gateways for automated prepaid orders.", "9.1 ")
add_bullet("WhatsApp & SMS Order Bot: Integrate Twilio or WhatsApp Cloud API to send real-time preparation updates to customers' phones.", "9.2 ")
add_bullet("3D Cake Customizer: Integrate Three.js to allow users to visualize customized fondant layers, cake toppings, and photo prints in real-time 3D.", "9.3 ")
add_bullet("Multi-Branch Multi-Vendor Expansion: Support regional cloud delivery hubs with distance-based delivery fee calculations.", "9.4 ")

add_title("CHAPTER 10 - CONCLUSION", 1)
add_body("The “Sweet Cravings – Full-Stack Online Cake Shop & Bakery Management Web Application” successfully modernizes traditional confectionery retail by delivering an end-to-end e-commerce solution.")
add_body("By leveraging Python Flask, MySQL, and Bootstrap 5, the platform eliminates paper-based ordering errors, prevents customer miscommunication, provides dynamic portion pricing, and empowers bakery managers with real-time sales and inventory insights.")
add_body("The project provided profound practical learnings in full-lifecycle software engineering, secure password cryptography, relational database normalisation, responsive web styling, and viva presentation readiness.")

add_title("CHAPTER 11 - BIBLIOGRAPHY & REFERENCES", 1)
add_bullet("Grinberg, Miguel. Flask Web Development: Developing Web Applications with Python. O'Reilly Media.", "1. ")
add_bullet("Silberschatz, Abraham, Henry F. Korth, and S. Sudarshan. Database System Concepts. McGraw-Hill Education.", "2. ")
add_bullet("Flask Documentation (Pallets Projects): https://flask.palletsprojects.com/", "3. ")
add_bullet("MySQL 8.0 Reference Manual: https://dev.mysql.com/doc/refman/8.0/en/", "4. ")
add_bullet("Bootstrap 5.3 Documentation: https://getbootstrap.com/docs/5.3/", "5. ")
add_bullet("MDN Web Docs - JavaScript & DOM APIs: https://developer.mozilla.org/", "6. ")

output_path = r"C:\Users\Admin\.gemini\antigravity\scratch\sweet_cravings\report\Sweet_Cravings_Project_Report.docx"
doc.save(output_path)
print(f"Project report successfully created at: {output_path}")
