import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BMR Calculator")
        self.geometry("800x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Initialize selected_gender variable
        self.selected_gender = None

        # Call the method to set up gender selection
        self.select_gender()
        self.some_other_method()

    def select_gender(self):
        self.gender = ["Male", "Female"]
        
        self.gender_label = ctk.CTkLabel(self, text="Please select gender:")
        self.gender_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")

        # Create an option menu with a default value
        self.operation_menu = ctk.CTkOptionMenu(self, values=self.gender, command=self.update_gender)
        self.operation_menu.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def update_gender(self, selected_value):
        # Update the instance variable with the selected value
        self.selected_gender = selected_value
        print(f"Selected Gender: {self.selected_gender}")

    def some_other_method(self):
        # Use self.selected_gender in other methods
        if self.selected_gender:
            print(f"Using selected gender in another method: {self.selected_gender}")
        else:
            print("No gender selected yet.")

if __name__ == "__main__":
    app = App()
    app.mainloop()

    # Access selected_gender after the main loop (optional)
    print(f"Final selected gender: {app.selected_gender}")
