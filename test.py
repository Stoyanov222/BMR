import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("400x250")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Input fields for numbers
        self.input_1 = customtkinter.CTkEntry(self, placeholder_text="Enter first number")
        self.input_1.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.input_2 = customtkinter.CTkEntry(self, placeholder_text="Enter second number")
        self.input_2.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Dropdown menu for selecting operation
        self.operations = ["Add", "Subtract", "Multiply", "Divide"]
        self.operation_menu = customtkinter.CTkOptionMenu(self, values=self.operations)
        self.operation_menu.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Button to trigger the calculation
        self.button = customtkinter.CTkButton(self, text="Calculate", command=self.calculate)
        self.button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Label to display the result
        self.result_label = customtkinter.CTkLabel(self, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def calculate(self):
        try:
            num1 = float(self.input_1.get())
            num2 = float(self.input_2.get())
            operation = self.operation_menu.get()
            if operation == "Add":
                result = num1 + num2
            elif operation == "Subtract":
                result = num1 - num2
            elif operation == "Multiply":
                result = num1 * num2
            elif operation == "Divide":
                result = num1 / num2
            self.result_label.configure(text=f"Result: {result}")
        except ValueError:
            self.result_label.configure(text="Invalid input")
        except ZeroDivisionError:
            self.result_label.configure(text="Error: Division by zero")

if __name__ == "__main__":
    app = App()
    app.mainloop()
