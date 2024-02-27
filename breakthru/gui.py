# gui.py

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from board import Board  # Importa a classe Board do arquivo board.py

class GUI(App):
    def build(self):
        Window.size = (800, 800)
        layout = GridLayout(cols=11, padding=10, spacing=10)

        board_instance = Board()
        board_data = board_instance.get_board()

        for row in board_data:
            for cell in row:
                if cell == 'P':
                    button = Button(text='P', background_color=(0.5, 0.5, 0.5, 1))
                elif cell == 'G':
                    button = Button(text='G', background_color=(1, 0.84, 0, 1))
                elif cell == 'X':
                    button = Button(text='X', background_color=(0.8, 0.5, 0, 1))
                else:
                    button = Button(text='-', background_color=(0.8, 0.5, 0, 1))
                layout.add_widget(button)

        return layout

if __name__ == '__main__':
    GUI().run()
