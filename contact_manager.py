import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title(" Contact Management System")
        self.root.geometry("1728x1344")  
        self.root.config(bg="#EAEAEA")
        self.root.resizable(True, True)  

        self.contacts_file = "contacts.json"
        self.contacts = []

        self.load_contacts()
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#EAEAEA")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Contact Management System", font=("Arial", 24), bg="#EAEAEA")
        self.title_label.pack(pady=10)

        # Input Frame
        self.input_frame = tk.Frame(self.main_frame, bg="#FFFFFF", bd=2, relief=tk.RAISED)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Input Fields
        self.name_label = tk.Label(self.input_frame, text="Name", bg="#FFFFFF")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.input_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.phone_label = tk.Label(self.input_frame, text="Phone", bg="#FFFFFF")
        self.phone_label.grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.input_frame, width=50)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        self.email_label = tk.Label(self.input_frame, text="Email", bg="#FFFFFF")
        self.email_label.grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.input_frame, width=50)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button Frame
        self.button_frame = tk.Frame(self.main_frame, bg="#EAEAEA")
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Buttons
        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact, bg="#4169E1", fg="white")
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Contact", command=self.edit_contact, bg="#4169E1", fg="white")
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact, bg="#4169E1", fg="white")
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        # Search Bar Frame
        self.search_frame = tk.Frame(self.main_frame, bg="#EAEAEA")
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Search Bar
        self.search_label = tk.Label(self.search_frame, text="Search:", bg="#EAEAEA")
        self.search_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_contact, bg="#4169E1", fg="white")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Sort Dropdown Frame
        self.sort_frame = tk.Frame(self.main_frame, bg="#EAEAEA")
        self.sort_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Sort Dropdown
        self.sort_label = tk.Label(self.sort_frame, text="Sort by:", bg="#EAEAEA")
        self.sort_label.grid(row=0, column=0, padx=5, pady=5)
        self.sort_var = tk.StringVar(value="Name")
        self.sort_combobox = ttk.Combobox(self.sort_frame, textvariable=self.sort_var, values=["Name", "Phone", "Email"], state='readonly')
        self.sort_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.sort_button = tk.Button(self.sort_frame, text="Sort", command=self.sort_contacts, bg="#4169E1", fg="white")
        self.sort_button.grid(row=0, column=2, padx=5, pady=5)

        # Contact List Frame
        self.contact_list_frame = tk.Frame(self.main_frame)
        self.contact_list_frame.pack(fill=tk.BOTH, expand=True)

        self.contact_listbox = tk.Listbox(self.contact_list_frame, font=("Arial", 12), bg="#FFFFFF")
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.contact_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contact_listbox.yview)

        self.load_listbox()

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r') as f:
                self.contacts = json.load(f)

    def save_contacts(self):
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f)

    def load_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if self.validate_contact(name, phone, email):
            self.contacts.append({"name": name, "phone": phone, "email": email})
            self.save_contacts()
            self.load_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Invalid contact details")

    def edit_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if self.validate_contact(name, phone, email):
                contact = self.contacts[selected_index[0]]
                contact["name"] = name
                contact["phone"] = phone
                contact["email"] = email
                self.save_contacts()
                self.load_listbox()
                self.clear_entries()
            else:
                messagebox.showwarning("Warning", "Invalid contact details")
        else:
            messagebox.showwarning("Warning", "Select a contact to edit")

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            del self.contacts[selected_index[0]]
            self.save_contacts()
            self.load_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Select a contact to delete")

    def search_contact(self):
        search_term = self.search_entry.get().strip().lower()
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or
                search_term in contact['phone'].lower() or
                search_term in contact['email'].lower()):
                self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

    def sort_contacts(self):
        sort_by = self.sort_var.get()
        if sort_by == "Name":
            self.contacts.sort(key=lambda x: x['name'])
        elif sort_by == "Phone":
            self.contacts.sort(key=lambda x: x['phone'])
        elif sort_by == "Email":
            self.contacts.sort(key=lambda x: x['email'])
        self.save_contacts()
        self.load_listbox()

    def validate_contact(self, name, phone, email):
        # Simple validation checks
        if not name or not phone or not email:
            return False
        if not re.match(r'^\+?[0-9\s]+$', phone): 
            return False
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  
            return False
        return True

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
