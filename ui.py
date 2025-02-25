from tkinter import Frame, Label, CENTER
import constants as c
from logic import Game2048

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        
        self.game = Game2048()
        
        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        # Key mapping for UI
        self.key_commands = {
            c.KEY_UP: 'Up',
            c.KEY_DOWN: 'Down',
            c.KEY_LEFT: 'Left',
            c.KEY_RIGHT: 'Right',
            c.KEY_UP_ALT1: 'Up',
            c.KEY_DOWN_ALT1: 'Down',
            c.KEY_LEFT_ALT1: 'Left',
            c.KEY_RIGHT_ALT1: 'Right',
            c.KEY_UP_ALT2: 'Up',
            c.KEY_DOWN_ALT2: 'Down',
            c.KEY_LEFT_ALT2: 'Left',
            c.KEY_RIGHT_ALT2: 'Right',
        }

        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        matrix = self.game.get_state()
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()
        
        # Check game state
        if self.game.has_won():
            self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        elif self.game.is_game_over():
            self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def key_down(self, event):
        key = event.keysym
        if key == c.KEY_QUIT: 
            exit()
        if key == c.KEY_BACK and len(self.game.history_matrices) > 1:
            self.game.matrix = self.game.history_matrices.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.game.history_matrices))
        elif key in self.key_commands:
            done = self.game.make_move(self.key_commands[key])
            if done:
                self.update_grid_cells()

    # NEED TO IMPLEMENT:
    # method for GA to play the game
    
    # if self.game.has_won():
    # elif self.game.is_game_over():
