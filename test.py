from tkinter import *
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button, messagebox
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from num2words import num2words
import os
from datetime import datetime

root = Tk()
root.title("SHRI VAARI TANK & DOORS")

# Set background color
root.configure(bg="#8caba8")

# Create Entry widgets for various fields including total_in_text_igst_entry
grand_total_entry = Entry(root)
gst_entry = Entry(root)
total_in_text_entry = Entry(root)
cgst_entry = Entry(root)
sgst_entry = Entry(root)
igst_entry = Entry(root)
total_in_text_igst_entry = Entry(root)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 90% of screen dimensions
window_width = int(screen_width * 0.9)
window_height = int(screen_height * 0.9)
root.geometry(f"{window_width}x{window_height}")

# Calculate the x and y positions for centering vertically and offsetting from the top
x = int((screen_width - window_width) / 2)  # Centered horizontally
y = int(screen_height * 0.05)  # 5% down from the top

# Set the window position
root.geometry(f"+{x}+{y}")

today = date.today()
# Date
date_label = Label(root, text="Date: " + today.strftime("%d/%m/%Y"), font=("Calibri", int(screen_height * 0.015)))
date_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Customer Details Entry Fields
customer_frame = Frame(root)
customer_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

customer_labels = ["Name:", "Contact:", "Address:","GSTN:"]
entry_fields = {}

for index, label in enumerate(customer_labels):
    lbl = Label(customer_frame, text=label, font=("Calibri", int(screen_height * 0.015)))
    lbl.grid(row=index, column=0, padx=int(screen_width * 0.01), pady=int(screen_height * 0.01), sticky="w")

    entry_fields[label] = Entry(customer_frame, font=("Calibri", int(screen_height * 0.015)), width=75)
    entry_fields[label].grid(row=index, column=1, padx=int(screen_width * 0.01), pady=int(screen_height * 0.01))

# Initialize a list to store product details
products = []

def add_product_field():
    # Get data from entries
    product_name = product_name_entry.get()
    product_HSNCODE = product_HSNCODE_entry.get()
    product_quantity = product_quantity_entry.get()
    product_price = product_price_entry.get()

    try:
        # Calculate total value
        total_value = float(product_quantity)*float(product_price)
    except ValueError:
        messagebox.showerror("Error", "Invalid input for price or quantity")
        return

    # Add product details to the products list
    products.append([product_name,product_HSNCODE, product_price, product_quantity, total_value])

    # Clear entry fields
    product_name_entry.delete(0, END)
    product_HSNCODE_entry.delete(0, END)
    product_quantity_entry.delete(0, END)
    product_price_entry.delete(0, END)

    # Update Treeview with new data
    update_product_tree()

def update_product_tree():
    # Clear existing Treeview data
    for row in product_tree.get_children():
        product_tree.delete(row)

    # Populate Treeview with data from products list
    for product in products:
        product_tree.insert("", "end", values=product)


# Frame for Product Details
product_frame = Frame(root, padx=10, pady=10)
product_frame.grid(row=5, column=0, columnspan=2)

# Labels and Entries for adding products within the frame
product_name_label = Label(product_frame, text="PRODUCT :")
product_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
product_name_entry = Entry(product_frame, width=30)
product_name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

product_price_label = Label(product_frame, text="QUANTITY :")
product_price_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
product_price_entry = Entry(product_frame, width=30)
product_price_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

product_quantity_label = Label(product_frame, text="RATE :")
product_quantity_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
product_quantity_entry = Entry(product_frame, width=30)
product_quantity_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

product_HSNCODE_label = Label(product_frame, text="HSNCODE :")
product_HSNCODE_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
product_HSNCODE_entry = Entry(product_frame, width=30)
product_HSNCODE_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)


# Create Treeview for displaying products
product_tree = ttk.Treeview(root, columns=("PRODUCT","HSNCODE","QNT","RATE","AMOUNT"), show="headings")

product_tree.heading("PRODUCT", text="PRODUCT")
product_tree.heading("HSNCODE", text="HSNCODE")
product_tree.heading("QNT", text="QNT")
product_tree.heading("RATE", text="RATE")
product_tree.heading("AMOUNT", text="AMOUNT")
product_tree.grid(row=20, column=0, columnspan=2, padx=20, pady=20)

# Add button for adding products
add_product_button = Button(root, text="Add Product", command=add_product_field, bg="green", fg="white")
add_product_button.grid(row=10, column=0, columnspan=2, pady=10)

# Read the last bill number from a file
def get_last_bill_number():
    try:
        with open("last_bill_number.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0  # If the file doesn't exist yet, start from 0 or any initial number

# Save the latest bill number to a file
def save_bill_number(number):
    with open("last_bill_number.txt", "w") as file:
        file.write(str(number))

# Generate a new bill number
def generate_bill_number():
    current_bill_number = get_last_bill_number() + 1
    save_bill_number(current_bill_number)  # Save the updated bill number
    return current_bill_number

# Function to generate PDF report
def generate_pdf():
    # Gather invoice details from the UI fields
    customer_name = entry_fields["Name:"].get()
    customer_contact = entry_fields["Contact:"].get()
    customer_address = entry_fields["Address:"].get()
    GSTN = entry_fields["GSTN:"].get()

    # Calculate grand total and CGST, SGST, IGST
    grand_total = sum(item[4] for item in products)
    grand_total_entry.delete(0, END)
    grand_total_entry.insert(0, grand_total)

    # Calculate CGST, SGST, IGST
    cgst = grand_total * 0.09

    sgst = grand_total * 0.09

    igst = " "

    # Update Entry widgets with CGST, SGST, IGST
    cgst_entry.delete(0, END)
    cgst_entry.insert(0, cgst)

    sgst_entry.delete(0, END)
    sgst_entry.insert(0, sgst)

    igst_entry.delete(0, END)
    igst_entry.insert(0, igst)

    # Calculate grand total with IGST
    grand_total_with_igst = grand_total + cgst + sgst



    # Convert total amount with IGST to text format
    total_in_text_igst = f"{num2words(grand_total_with_igst, lang='en_IN')}"

    # Update Entry widget with total amount in text format with IGST
    total_in_text_igst_entry.delete(0, END)
    total_in_text_igst_entry.insert(0, total_in_text_igst)

    # Create a directory named 'Bill PDF' in the current directory if it doesn't exist
    directory = "Bill PDF"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the current date to create year, month, and day folders
    current_date = datetime.now()
    year_folder = os.path.join(directory, str(current_date.year))
    month_folder = os.path.join(year_folder, str(current_date.month))
    day_folder = os.path.join(month_folder, str(current_date.day))

    # Create year, month, and day folders if they don't exist
    for folder in [year_folder, month_folder, day_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Create a PDF file in the 'day_folder' directory
    pdf_filename = f"{customer_name}_invoice.pdf"
    pdf_path = os.path.join(day_folder, pdf_filename)

    # Create a canvas for the PDF
    c = canvas.Canvas(pdf_path)

    # Draw the images and adjust their size
    c.drawImage("0101.jpg", x=50, y=715, width=100, height=75)  # TOP left corner
    c.drawImage("0102.jpg", x=265, y=760, width=100, height=70)  # TOP right corner
    c.drawImage("Untitled-1-01.jpg", x=450, y=695, width=100, height=100)  # Header

    # Heading (centered)
    c.setFont("Helvetica-Bold", 18)  # Heading font and size
    c.drawCentredString(300, 760, "SHRI VAARI TANK & DOORS")  # Heading

    # Address (centered)
    c.setFont("Helvetica", 10)  # Address font and size
    c.drawCentredString(300, 740,

                       "85, Devangapuram Extension, Shevapet, Salem-636 002")  # Address
    # E-mail(align center)
    c.drawCentredString(300, 720,"E - mail: shrivaari2013 @ gmail.com")
    # Phone numbers (align center)
    c.setFont("Helvetica", 10)  # Phone number font and size
    c.drawCentredString(300, 700, "Phone: 9442530991, 7373525234")  # Phone numbers

    # Tax Invoice (centered)
    c.setFont("Helvetica-Bold", 14)  # Tax Invoice font and size
    c.drawCentredString(300, 660, "TAX INVOICE")  # Tax Invoice

    # GSTN (left right corner)
    c.setFont("Helvetica", 12)
    c.drawCentredString(125, 800, "GSTN:33AIYPJ3686K1ZH")

    # Date (top right corner)
    c.setFont("Helvetica", 12)  # Date font and size
    c.drawString(450, 660, "Date: " + today.strftime("%d/%m/%Y"))  # Date

    # Use the generate_bill_number function whenever you need a new bill number
    new_bill_number = generate_bill_number()
    c.setFont("Helvetica", 12)
    c.drawCentredString(95, 660,f"INVOICE NO: {new_bill_number}")

    # Customer details
    c.drawString(50, 630, f"CUSTOMER NAME: {customer_name}")
    c.drawString(50, 610, f"CONTACT: {customer_contact}")
    c.drawString(50, 590, f"ADDRESS: {customer_address}")
    c.drawString(50, 570, f"GSTN: {GSTN}")
    
    # Add more content as needed based on your invoice structure

    # Table Header (Product details)
    table_header = ["S.NO", "PRODUCT", "HSNCODE", "QNT", "RATE", "AMOUNT"]
    table_x = 50
    table_y = 530
    col_width_sno = 40  # Reduced width for S.NO column by 50%
    col_width_product = 160
    col_width_qnt = 40

    col_width = [col_width_sno, col_width_product, 80, col_width_qnt, 80, 80]  # Adjust the column widths as necessary
    cell_height = 20  # Height of each cell

    c.setFont("Helvetica-Bold", 10)  # Table header font and size

    # Drawing table headers and borders
    for i, header in enumerate(table_header):
        c.rect(table_x, table_y, col_width[i], cell_height)
        c.drawString(table_x + 5, table_y + 5, header)
        table_x += col_width[i]

    # Table Content (Product details)
    c.setFont("Helvetica", 10)  # Table content font and size
    table_y -= cell_height  # Move to the next row for products

    # Generating sample products with S.NO based on entry
    for idx, product_row in enumerate(products, start=1):
        table_x = 50
        # Add borders and content for each cell
        for i, data in enumerate([str(idx), product_row[0], product_row[1], product_row[2], product_row[3], product_row[4]]):
            c.rect(table_x, table_y, col_width[i], cell_height)
            c.drawString(table_x + 5, table_y + 5, str(data))
            table_x += col_width[i]
        table_y -= cell_height  # Move to the next row

    # Calculate the positions for the text
    text_x = 373  # X-coordinate for the text
    text_y = table_y - 5
    col_width = 78

    # Define labels and corresponding values
    labels = ["TOTAL", "CGST", "SGST", "IGST", "G.TOTAL"]
    values = [str(grand_total), str(cgst), str(sgst), str(igst), str(grand_total_with_igst)]

    # Format the values with two decimal places
    formatted_values = []
    for val in values:
        if val == str(igst):  # Skip formatting for 'IGST'
            formatted_values.append(val)
        else:
            formatted_values.append("{:.2f}".format(float(val)))  # Format to two decimal places

    # Set the font for specific values to be bold
    c.setFont("Helvetica-Bold", 10)  # Change the font to bold

    # Draw borders around labels and values
    for i, label in enumerate(labels):
        c.rect(text_x, text_y - 20 * i, col_width, 20)  # Border around the text
        c.drawString(text_x + 5, text_y - 20 * i + 5, f"{label}")  # Draw text within the border

        # Draw values in the adjacent column
        if i < len(formatted_values):  # Check if index within formatted_values list
            if i == 4:  # Check if it's the G.TOTAL
                c.setFont("Helvetica-Bold", 10)  # Change the font to bold for G.TOTAL
            c.rect(text_x + col_width, text_y - 20 * i, col_width, 20)  # Border around the value
            c.drawString(text_x + col_width + 5, text_y - 20 * i + 5,
                         f"{formatted_values[i]}")  # Draw value within the border

    # Total in text
    c.setFont("Helvetica", 8)
    c.drawString(50, 150, f"G.Total: {total_in_text_igst} Rupees.")  # Grand Total with IGST

    #Above signature
    c.setFont("Helvetica", 10)
    c.drawString(360, 100, "for SHRI VAARI TANKS & DOORS")

    # Shop Owner's Signature
    c.drawString(400, 50, "Proprietor Signature")  # Signature placeholder
    c.drawString(50, 80, "All Our Transaction and Invoice are ")
    c.drawString(50, 70, "subject to Salem Jurisdiction")
    c.drawString(50, 40, "E & O.E.")

    # Display a message indicating the PDF generation
    messagebox.showinfo("PDF Generated", f"PDF generated successfully: {pdf_filename}")

    c.save()
# Button to generate PDF
pdf_button = Button(root, text="Generate PDF", command=generate_pdf, bg="Orange", fg="white")
pdf_button.grid(row=25, column=0,columnspan=4, pady=10)


root.mainloop()
