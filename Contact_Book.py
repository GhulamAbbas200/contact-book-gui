import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


# Node class for linked list
class Node:
    def __init__(self, first_name, last_name, title, email, mobile, number_type):
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.email = email
        self.mobile = mobile
        self.number_type = number_type
        self.next = None


# LinkedList class for managing contacts
class LinkedList:
    def __init__(self):
        self.top = None  # Stack top or linked list head

    def push(self, first_name, last_name, title, email, mobile, number_type):
        new_node = Node(first_name, last_name, title, email, mobile, number_type)
        new_node.next = self.top
        self.top = new_node

    def find(self, name):
        current = self.top
        matches = []
        while current:
            if f"{current.first_name} {current.last_name}".lower() == name.lower():
                matches.append(current)
            current = current.next
        return matches

    def update(self, node, updated_contact):
        if node:
            node.first_name = updated_contact['first_name']
            node.last_name = updated_contact['last_name']
            node.title = updated_contact['title']
            node.email = updated_contact['email']
            node.mobile = updated_contact['mobile']
            node.number_type = updated_contact['number_type']

    def delete(self, node):
        if not self.top:
            return False
        if self.top == node:
            self.top = self.top.next
            return True

        current = self.top
        while current.next and current.next != node:
            current = current.next

        if current.next == node:
            current.next = node.next
            return True
        return False

    def view_stack(self):
        stack = []
        current = self.top
        while current:
            stack.append({
            'first_name': current.first_name,
            'last_name': current.last_name,
            'title': current.title,
            'email': current.email,
            'mobile': current.mobile,
            'number_type': current.number_type
            })
            current = current.next  # This line ensures the loop moves forward
        return stack[::-1]  # Reverse the stack to show the most recent first



    def to_array(self):
        contacts = []
        current = self.top
        while current:
            contacts.append({
                'first_name': current.first_name,
                'last_name': current.last_name,
                'title': current.title,
                'email': current.email,
                'mobile': current.mobile,
                'number_type': current.number_type
            })
            current = current.next
        return contacts


# File handling
file_path = "contacts2.json"

def load_contacts(linked_list):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            contacts = json.load(file)
            for contact in contacts:
                # Handle old format where 'name' exists instead of 'first_name' and 'last_name'
                if 'name' in contact:
                    name_parts = contact['name'].split(maxsplit=1)
                    contact['first_name'] = name_parts[0]
                    contact['last_name'] = name_parts[1] if len(name_parts) > 1 else ''
                    contact['title'] = contact.get('title', 'Unknown')
                    contact['number_type'] = contact.get('number_type', 'Phone')
                
                # Push to linked list using the new format
                linked_list.push(
                    contact['first_name'], 
                    contact['last_name'], 
                    contact['title'], 
                    contact.get('email', ''), 
                    contact['mobile'], 
                    contact['number_type']
                )


def save_contacts(linked_list):
    with open(file_path, 'w') as file:
        json.dump(linked_list.to_array(), file)


# GUI Application
linked_list = LinkedList()
load_contacts(linked_list)

def create_contact():
    def save_new_contact():
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        title = title_entry.get().strip()
        email = email_entry.get().strip()
        mobile = mobile_entry.get().strip()
        number_type = number_type_var.get()

        if not first_name or not last_name or not mobile or not title:
            messagebox.showerror("Error", "First Name, Last Name, Title, and Mobile Number are required!")
            return

        if number_type == "Landline" and len(mobile) != 10:
            messagebox.showerror("Error", "Landline number must be exactly 10 digits!")
            return

        if number_type == "Phone" and len(mobile) != 11:
            messagebox.showerror("Error", "Phone number must be exactly 11 digits!")
            return

        linked_list.push(first_name, last_name, title, email if email else None, mobile, number_type)
        save_contacts(linked_list)
        messagebox.showinfo("Success", f"Contact {first_name} {last_name} added successfully!")
        new_contact_window.destroy()

    new_contact_window = tk.Toplevel(root)
    new_contact_window.title("Create New Contact")

    tk.Label(new_contact_window, text="First Name:").pack()
    first_name_entry = tk.Entry(new_contact_window)
    first_name_entry.pack()

    tk.Label(new_contact_window, text="Last Name:").pack()
    last_name_entry = tk.Entry(new_contact_window)
    last_name_entry.pack()

    tk.Label(new_contact_window, text="Title:").pack()
    title_entry = tk.Entry(new_contact_window)
    title_entry.pack()

    tk.Label(new_contact_window, text="Email (Optional):").pack()
    email_entry = tk.Entry(new_contact_window)
    email_entry.pack()

    tk.Label(new_contact_window, text="Mobile Number:").pack()
    mobile_entry = tk.Entry(new_contact_window)
    mobile_entry.pack()

    tk.Label(new_contact_window, text="Number Type:").pack()
    number_type_var = tk.StringVar(value="Phone")
    tk.Radiobutton(new_contact_window, text="Phone", variable=number_type_var, value="Phone").pack()
    tk.Radiobutton(new_contact_window, text="Landline", variable=number_type_var, value="Landline").pack()

    tk.Button(new_contact_window, text="Save", command=save_new_contact).pack()
    
def update_contact():
    def select_and_update():
        try:
            index = int(option.get()) - 1
            selected_node = matches[index]

            new_first_name = simpledialog.askstring("Update Contact", "Enter new First name:", initialvalue=selected_node.first_name)
            new_last_name = simpledialog.askstring("Update Contact", "Enter new Last name:", initialvalue=selected_node.last_name)
            new_title = simpledialog.askstring("Update Contact", "Enter new Title:", initialvalue=selected_node.title)
            new_email = simpledialog.askstring("Update Contact", "Enter new Email:", initialvalue=selected_node.email)
            new_mobile = simpledialog.askstring("Update Contact", "Enter new Mobile:", initialvalue=selected_node.mobile)

            if not new_first_name or not new_last_name or not new_title or not new_mobile:
                messagebox.showerror("Error", "All fields except email are required!")
                return

            # Update the contact
            updated_contact = {
                'first_name': new_first_name,
                'last_name': new_last_name,
                'title': new_title,
                'email': new_email if new_email else None,
                'mobile': new_mobile,
                'number_type': selected_node.number_type  # Preserve existing number type
            }

            linked_list.update(selected_node, updated_contact)
            save_contacts(linked_list)
            messagebox.showinfo("Success", "Contact updated successfully!")
            update_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please select a valid option!")
    
    # Get the name to search
    first_name = simpledialog.askstring("Update Contact", "Enter the full name of the contact to update:")
    if not first_name:
        return

    matches = linked_list.find(first_name)
    if not matches:
        messagebox.showerror("Error", f"No contact found with the name '{first_name}'")
        return

    # Create a window to show all matches
    update_window = tk.Toplevel(root)
    update_window.title("Update Contact")
    option = tk.StringVar(value="1")

    # List all matches as radio buttons
    for i, contact in enumerate(matches):
        tk.Radiobutton(
            update_window,
            text=f"{i + 1}. {contact.first_name} {contact.last_name} | Title: {contact.title} | Email: {contact.email if contact.email else 'N/A'} | Mobile: {contact.mobile}",
            variable=option,
            value=str(i + 1)
        ).pack(anchor="w")

    tk.Button(update_window, text="Update Selected Contact", command=select_and_update).pack()




def delete_contact():
    name = simpledialog.askstring("Delete Contact", "Enter the name of the contact to delete:")
    if not name:
        return

    matches = linked_list.find(name)
    if not matches:
        messagebox.showerror("Error", f"No contacts found with the name '{name}'!")
        return

    # Allow user to choose which contact to delete
    delete_window = tk.Toplevel(root)
    delete_window.title("Select Contact to Delete")

    option = tk.StringVar(value="1")
    for i, contact in enumerate(matches):
        tk.Radiobutton(
            delete_window,
            text=f"{i + 1}. {contact.first_name} {contact.last_name} | Email: {contact.email} | Mobile: {contact.mobile}",
            variable=option,
            value=str(i + 1)
        ).pack()

    def confirm_delete():
        index = int(option.get()) - 1
        selected_node = matches[index]
        linked_list.delete(selected_node)
        save_contacts(linked_list)
        messagebox.showinfo("Success", f"Deleted contact: {selected_node.first_name} {selected_node.last_name}")
        delete_window.destroy()

    tk.Button(delete_window, text="Delete Selected Contact", font=("Times New Roman", 12), command=confirm_delete).pack()
    

def search_contact():
    full_name = simpledialog.askstring("Search Contact", "Enter full name (First Last):")
    if not full_name:
        return

    # Split the input into first and last name
    name_parts = full_name.strip().split(maxsplit=1)
    if len(name_parts) < 2:
        messagebox.showerror("Invalid Input", "Please enter both first and last names!")
        return

    first_name, last_name = name_parts[0], name_parts[1]

    matches = linked_list.find(f"{first_name} {last_name}")
    if not matches:
        messagebox.showerror("Not Found", f"No contacts found with the name '{first_name} {last_name}'")
        return

    # Show matching results
    result = "\n".join([f"{contact.first_name} {contact.last_name} | {contact.email if contact.email else 'N/A'} | {contact.mobile} | {contact.title}" for contact in matches])
    messagebox.showinfo("Search Results", result)


def count_contacts():
    count = len(linked_list.to_array())
    messagebox.showinfo("Total Contacts", f"Total number of contacts: {count}")
    
def view_contacts():
    contacts = linked_list.view_stack()
    if not contacts:
        messagebox.showinfo("No Contacts", "No contacts to display.")
        return

    contact_list = "\n".join([f"{i + 1}. {contact['first_name']} {contact['last_name']} | Title: {contact['title']} | Email: {contact['email'] if contact['email'] else 'N/A'} | Mobile: {contact['mobile']} ({contact['number_type']})" for i, contact in enumerate(contacts)])
    messagebox.showinfo("Contacts", contact_list)
    contacts = linked_list.view_stack()
    if not contacts:
        messagebox.showinfo("No Contacts", "No contacts to display.")
        return
    

    
# Main GUI
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x400")

tk.Label(root, text="Contact Book Application", font=("Times New Roman", 16)).pack(pady=10)

tk.Button(root, text="Create Contact", font=("Times New Roman", 12), command=create_contact).pack(pady=10)
tk.Button(root, text="Update Contact", font=("Times New Roman", 12), command=update_contact).pack(pady=10)
tk.Button(root, text="View Contacts",  font=("Times New Roman", 12), command=view_contacts).pack(pady=10)
tk.Button(root, text="Search Contact", font=("Times New Roman", 12), command=search_contact).pack(pady=10)
tk.Button(root, text="Delete Contact", font=("Times New Roman", 12), command=delete_contact).pack(pady=10)
tk.Button(root, text="Count Contacts", font=("Times New Roman", 12), command=count_contacts).pack(pady=10)

root.mainloop()
