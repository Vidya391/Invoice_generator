# 🧾 Invoice Generator System

A desktop application built with **Python, Tkinter, SQLite, and FPDF** to generate and manage invoices.  
It creates professional invoices for products/services with auto-calculated taxes, discounts, and totals. The system provides a clean user interface for entering client and product details and allows users to generate/exports invoices as **PDF files**.

---

## 🎯 Goal

*** Design a user-friendly interface where users can:

*Enter product/service details

*Automatically calculate subtotal, tax, discount, and grand total

*Export invoice in PDF format

---

## 🚀 Features

- 🖥️ **GUI with Tkinter**

- ➕ Add, delete, and manage invoice items

- 📊 Automatic calculation of:

  - Subtotal

  - Taxes

  - Discounts

  - Grand Total

- 📂 **Database (SQLite)** integration

  - Clients

  - Products

  - Invoices

  - Invoice Items

- 📑 Export invoice as a **professional PDF**

- 🔍 Easy retrieval of saved invoices

- ⏱️ Auto-incrementing invoice numbers

- ✅ Cross-platform (Windows, Linux, macOS)

---

## 📂 Project Structure

Invoice-Generator/

│── invoice_app.py              # Main Tkinter application (invoice generator)

│── requirements.txt     # Python dependencies

│── database/

│   └── invoice.db       # MySQL database schema (optional)

│── output/

│   └── INV20250925-001.pdf  # Example exported PDF

---

## ⚙️ Installation & Setup

### 1. Clone Repository

git clone https://github.com/Vidya391/invoice-generator.git

cd invoice-generator

### 2. Create Virtual Environment (optional but recommended)

python -m venv venv

source venv/bin/activate   # macOS/Linux

venv\Scripts\activate      # Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run the Application

python invoice_app.py

---

## 📄 Example Invoice PDF

[INV20250925-001.pdf](https://github.com/user-attachments/files/22539919/INV20250925-001.pdf)

---

## 🔮 Future Enhancements

  * Add authentication (login system)

  * Search & filter invoices

  * Generate invoice reports (monthly/yearly)

  * Cloud database support (MySQL/PostgreSQL)

  * Option to email invoices directly from the app
