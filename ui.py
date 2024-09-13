import customtkinter as ctk
import numpy as np
import pandas as pd
from tkinter import simpledialog
from db import get_db_connection, save_data, load_latest_data


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set global appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("BMR Calculator")
        self.geometry("600x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.selected_weight = None
        self.selected_height = None
        self.selected_gender = None
        self.selected_protein = None
        self.selected_calories = None
        self.result_text = None

        self.db_connection = get_db_connection()

        self.create_widgets()

    def create_widgets(self):

        # Gender Selection
        self.gender = ["Please select", "Male", "Female"]
        self.gender_label = ctk.CTkLabel(self, text="Please select gender:")
        self.gender_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        self.gender_menu = ctk.CTkOptionMenu(
            self, values=self.gender, command=self.update_gender)
        self.gender_menu.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Weight Input with slider selection
        self.weight_entry = ctk.CTkLabel(self, text="Select Weight:")
        self.weight_entry.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        self.weight_slider = ctk.CTkSlider(
            self, from_=20, to=200, command=self.update_weight)
        self.weight_slider.grid(
            row=3, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.weight_slider.set(60)

        # Height Input
        self.height_entry = ctk.CTkLabel(self, text="Select Height:")
        self.height_entry.grid(row=4, column=0, padx=20, pady=0, sticky="w")
        self.height_slider = ctk.CTkSlider(
            self, from_=120, to=250, command=self.update_height)
        self.height_slider.grid(
            row=5, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        self.height_slider.set(150)

        # Age Input
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Age")
        self.age_entry.grid(row=6, column=0, columnspan=2,
                            padx=20, pady=10, sticky="ew")

        # Protein Input
        start = 0.3
        stop = 1.5
        step = 0.1

        self.protein_per_g = ["Please select"] + \
            [f"{i:.1f}" for i in np.arange(start, stop + step, step)]
        self.protein_label = ctk.CTkLabel(
            self, text="Protein g/lb Bodyweight:")
        self.protein_label.grid(row=7, column=0, padx=20, pady=0, sticky="w")
        self.protein_menu = ctk.CTkOptionMenu(
            self, values=self.protein_per_g, command=self.update_protein)
        self.protein_menu.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

        # Weight Gain/Loss Input in Calories
        start = -1000
        stop = 1400
        step = 100

        self.calories_change = ["Please select"] + \
            [f"{i}" for i in np.arange(start, stop + step, step)]
        self.calories_label = ctk.CTkLabel(
            self, text="Select Additional daily calories for gain or reduce for weight loss:")
        self.calories_label.grid(row=8, column=0, padx=20, pady=0, sticky="w")
        self.calories_menu = ctk.CTkOptionMenu(
            self, values=self.calories_change, command=self.update_calories)
        self.calories_menu.grid(row=8, column=1, padx=20, pady=10, sticky="ew")

        # Calculate Button
        self.calculate_button = ctk.CTkButton(
            self, text="Calculate BMR", command=self.calculate_bmr)
        self.calculate_button.grid(
            row=9, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Export Data Button
        self.export_button = ctk.CTkButton(
            self, text="Export Data", command=self.export_result)
        self.export_button.grid(
            row=10, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Reset Button
        self.reset_button = ctk.CTkButton(
            self, text="Reset", command=self.reset_fields)
        self.reset_button.grid(
            row=11, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Save to Database Button
        self.save_button = ctk.CTkButton(
            self, text="Save to DB", command=self.save_to_db)
        self.save_button.grid(row=12, column=0, columnspan=2,
                              padx=20, pady=10, sticky="ew")

        # Load from Database Button
        self.load_button = ctk.CTkButton(
            self, text="Load from DB", command=self.load_from_db)
        self.load_button.grid(row=13, column=0, columnspan=2,
                              padx=20, pady=10, sticky="ew")

        # Result Display
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(
            row=14, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    def update_weight(self, value):
        self.selected_weight = value if value else 0
        self.weight_entry.configure(text=f"Selected weight: {
                                    round(self.selected_weight)} kg")

    def update_height(self, value):
        self.selected_height = value if value else 0
        self.height_entry.configure(text=f"Selected height: {
                                    round(self.selected_height)} cm")

    def update_gender(self, value):
        self.selected_gender = value if value != "Please select" else None

    def update_protein(self, value):
        self.selected_protein = float(
            value) if value != "Please select" else None

    def update_calories(self, value):
        self.selected_calories = float(
            value) if value != "Please select" else None

    def update_result(self, value):
        self.result_text = value if value else None
    # (Add all the necessary methods like calculate_bmr, export_result, save_to_db, load_from_db)

    def calculate_bmr(self):
        try:
            weight = self.selected_weight if self.selected_weight is not None else 0
            weight_lb = weight * 2.2
            height = self.selected_height if self.selected_height is not None else 0
            age = int(self.age_entry.get())
            calories_adjust = self.selected_calories if self.selected_calories is not None else 0
            protein = self.selected_protein if self.selected_protein is not None else 0

            if not self.validate_inputs(weight, height, age):
                return

            gender = self.selected_gender
            if gender == "Male":
                bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
            elif gender == "Female":
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
                f"Sedentary: {round(sedentery_cals)} cal/day\n"
                f"Lightly active: {round(light_cals)} cal/day\n"
                f"Moderately active: {round(moderate_cals)} cal/day\n"
                f"Very active: {round(high_cals)} cal/day\n"
                f"Protein per day: {
                    round(protein_per_day)}g / {round(protein_per_day_cals)} cal\n"
                f"Caloric adjustment: {int(calories_adjust)} cal\n"
            )
            self.result_label.configure(text=self.result_text)

        except ValueError:
            self.result_label.configure(text="Please enter valid data.")

    def export_result(self):
        if self.result_text:
            # Prompt the user to enter a file name
            file_name = simpledialog.askstring(
                "Input", "Enter the file name (without extension):", parent=self)

            if file_name:
                file_name = file_name.strip() + ".xlsx"  # Ensure the file has .xlsx extension

                # Parse the result text into a list of dictionaries
                data = []
                for line in self.result_text.splitlines():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data.append({"Description": key.strip(),
                                    "Value": value.strip()})

                # Create a DataFrame from the parsed data
                df = pd.DataFrame(data)

                # Export the DataFrame to an Excel file with the user-provided name
                df.to_excel(file_name, index=False)
                self.result_label.configure(
                    text=f"Data has been exported to {file_name}!")
            else:
                self.result_label.configure(text="File name cannot be empty!")
        else:
            self.result_label.configure(
                text="There is no data to be exported!")

    def validate_inputs(self, weight, height, age):
        if weight is None or weight < 0:
            self.result_label.configure(
                text="Weight can't be negative or invalid!")
            return False

        if height is None or height < 0:
            self.result_label.configure(
                text="Height can't be negative or invalid!")
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
        self.age_entry.delete(0, 'end')
        self.protein_menu.set("Please select")
        self.calories_menu.set("Please select")
        self.result_label.configure(text="")

        # Reset stored values
        self.weight_slider.set(60)
        self.selected_weight = None
        self.weight_entry.configure(text=f"Select Weight:")

        self.height_slider.set(150)
        self.selected_height = None
        self.height_entry.configure(text="Select Height:")

        self.selected_gender = None
        self.selected_protein = None
        self.selected_calories = None
        self.result_text = None

    def save_to_db(self):
        try:
            weight = self.selected_weight if self.selected_weight is not None else 0
            height = self.selected_height if self.selected_height is not None else 0
            age = int(self.age_entry.get())
            gender = self.selected_gender
            protein = self.selected_protein if self.selected_protein is not None else 0
            calories = self.selected_calories if self.selected_calories is not None else 0

            if not self.result_text:
                self.result_label.configure(text="Please calculate BMR first.")
                return

            save_data(self.db_connection, weight, height, age,
                      gender, protein, calories, self.result_text)
            self.result_label.configure(text="Data saved to database.")

        except Exception:
            self.result_label.configure(text=f"There is no data to be saved to database!")

    def load_from_db(self):
        try:
            row = load_latest_data(self.db_connection)

            if row:
                self.selected_weight = row[1]
                self.selected_height = row[2]
                self.age_entry.insert(0, row[3])
                self.selected_gender = row[4]
                self.selected_protein = row[5]
                self.selected_calories = row[6]
                self.result_text = row[7]

                # Update the UI
                self.weight_slider.set(self.selected_weight)
                self.height_slider.set(self.selected_height)
                self.gender_menu.set(self.selected_gender)
                self.protein_menu.set(str(self.selected_protein))
                self.calories_menu.set(str(int(self.selected_calories)))
                self.result_label.configure(text=self.result_text)

            else:
                self.result_label.configure(
                    text="No data found in the database.")

        except Exception as e:
            self.result_label.configure(text=f"Error loading data: {str(e)}")
