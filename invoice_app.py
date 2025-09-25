import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

def money(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        root.title("Invoice Generator")
        root.geometry("920x600")

        # Invoice metadata frame
        meta = ttk.Frame(root, padding=8)
        meta.pack(fill="x")
        ttk.Label(meta, text="Invoice No:").grid(row=0, column=0, sticky="w")
        self.invoice_no = ttk.Entry(meta)
        self.invoice_no.grid(row=0, column=1, padx=4)
        self.invoice_no.insert(0, f"INV{date.today().strftime('%Y%m%d')}-001")

        ttk.Label(meta, text="Invoice Date:").grid(row=0, column=2, sticky="w")
        self.date_entry = ttk.Entry(meta)
        self.date_entry.grid(row=0, column=3, padx=4)
        self.date_entry.insert(0, date.today().isoformat())

        ttk.Label(meta, text="Client:").grid(row=1, column=0, sticky="w")
        self.client_entry = ttk.Entry(meta, width=50)
        self.client_entry.grid(row=1, column=1, columnspan=3, sticky="w")

        # Items frame
        items_frame = ttk.Frame(root, padding=8)
        items_frame.pack(fill="both", expand=True)

        cols = ("#","Description","Qty","Unit Price","Tax %","Discount","Line Total")
        self.tree = ttk.Treeview(items_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            if c == "Description":
                self.tree.column(c, width=300)
            else:
                self.tree.column(c, width=90, anchor="e")
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="left", fill="y")

        # Controls to add item
        control = ttk.Frame(root, padding=8)
        control.pack(fill="x")
        ttk.Label(control, text="Description").grid(row=0, column=0)
        self.desc = ttk.Entry(control, width=40)
        self.desc.grid(row=0, column=1)

        ttk.Label(control, text="Qty").grid(row=0, column=2)
        self.qty = ttk.Entry(control, width=8)
        self.qty.grid(row=0, column=3)
        self.qty.insert(0,"1")

        ttk.Label(control, text="Unit Price").grid(row=0, column=4)
        self.up = ttk.Entry(control, width=10)
        self.up.grid(row=0, column=5)
        self.up.insert(0,"0.00")

        ttk.Label(control, text="Tax %").grid(row=0, column=6)
        self.tax = ttk.Entry(control, width=6)
        self.tax.grid(row=0, column=7)
        self.tax.insert(0,"0")

        ttk.Label(control, text="Discount").grid(row=0, column=8)
        self.disc = ttk.Entry(control, width=8)
        self.disc.grid(row=0, column=9)
        self.disc.insert(0,"0.00")

        ttk.Button(control, text="Add Item", command=self.add_item).grid(row=0, column=10, padx=6)
        ttk.Button(control, text="Delete Item", command=self.delete_item).grid(row=0, column=11, padx=6)

        # Summary frame
        summary = ttk.Frame(root, padding=8)
        summary.pack(fill="x", side="bottom")

        ttk.Label(summary, text="Subtotal:").grid(row=0, column=0, sticky="e")
        self.subtotal_var = tk.StringVar(value="0.00")
        ttk.Label(summary, textvariable=self.subtotal_var, width=12).grid(row=0, column=1, sticky="w")

        ttk.Label(summary, text="Total Tax:").grid(row=1, column=0, sticky="e")
        self.totaltax_var = tk.StringVar(value="0.00")
        ttk.Label(summary, textvariable=self.totaltax_var, width=12).grid(row=1, column=1, sticky="w")

        ttk.Label(summary, text="Discount:").grid(row=2, column=0, sticky="e")
        self.totaldisc_var = tk.StringVar(value="0.00")
        ttk.Label(summary, textvariable=self.totaldisc_var, width=12).grid(row=2, column=1, sticky="w")

        ttk.Label(summary, text="Grand Total:").grid(row=3, column=0, sticky="e")
        self.grand_var = tk.StringVar(value="0.00")
        ttk.Label(summary, textvariable=self.grand_var, width=12).grid(row=3, column=1, sticky="w")

        ttk.Button(summary, text="Export PDF", command=self.export_pdf).grid(row=3, column=2, padx=10)
        ttk.Button(summary, text="Clear All", command=self.clear_all).grid(row=3, column=3)

    def add_item(self):
        desc = self.desc.get().strip()
        try:
            qty = money(self.qty.get())
            up = money(self.up.get())
            tax = Decimal(self.tax.get() or "0")
            disc = money(self.disc.get())
        except Exception as e:
            messagebox.showerror("Error","Invalid numeric value.")
            return
        if not desc:
            messagebox.showerror("Error","Description cannot be empty.")
            return

        line_before_tax = qty * up
        line_after_disc = line_before_tax - disc
        tax_amount = (line_after_disc * tax / Decimal("100")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        line_total = (line_after_disc + tax_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        idx = len(self.tree.get_children()) + 1
        self.tree.insert("", "end", values=(idx, desc, str(qty), f"{up:.2f}", f"{tax:.2f}", f"{disc:.2f}", f"{line_total:.2f}"))
        self.clear_entry_fields()
        self.recalculate()

    def delete_item(self):
        sel = self.tree.selection()
        if not sel:
            return
        self.tree.delete(sel[0])
        # re-index
        for i, item in enumerate(self.tree.get_children(), start=1):
            vals = list(self.tree.item(item,"values"))
            vals[0] = i
            self.tree.item(item, values=vals)
        self.recalculate()

    def clear_entry_fields(self):
        self.desc.delete(0,'end'); self.qty.delete(0,'end'); self.up.delete(0,'end')
        self.tax.delete(0,'end'); self.disc.delete(0,'end')
        self.qty.insert(0,"1"); self.up.insert(0,"0.00"); self.tax.insert(0,"0"); self.disc.insert(0,"0.00")

    def recalculate(self):
        subtotal = Decimal('0.00')
        total_tax = Decimal('0.00')
        total_discount = Decimal('0.00')
        for it in self.tree.get_children():
            vals = self.tree.item(it,"values")
            # vals: idx, desc, qty, up, tax, disc, line_total
            qty = Decimal(vals[2])
            up = Decimal(vals[3])
            tax = Decimal(vals[4])
            disc = Decimal(vals[5])
            line_before_tax = qty * up
            line_after_disc = line_before_tax - Decimal(disc)
            tax_amount = (line_after_disc * tax / Decimal("100")).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            line_total = (line_after_disc + tax_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            subtotal += line_after_disc
            total_tax += tax_amount
            total_discount += Decimal(disc)
        grand = (subtotal + total_tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.subtotal_var.set(f"{subtotal:.2f}")
        self.totaltax_var.set(f"{total_tax:.2f}")
        self.totaldisc_var.set(f"{total_discount:.2f}")
        self.grand_var.set(f"{grand:.2f}")

    def clear_all(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        self.recalculate()

    def export_pdf(self):
        if not self.tree.get_children():
            messagebox.showwarning("No items","Add at least one item.")
            return

        fname = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")], initialfile=self.invoice_no.get()+".pdf")
        if not fname:
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "INVOICE", ln=True, align="C")
        pdf.ln(4)

        pdf.set_font("Helvetica", size=10)
        # Company (placeholder) left
        pdf.cell(100, 5, "Your Company Name", ln=0)
        pdf.cell(0, 5, f"Invoice No: {self.invoice_no.get()}", ln=1)
        pdf.cell(100, 5, "Address line 1", ln=0)
        pdf.cell(0, 5, f"Date: {self.date_entry.get()}", ln=1)
        pdf.ln(6)
        pdf.cell(0, 5, f"Billed To: {self.client_entry.get()}", ln=1)
        pdf.ln(6)

        # Table header
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(8,8,"#",1)
        pdf.cell(90,8,"Description",1)
        pdf.cell(18,8,"Qty",1,align="R")
        pdf.cell(24,8,"Unit",1,align="R")
        pdf.cell(16,8,"Tax%",1,align="R")
        pdf.cell(24,8,"Total",1,ln=1,align="R")

        pdf.set_font("Helvetica", size=10)
        for it in self.tree.get_children():
            idx, desc, qty, up, tax, disc, line_total = self.tree.item(it,"values")
            pdf.cell(8,8,str(idx),1)
            # description:
            pdf.cell(90,8, str(desc)[:50],1)  # truncate if long
            pdf.cell(18,8,str(qty),1,align="R")
            pdf.cell(24,8,str(up),1,align="R")
            pdf.cell(16,8,str(tax),1,align="R")
            pdf.cell(24,8,str(line_total),1,ln=1,align="R")

        pdf.ln(4)
        # Summary
        pdf.set_font("Helvetica", size=10)
        pdf.cell(140,6,"Subtotal",0,0,'R')
        pdf.cell(40,6,self.subtotal_var.get(),0,1,'R')
        pdf.cell(140,6,"Total Tax",0,0,'R')
        pdf.cell(40,6,self.totaltax_var.get(),0,1,'R')
        pdf.cell(140,6,"Discount",0,0,'R')
        pdf.cell(40,6,self.totaldisc_var.get(),0,1,'R')
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(140,8,"Grand Total",0,0,'R')
        pdf.cell(40,8,self.grand_var.get(),0,1,'R')

        pdf.ln(6)
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0,5,"Notes: Thank you for your business. Payment due within 15 days.")
        try:
            pdf.output(fname)
            messagebox.showinfo("Saved", f"Invoice saved to {fname}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
