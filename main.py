import customtkinter as ctk
import numpy as np

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BMR Calculator")
        self.geometry("800x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.selected_gender = None
        self.selected_protein = None
        self.selected_calories = None

        # Gender Selection
        self.gender = ["Please select", "Male", "Female"]
        self.gender_label = ctk.CTkLabel(self, text="Please select gender:")
        self.gender_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        self.gender_menu = ctk.CTkOptionMenu(self, values=self.gender, command=self.update_gender)
        self.gender_menu.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Weight Input
        self.weight_entry = ctk.CTkEntry(self, placeholder_text="Weight (in kg)")
        self.weight_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Height Input
        self.height_entry = ctk.CTkEntry(self, placeholder_text="Height (in cm)")
        self.height_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Age Input
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Age")
        self.age_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Protein Input
        start = 0.3
        stop = 1.5
        step = 0.1

        self.protein_per_g = ["Please select"] + [f"{i:.1f}" for i in np.arange(start, stop + step, step)]
        self.protein_label = ctk.CTkLabel(self, text="Protein g/lb Bodyweight:")
        self.protein_label.grid(row=6, column=0, padx=20, pady=0, sticky="w")
        self.protein_menu = ctk.CTkOptionMenu(self, values=self.protein_per_g, command=self.update_protein)
        self.protein_menu.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        # Weight Gain/Loss Input in Calories
        start = -1000
        stop = 1400
        step = 100

        self.calories_change = ["Please select"] + [f"{i:.1f}" for i in np.arange(start, stop + step, step)]
        self.calories_label = ctk.CTkLabel(self, text="Select Additional daily calories for gain or reduce for weight loss:")
        self.calories_label.grid(row=7, column=0, padx=20, pady=0, sticky="w")
        self.calories_menu = ctk.CTkOptionMenu(self, values=self.calories_change, command=self.update_calories)
        self.calories_menu.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

        # Calculate Button
        self.calculate_button = ctk.CTkButton(self, text="Calculate BMR", command=self.calculate_bmr)
        self.calculate_button.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Result Display
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=9, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    def update_gender(self, value):
        self.selected_gender = value if value != "Please select" else None

    def update_protein(self, value):
        self.selected_protein = float(value) if value != "Please select" else None

    def update_calories(self, value):
        self.selected_calories = float(value) if value != "Please select" else None

    def calculate_bmr(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            age = int(self.age_entry.get())
            
            if self.selected_gender is None:
                self.result_label.configure(text="Please select a gender.")
                return

            if self.selected_protein is None:
                self.result_label.configure(text="Please select a protein value.")
                return

            if self.selected_gender == "Male":
                bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
            elif self.selected_gender == "Female":
                bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)

            self.result_label.configure(text=f"Your BMR is: {bmr:.2f} calories/day")
        except ValueError:
            self.result_label.configure(text="Please enter valid data.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
