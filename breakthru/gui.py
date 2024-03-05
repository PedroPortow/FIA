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
        self.board = Board()
        self.board.on_ai_turn_finished = self.update_ui
       
        self.first_button_pressed = None
        self.button_positions = {}
        self.turn_label = None  
        self.status_label = None  

    def build(self):
        Window.size = (800, 600)
        self.title = 'Breakthru'
        return self.build_menu()  
    
    def build_menu(self):
        menu_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        btn_play_vs_ai = Button(text='Jogar contra IA', size_hint=(None, None), size=(200, 50))
        btn_play_vs_ai.bind(on_press=self.set_mode_play_vs_ai)

        menu_layout.add_widget(btn_play_vs_ai)

        return menu_layout
    
    def build_game(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)  
        board_layout = GridLayout(cols=7, padding=10, spacing=2) 

        board_data = self.board.board
        for row_index, row in enumerate(board_data):
            for col_index, cell in enumerate(row):
                button = Button(text=cell if cell else '-', background_color=self.get_cell_color(cell, row_index, col_index))
                button.bind(on_press=lambda instance, x=row_index, y=col_index: self.button_pressed(instance, x, y))
                self.button_positions[(row_index, col_index)] = button
                board_layout.add_widget(button)

        main_layout.add_widget(board_layout)

        labels_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=5)
        self.turn_label = Label(text='', font_size=24, size_hint_y=None, height=50)
        self.status_label = Label(text='', font_size=20, size_hint_y=None, height=50)
        
        labels_layout.add_widget(self.turn_label)  
        labels_layout.add_widget(self.status_label)  

        main_layout.add_widget(labels_layout) 

        if self.board.mode == "player_vs_ai":
            self.start_mode_player_vs_ai()

        return main_layout

    def set_mode_play_vs_ai(self, instance):
        self.board.mode = 'player_vs_ai'
        self.start_game_layout()  

    def start_game_layout(self):
        self.root.clear_widgets()
        self.root.add_widget(self.build_game())
        
    def set_turn_label(self):
        if self.board.mode == 'player_vs_ai':
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
        
    def print_status_label(self, message):
        self.status_label.text = message

    def button_pressed(self, instance, row, col):
        print(self.board.turn)
        if not self.board.is_player_turn():
            self.print_status_label("Não é sua vez!")
            return

        if not self.first_button_pressed: # PRIMEIRA BOTÃO PRESSIONADO
            if not self.board.is_valid_first_press(row, col): # verificação de pos invalida
                self.print_status_label("INVALID FIRST PRESS")
                return 

            self.first_button_pressed = (row, col)
            self.update_button_colors()  
            return

        if self.first_button_pressed == (row, col):  # CANCELOU A JOGADA!
            self.first_button_pressed = None
            self.update_button_colors()  # update as cores
            return
        
        if self.board.is_valid_play(self.first_button_pressed[0], self.first_button_pressed[1], row, col): # aqui tem que adicionar limitação de 1 casa por vez
            self.board.make_play(self.first_button_pressed[0], self.first_button_pressed[1], row, col)
            self.first_button_pressed = None
            self.board.switch_player()
            self.board.ai_player_turn()            

    def start_mode_player_vs_ai(self):
        self.set_turn_label()
        if self.board.is_ai_turn():  
            self.print_status_label("ai")
            self.board.ai_player_turn()

    def update_ui(self):
        self.set_turn_label()
        for (row, col), button in self.button_positions.items():
            cell = self.board.board[row][col]
            button.text = cell if cell else '-'
            button.background_color = self.get_cell_color(cell, row, col)

    def update_button_colors(self):
        for (row, col), button in self.button_positions.items():
            button.background_color = self.get_cell_color(button.text, row, col)

if __name__ == '__main__':
    GUI().run()
