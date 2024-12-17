import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE_NAME = "bike_records.csv"

# Bike Management System Class
class BikeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bike Management System")
        self.root.geometry("800x500")

        self.bike_id = tk.StringVar()
        self.bike_name = tk.StringVar()
        self.bike_model = tk.StringVar()
        self.bike_price = tk.StringVar()

        # GUI Components
        self.setup_gui()
        self.load_data()

    def setup_gui(self):
        # Title Label
        title = tk.Label(self.root, text="Bike Management System", font=("Arial", 20, "bold"), bg="blue", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)

        # Input Frame
        input_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="lightgray")
        input_frame.place(x=20, y=50, width=400, height=400)

        tk.Label(input_frame, text="Bike ID", font=("Arial", 12, "bold"), bg="lightgray").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        tk.Entry(input_frame, textvariable=self.bike_id, font=("Arial", 12)).grid(row=0, column=1, pady=10, padx=10, sticky="w")

        tk.Label(input_frame, text="Bike Name", font=("Arial", 12, "bold"), bg="lightgray").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        tk.Entry(input_frame, textvariable=self.bike_name, font=("Arial", 12)).grid(row=1, column=1, pady=10, padx=10, sticky="w")

        tk.Label(input_frame, text="Bike Model", font=("Arial", 12, "bold"), bg="lightgray").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        tk.Entry(input_frame, textvariable=self.bike_model, font=("Arial", 12)).grid(row=2, column=1, pady=10, padx=10, sticky="w")

        tk.Label(input_frame, text="Bike Price", font=("Arial", 12, "bold"), bg="lightgray").grid(row=3, column=0, pady=10, padx=10, sticky="w")
        tk.Entry(input_frame, textvariable=self.bike_price, font=("Arial", 12)).grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Button Frame
        button_frame = tk.Frame(input_frame, bg="lightgray")
        button_frame.grid(row=4, columnspan=2, pady=10)

        tk.Button(button_frame, text="Add Bike", command=self.add_bike, width=10, bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Bike", command=self.update_bike, width=10, bg="blue", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Bike", command=self.delete_bike, width=10, bg="red", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_inputs, width=10, bg="gray", fg="white").grid(row=0, column=3, padx=5)

        # Data Table Frame
        table_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        table_frame.place(x=440, y=50, width=340, height=400)

        self.bike_table = ttk.Treeview(table_frame, columns=("id", "name", "model", "price"), show="headings")
        self.bike_table.heading("id", text="ID")
        self.bike_table.heading("name", text="Name")
        self.bike_table.heading("model", text="Model")
        self.bike_table.heading("price", text="Price")

        self.bike_table['columns'] = ('id', 'name', 'model', 'price')
        self.bike_table.column("id", width=50)
        self.bike_table.column("name", width=100)
        self.bike_table.column("model", width=100)
        self.bike_table.column("price", width=80)

        self.bike_table.pack(fill=tk.BOTH, expand=1)
        self.bike_table.bind("<ButtonRelease-1>", self.get_selected_row)

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.bike_table.insert('', tk.END, values=row)

    def add_bike(self):
        if self.validate_inputs():
            bike = (self.bike_id.get(), self.bike_name.get(), self.bike_model.get(), self.bike_price.get())
            self.bike_table.insert('', tk.END, values=bike)
            self.save_data()
            messagebox.showinfo("Success", "Bike added successfully!")
            self.clear_inputs()

    def update_bike(self):
        selected_item = self.bike_table.selection()
        if selected_item:
            self.bike_table.item(selected_item, values=(
                self.bike_id.get(), self.bike_name.get(), self.bike_model.get(), self.bike_price.get()
            ))
            self.save_data()
            messagebox.showinfo("Success", "Bike updated successfully!")
            self.clear_inputs()
        else:
            messagebox.showwarning("Warning", "No bike selected to update!")

    def delete_bike(self):
        selected_item = self.bike_table.selection()
        if selected_item:
            self.bike_table.delete(selected_item)
            self.save_data()
            messagebox.showinfo("Success", "Bike deleted successfully!")
            self.clear_inputs()
        else:
            messagebox.showwarning("Warning", "No bike selected to delete!")

    def save_data(self):
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in self.bike_table.get_children():
                writer.writerow(self.bike_table.item(row)['values'])

    def get_selected_row(self, event):
        selected_item = self.bike_table.selection()[0]
        bike = self.bike_table.item(selected_item, 'values')
        self.bike_id.set(bike[0])
        self.bike_name.set(bike[1])
        self.bike_model.set(bike[2])
        self.bike_price.set(bike[3])

    def clear_inputs(self):
        self.bike_id.set("")
        self.bike_name.set("")
        self.bike_model.set("")
        self.bike_price.set("")

    def validate_inputs(self):
        if not all([self.bike_id.get(), self.bike_name.get(), self.bike_model.get(), self.bike_price.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return False
        return True


def main():
    root = tk.Tk()
    app = BikeManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()