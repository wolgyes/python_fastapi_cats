import tkinter as tk
from tkinter import filedialog
import requests


class CatApp:
    def __init__(self, master):

        self.master = master
        master.title("Cat App")

        # Create input fields for cat data
        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        self.breed_label = tk.Label(master, text="Breed:")
        self.breed_label.grid(row=1, column=0)
        self.breed_entry = tk.Entry(master)
        self.breed_entry.grid(row=1, column=1)

        self.age_label = tk.Label(master, text="Age:")
        self.age_label.grid(row=2, column=0)
        self.age_entry = tk.Entry(master)
        self.age_entry.grid(row=2, column=1)

        # Create button to submit cat data
        self.submit_button = tk.Button(master, text="Create Cat", command=self.create_cat)
        self.submit_button.grid(row=3, column=1)

        # Create button to select image file
        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_button.grid(row=4, column=0)

        # Create button to upload image
        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image, state="disabled")
        self.upload_button.grid(row=4, column=1)

        # Create label for image file path
        self.file_path_label = tk.Label(master, text="")
        self.file_path_label.grid(row=5, column=0, columnspan=2)

        # Initialize image file path and cat ID
        self.file_path = None
        self.cat_id = None

        self.get_cats()

    def get_cats(self):
        cats = requests.get("http://localhost:8000/cats").json()

        for idx, cat in enumerate(cats):

            e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
            e.grid(row=idx + 8, column=0)
            e.insert(1, cat['id'])

            e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
            e.grid(row=idx + 8, column=1)
            e.insert(1, cat['name'])

            e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
            e.grid(row=idx + 8, column=2)
            e.insert(1, cat['age'])

            e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
            e.grid(row=idx + 8, column=3)
            e.insert(1, cat['breed'])

            if cat['image'] == None:
                e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
                e.grid(row=idx + 8, column=4)
                e.insert(1, "No Image")

            else:
                e = tk.Entry(self.master, width=20, fg='white', font=('Arial', 14))
                e.grid(row=idx + 8, column=4)
                e.insert(1, cat['image'])

            e = tk.Button(
                self.master, width=10,
                fg='blue', font=('Arial', 14),
                text="Delete",
                command=lambda idx=cat["id"]: self.delete_cat(idx))
            e.grid(row=idx + 8, column=5)

    def create_cat(self):
        # Get cat data from input fields
        cat_data = {
            "name": self.name_entry.get(),
            "breed": self.breed_entry.get(),
            "age": int(self.age_entry.get())
        }

        # Make POST request to create new cat
        response = requests.post("http://localhost:8000/cats", json=cat_data)
        if response.status_code == 200:
            # Store cat ID and enable image upload button if cat was created successfully
            self.cat_id = response.json()["id"]
            self.upload_button.config(state="normal")

    def select_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

    def refresh(self):
        root.destroy()
        self.__init__(self.master)

    def upload_image(self):
        # Check if an image file has been selected and a cat ID has been assigned
        if self.file_path and self.cat_id:
            # Open image file and read contents
            with open(self.file_path, "rb") as f:
                file_contents = f.read()

            # Make POST request to upload image for the specified cat
            response = requests.post(f"http://localhost:8000/cats/{self.cat_id}/image", files={"image": file_contents})
            if response.status_code == 200:
                # Clear image file path and disable upload button
                self.file_path = None
                self.file_path_label.config(text="")
                self.upload_button.config(state="disabled")

    def delete_cat(self, idx):
        requests.delete(f"http://localhost:8000/cats/{idx}")



root = tk.Tk()
app = CatApp(root)
root.mainloop()
