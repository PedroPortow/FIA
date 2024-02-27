from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.label import Label
from kivy.core.window import Window
from board import Board

class GUI(App):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.first_button_pressed = None
        self.button_positions = {}
        self.board = Board()
        self.turn_label = None  

    def build(self):
        Window.size = (800, 600) 
        
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        board_layout = GridLayout(cols=11, padding=10, spacing=10)

        board_data = self.board.board
        for row_index, row in enumerate(board_data):
            for col_index, cell in enumerate(row):
                button = Button(text=cell if cell else '-', background_color=self.get_cell_color(cell, row_index, col_index))
                button.bind(on_press=lambda instance, x=row_index, y=col_index: self.button_pressed(instance, x, y))
                self.button_positions[(row_index, col_index)] = button
                board_layout.add_widget(button)

        main_layout.add_widget(board_layout)

        self.turn_label = Label(text='', font_size=24, size_hint_x=None, width=200)
        self.set_turn_label()
        main_layout.add_widget(self.turn_label)
        
        return main_layout
    
    def set_turn_label(self):
        self.turn_label.text = "Sua vez!" if self.board.is_player_turn else "Vez do robozão :("

    def get_cell_color(self, cell, row, col):
        if self.first_button_pressed == (row, col):
            return (0, 1, 0, 1)  
        elif cell == 'S':
            return (0.5, 0.5, 0.5, 1)
        elif cell == 'G':
            return (1, 0.84, 0, 1)
        elif cell == 'X':
            return (0.8, 0.5, 0, 1)
        else:
            return (0.8, 0.8, 0.8, 1)

    def button_pressed(self, instance, row, col):
        # IF !INVALID POSITION... clicou em uma posição nada ve 
        if not self.first_button_pressed:
            self.first_button_pressed = (row, col)
            self.update_button_colors()  
            return

        if self.first_button_pressed == (row, col):  # CANCELOU A JOGADA!
            self.first_button_pressed = None
            self.update_button_colors()  # update as cores
            return


        print(f"BUTTON ROW => {row}  col => {col} selected")

    def update_button_colors(self):
        for (row, col), button in self.button_positions.items():
            button.background_color = self.get_cell_color(button.text, row, col)

if __name__ == '__main__':
    GUI().run()
