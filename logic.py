import random
import constants as c

def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat

def game_state(mat):
    # check for win cell
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    # check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # check for same cells that touch each other
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = []
    for j in range(c.GRID_LEN):
        partial_new = []
        for i in range(c.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done

def up(game):
    # print("up")
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done

def down(game):
    # print("down")
    # return matrix after shifting down
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done

def left(game):
    # print("left")
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done

def right(game):
    # print("right")
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done

class Game2048:
    def __init__(self, grid_len=4):
        self.grid_len = grid_len
        self.matrix = new_game(grid_len)
        self.score = 0
        self.history_matrices = []
        self.game_over = False
        self.won = False
        
        self.commands = {
            'Up': up,
            'Down': down,
            'Left': left,
            'Right': right,
        }
    
    def get_state(self):
        return [row[:] for row in self.matrix]
    
    def get_score(self):
        return self.score
    
    def get_max_tile(self):
        return max(max(row) for row in self.matrix)
    
    def make_move(self, direction):
        if direction not in self.commands:
            return False
            
        old_matrix = [row[:] for row in self.matrix]
        self.matrix, done = self.commands[direction](self.matrix)
        
        if done:
            self.history_matrices.append([row[:] for row in self.matrix])
            
            self.matrix = add_two(self.matrix)
            
            new_max = self.get_max_tile()
            self.score += sum(sum(row) for row in self.matrix) - sum(sum(row) for row in old_matrix)
            
            state = game_state(self.matrix)
            if state == 'win':
                self.won = True
            elif state == 'lose':
                self.game_over = True
                
            return True
        return False
    
    def is_game_over(self):
        return self.game_over or self.won
    
    def has_won(self):
        return self.won
    
    def get_available_moves(self):
        available_moves = []
        for direction in ['Up', 'Down', 'Left', 'Right']:
            test_matrix = [row[:] for row in self.matrix]
            test_matrix, done = self.commands[direction](test_matrix)
            if done:
                available_moves.append(direction)
        return available_moves
    
    def get_empty_cells(self):
        return sum(row.count(0) for row in self.matrix)
    
    def reset(self):
        self.matrix = new_game(self.grid_len)
        self.score = 0
        self.history_matrices = []
        self.game_over = False
        self.won = False

