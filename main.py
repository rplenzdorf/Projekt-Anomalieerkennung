import sys
import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

p=5
n=10
w=1

class interface(App):
    def build(self):
        root_widget = BoxLayout(orientation="vertical")

        Erkennung = GridLayout(cols = 2,size_hint_y=1.5)
        Erkennung.add_widget(Label(text='Anmomalie'))
        Erkennung.add_widget(Button(text="AN"))

        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=')

        button_grid = GridLayout(cols=4, size_hint_y=2)
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        input_grid = GridLayout(cols=3,size_hint_y=2)
        for i in range(3):
            input_grid.add_widget(Button(text="+"))
        
        input_grid.add_widget(Label(text="Leistung:\n"+str(p)))
        input_grid.add_widget(Label(text="Drehzahl"))
        input_grid.add_widget(Label(text="Wind:\n"+str(w)))

        for i in range(3):
            input_grid.add_widget(Button(text="-"))
        
        hack_button = Button(text='Überschreiben',
                              size_hint_y=None,
                              height=100)

        def p_up(p):
            input_grid.children[5].text="Leistung:\n"+str(20)                 
        input_grid.children[8].bind(on_press=(p_up))

        def p_down(p):
            input_grid.children[5].text="Leistung:\n"+str(0)                   
        input_grid.children[2].bind(on_press=(p_down))

        root_widget.add_widget(Erkennung)
        root_widget.add_widget(input_grid)
        root_widget.add_widget(hack_button)


        return root_widget

if __name__ == "__main__":
    interface().run()