# importing different features from kivy framework 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

# logic separation (Celsius to Fahrenheit conversion)
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

# logic of (Fahrenheit to Celsius conversion)
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

# creating main UI class which inherits from BoxLayout
class TempLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=15, padding=20, **kwargs)

        # Canvas background (warm-cool gradient style)
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Cool blue tone
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.title = Label(text="🌡 Temperature Converter: Celsius / Fahrenheit", font_size=22, bold=True)

        self.temp_input = TextInput(hint_text="Enter temperature", multiline=False, font_size=20)

        self.result_label = Label(text="Result will appear here", font_size=18)

        # Creating Conversion buttons
        self.to_celsius_btn = Button(text="Convert to Celsius (°C)", background_color=(0.4, 0.6, 1, 1), font_size=18)
        self.to_fahrenheit_btn = Button(text="Convert to Fahrenheit (°F)", background_color=(1, 0.5, 0.5, 1), font_size=18)

        # Connecting buttons to a conversion function 
        self.to_celsius_btn.bind(on_press=self.handle_celsius_conversion)
        self.to_fahrenheit_btn.bind(on_press=self.handle_fahrenheit_conversion)

        # Adding all UI elements to the Layout in order
        self.add_widget(self.title)
        self.add_widget(self.temp_input)
        self.add_widget(self.to_celsius_btn)
        self.add_widget(self.to_fahrenheit_btn)
        self.add_widget(self.result_label)

# Making layout as background responsive. This function automatically calls when window is resized.
    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def handle_celsius_conversion(self, instance):
        temp_str = self.temp_input.text.strip()
        if not temp_str:
            self.result_label.text = "Please enter a value."
            return
        try:
            f = float(temp_str)
            c = fahrenheit_to_celsius(f)
            self.result_label.text = f"{f:.2f} °F = {c:.2f} °C "
        except ValueError:
            self.result_label.text = " Invalid input. Use numbers only."

    def handle_fahrenheit_conversion(self, instance):
        temp_str = self.temp_input.text.strip()
        if not temp_str:
            self.result_label.text = " Please enter a value."
            return
        try:
            c = float(temp_str)
            f = celsius_to_fahrenheit(c)
            self.result_label.text = f"{c:.2f} °C = {f:.2f} °F "
        except ValueError:
            self.result_label.text = " Invalid input. Use numbers only."

# App class & entry point 
class RealTempApp(App):
    def build(self):
        return TempLayout()

RealTempApp().run()
