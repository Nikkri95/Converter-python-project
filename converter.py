import customtkinter as ctk
import requests
from tkinter import messagebox

# --- Configuration & Styling ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PrecisionConvertPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("UltimateConverter")
        self.geometry("600x600")
        self.resizable(False, False)

        # --- Comprehensive Unit Database ---
        # Logic: All units in a category are converted to a "Base Unit" first.
        self.units_data = {
            "Length": {
                "base": "Meter",
                "factors": {
                    "Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000,
                    "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701,
                    "Nautical Mile": 0.000539957, "Micron": 1000000
                }
            },
            "Weight/Mass": {
                "base": "Kilogram",
                "factors": {
                    "Kilogram": 1, "Gram": 1000, "Milligram": 1000000, "Metric Ton": 0.001,
                    "Pound": 2.20462, "Ounce": 35.274, "Stone": 0.157473, "Grain": 15432.3
                }
            },
            "Volume": {
                "base": "Liter",
                "factors": {
                    "Liter": 1, "Milliliter": 1000, "Cubic Meter": 0.001, "Gallon (US)": 0.264172,
                    "Gallon (UK)": 0.219969, "Quart (US)": 1.05669, "Pint (US)": 2.11338, "Cup": 4.22675
                }
            },
            "Area": {
                "base": "Sq Meter",
                "factors": {
                    "Sq Meter": 1, "Sq Kilometer": 0.000001, "Sq Foot": 10.7639, "Sq Inch": 1550.0,
                    "Acre": 0.000247105, "Hectare": 0.0001, "Sq Mile": 0.0000003861
                }
            },
            "Digital Storage": {
                "base": "Byte",
                "factors": {
                    "Byte": 1, "Kilobyte (KB)": 1/1024, "Megabyte (MB)": 1/(1024**2), 
                    "Gigabyte (GB)": 1/(1024**3), "Terabyte (TB)": 1/(1024**4), "Petabyte (PB)": 1/(1024**5)
                }
            },
            "Time": {
                "base": "Second",
                "factors": {
                    "Second": 1, "Millisecond": 1000, "Minute": 1/60, "Hour": 1/3600, 
                    "Day": 1/86400, "Week": 1/604800, "Month (Avg)": 1/2629743, "Year": 1/31536000
                }
            },
            "Pressure": {
                "base": "Pascal",
                "factors": {
                    "Pascal": 1, "Bar": 1e-5, "PSI": 0.000145038, "Atmosphere": 9.8692e-6, "Torr": 0.00750062
                }
            },
            "Energy": {
                "base": "Joule",
                "factors": {
                    "Joule": 1, "Calorie": 0.239006, "Kilocalorie": 0.000239006, "Watt-hour": 0.000277778, "Electronvolt": 6.242e+18
                }
            },
            "Temperature": "SPECIAL",
            "Currency": "API"
        }

        self.setup_ui()

    def setup_ui(self):
        # Main Layout
        self.main_frame = ctk.CTkFrame(self, corner_radius=25)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=False)

        self.title_label = ctk.CTkLabel(self.main_frame, text="ULTIMATE CONVERTER ", 
                                        font=ctk.CTkFont(size=22, weight="bold", family="Segoe UI"))
        self.title_label.pack(pady=(30, 20))

        # --- Category Selection ---
        self.category_label = ctk.CTkLabel(self.main_frame, text="Category", font=ctk.CTkFont(size=13))
        self.category_label.pack()
        
        self.category_menu = ctk.CTkOptionMenu(self.main_frame, values=list(self.units_data.keys()), 
                                               command=self.update_unit_menus, width=250)
        self.category_menu.pack(pady=10)

        # --- Input Section ---
        self.input_entry = ctk.CTkEntry(self.main_frame, placeholder_text="0.00", 
                                        width=300, height=45, justify="center", 
                                        font=("Arial", 20))
        self.input_entry.pack(pady=20)

        # --- Units Row ---
        self.units_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.units_frame.pack(pady=10)

        self.from_menu = ctk.CTkOptionMenu(self.units_frame, values=["Loading..."], width=130)
        self.from_menu.grid(row=0, column=0, padx=10)

        self.to_menu = ctk.CTkOptionMenu(self.units_frame, values=["Loading..."], width=130)
        self.to_menu.grid(row=0, column=1, padx=10)

        # --- Action Button ---
        self.convert_btn = ctk.CTkButton(self.main_frame, text="CALCULATE PRECISION", 
                                         font=ctk.CTkFont(weight="bold"), height=45,
                                         command=self.perform_conversion, fg_color="#2c7fb8", hover_color="#1a5a8a")
        self.convert_btn.pack(pady=40)

        # --- Result Display ---
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b", corner_radius=10)
        self.result_frame.pack(pady=10, padx=40, fill="x")

        self.result_label = ctk.CTkLabel(self.result_frame, text="Result: ---", 
                                         font=ctk.CTkFont(size=18, weight="bold"), 
                                         text_color="#50C878", height=60)
        self.result_label.pack(fill="both", expand=True)

        # Initial trigger to populate menus
        self.update_unit_menus(self.category_menu.get())

    def update_unit_menus(self, choice):
        if choice == "Currency":
            # Fetch all current currencies from API to populate the menu
            try:
                response = requests.get("https://open.er-api.com/v6/latest/USD")
                data = response.json()
                currencies = list(data["rates"].keys())
                self.from_menu.configure(values=currencies)
                self.to_menu.configure(values=currencies)
            except:
                messagebox.showerror("API Error", "Could not fetch global currencies. Check internet.")
                self.from_menu.configure(values=["USD", "EUR", "GBP"])
                self.to_menu.configure(values=["USD", "EUR", "GBP"])
        
        elif choice == "Temperature":
            temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
            self.from_menu.configure(values=temp_units)
            self.to_menu.configure(values=temp_units)
        
        else:
            # Get units from our dictionary
            units_list = list(self.units_data[choice]["factors"].keys())
            self.from_menu.configure(values=units_list)
            self.to_menu.configure(values=units_list)
        
        # Set default values to the first item in the list
        self.from_menu.set(self.from_menu.cget("values")[0])
        self.to_menu.set(self.to_menu.cget("values")[0])

    def get_live_currency_rate(self, from_curr, to_curr):
        try:
            url = f"https://open.er-api.com/v6/latest/{from_curr}"
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                return data["rates"][to_curr]
        except:
            return None

    def perform_conversion(self):
        try:
            val = float(self.input_entry.get())
            category = self.category_menu.get()
            from_unit = self.from_menu.get()
            to_unit = self.to_menu.get()

            if category == "Currency":
                rate = self.get_live_currency_rate(from_unit, to_unit)
                if rate:
                    res = val * rate
                else:
                    messagebox.showerror("Error", "Currency rate not available.")
                    return

            elif category == "Temperature":
                # Convert to Celsius first
                if from_unit == "Fahrenheit": temp_c = (val - 32) * 5/9
                elif from_unit == "Kelvin": temp_c = val - 273.15
                else: temp_c = val

                # Convert Celsius to Target
                if to_unit == "Fahrenheit": res = (temp_c * 9/5) + 32
                elif to_unit == "Kelvin": res = temp_c + 273.15
                else: res = temp_c

            else:
                # Generic Unit Conversion using Base-Unit Logic
                factors = self.units_data[category]["factors"]
                # Step 1: Convert input to the base unit (Value / factor)
                base_val = val / factors[from_unit]
                # Step 2: Convert base unit to target unit (Base * factor)
                res = base_val * factors[to_unit]

            # Result Formatting
            if res == int(res):
                final_res = str(int(res))
            elif abs(res) < 0.0001 and res != 0:
                final_res = f"{res:.8e}" # Scientific notation for very small numbers
            else:
                final_res = f"{res:.6f}".rstrip('0').rstrip('.') # Clean trailing zeros

            self.result_label.configure(text=f"{final_res} {to_unit}")

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric value.")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PrecisionConvertPro()
    app.mainloop()
