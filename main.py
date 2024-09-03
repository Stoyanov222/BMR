import customtkinter as ctk
import numpy as np
import pandas as pd
from tkinter import simpledialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set global appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("BMR Calculator")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.selected_weight = 0
        self.selected_gender = None
        self.selected_protein = None
        self.selected_calories = None
        self.result_text = None

        self.create_widgets()


    def create_widgets(self):

        # Gender Selection
        self.gender = ["Please select", "Male", "Female"]
        self.gender_label = ctk.CTkLabel(self, text="Please select gender:")
        self.gender_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        self.gender_menu = ctk.CTkOptionMenu(self, values=self.gender, command=self.update_gender)
        self.gender_menu.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Weight Input with slider selection
        self.weight_entry = ctk.CTkLabel(self, text="Select Weight:")
        self.weight_entry.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        self.weight_slider = ctk.CTkSlider(self, from_=20, to=200, command=self.update_weight)
        self.weight_slider.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew") 

        # Height Input - todo: Update it with slider selection
        self.height_entry = ctk.CTkEntry(self, placeholder_text="Height (in cm)")
        self.height_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Age Input - todo: Update it with slider selection
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Age")
        self.age_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Protein Input - todo: Update it with slider selection
        start = 0.3
        stop = 1.5
        step = 0.1

        self.protein_per_g = ["Please select"] + [f"{i:.1f}" for i in np.arange(start, stop + step, step)]
        self.protein_label = ctk.CTkLabel(self, text="Protein g/lb Bodyweight:")
        self.protein_label.grid(row=6, column=0, padx=20, pady=0, sticky="w")
        self.protein_menu = ctk.CTkOptionMenu(self, values=self.protein_per_g, command=self.update_protein)
        self.protein_menu.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        # Weight Gain/Loss Input in Calories - todo: Update it with slider selection
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

        # Export Data Button
        self.export_button = ctk.CTkButton(self, text="Export Data", command=self.export_result)
        self.export_button.grid(row=9, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Reset Button
        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=10, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Result Display
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=11, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    def update_weight(self, value):
        self.selected_weight = value if value else None
        self.weight_entry.configure(text=f"Selected weight: {round(self.selected_weight)} kg")

    def update_gender(self, value):
        self.selected_gender = value if value != "Please select" else None

    def update_protein(self, value):
        self.selected_protein = float(value) if value != "Please select" else None

    def update_calories(self, value):
        self.selected_calories = float(value) if value != "Please select" else None

    def update_result(self, value):
        self.result_text = value if value else None

    def export_result(self):
        if self.result_text:
            # Prompt the user to enter a file name
            file_name = simpledialog.askstring("Input", "Enter the file name (without extension):", parent=self)
            
            if file_name:
                file_name = file_name.strip() + ".xlsx"  # Ensure the file has .xlsx extension

                # Parse the result text into a list of dictionaries
                data = []
                for line in self.result_text.splitlines():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data.append({"Description": key.strip(), "Value": value.strip()})

                # Create a DataFrame from the parsed data
                df = pd.DataFrame(data)

                # Export the DataFrame to an Excel file with the user-provided name
                df.to_excel(file_name, index=False)
                self.result_label.configure(text=f"Data has been exported to {file_name}!")
            else:
                self.result_label.configure(text="File name cannot be empty!")
        else:
            self.result_label.configure(text="There is no data to be exported!")

    def calculate_bmr(self):
        try:
            weight = self.selected_weight
            weight_lb = weight * 2.2
            height = float(self.height_entry.get())
            age = int(self.age_entry.get())
            calories_adjust = self.selected_calories
            protein = self.selected_protein

            if not self.validate_inputs(weight, height, age):
                return
            
            if self.selected_gender == "Male":
                bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
            elif self.selected_gender == "Female":
                bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
            
            sedentery_cals = bmr * 1.2 + calories_adjust
            light_cals = bmr * 1.35 + calories_adjust
            moderate_cals = bmr * 1.5 + calories_adjust
            high_cals = bmr * 1.68 + calories_adjust
            protein_per_day = weight_lb * protein
            protein_per_day_cals = protein_per_day * 4

            self.result_text = (
            f"Your BMR is: {round(bmr)} calories/day\n\n"
            f"Caloric needs based on activity level:\n"
            f"Sedentary (little or no exercise): {round(sedentery_cals)} calories/day\n"
            f"Lightly active (light exercise/sports 1-3 days/week): {round(light_cals)} calories/day\n"
            f"Moderately active (moderate exercise/sports 3-5 days/week): {round(moderate_cals)} calories/day\n"
            f"Very active (hard exercise/sports 6-7 days a week): {round(high_cals)} calories/day\n"
            f"Protein per day: {round(protein_per_day)}g / {round(protein_per_day_cals)} calories\n"
            f"Your calories deficit/surplus is: {int(calories_adjust)} calories"
        )
            self.result_label.configure(text=self.result_text)
            self.update_result(self.result_text)
        except ValueError:
            self.result_label.configure(text="Please enter valid data.")
    
    def validate_inputs(self, weight, height, age):
        if weight is None or weight < 0:
            self.result_label.configure(text="Weight can't be negative or invalid!")
            return False

        if height is None or height < 0:
            self.result_label.configure(text="Height can't be negative or invalid!")
            return False

        if age is None or age <= 0:
            self.result_label.configure(text="Age must be a positive integer!")
            return False

        if self.selected_gender is None:
            self.result_label.configure(text="Please select a gender.")
            return False

        if self.selected_protein is None:
            self.result_label.configure(text="Please select a protein value.")
            return False

        if self.selected_calories is None:
            self.result_label.configure(text="Please select calories.")
            return False

        return True

    def reset_fields(self):
        
        # Reset all input fields and selections
        self.gender_menu.set("Please select")
        self.height_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.protein_menu.set("Please select")
        self.calories_menu.set("Please select")
        self.result_label.configure(text="")
        
        # Reset stored values
        self.weight_slider.set(110)
        self.selected_weight = 0
        self.weight_entry.configure(text=f"Select Weight:")

        self.selected_gender = None
        self.selected_protein = None
        self.selected_calories = None
        self.result_text = None

if __name__ == "__main__":
    app = App()
    app.mainloop()

        