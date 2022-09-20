import pygame
import time
pygame.font.init()

def constraint_propagation(board):
    #Assigns each cube a unique index or the repeating values within board will make the potential dictionary contain only numbers 0-9
    constraint_board = [
    ["A1","A2","A3","A4","A5","A6","A7","A8","A9"],
    ["B1","B2","B3","B4","B5","B6","B7","B8","B9"],
    ["C1","C2","C3","C4","C5","C6","C7","C8","C9"],
    ["D1","D2","D3","D4","D5","D6","D7","D8","D9"],
    ["E1","E2","E3","E4","E5","E6","E7","E8","E9"],
    ["F1","F2","F3","F4","F5","F6","F7","F8","F9"],
    ["G1","G2","G3","G4","G5","G6","G7","G8","G9"],
    ["H1","H2","H3","H4","H5","H6","H7","H8","H9"],
    ["I1","I2","I3","I4","I5","I6","I7","I8","I9"]
    ]
    #stores the potential values each cube could take (1-9 inclusive)
    potential = {}
    #the following loop searches through all the cubes on the same row/column as the intended cube
    #if any of the 'peers' has a guaranteed value within it, it has 0 potential values
    #due to the rules of sudoku, the current cube can't contain any values that its peers are guaranteed to have
    #peers is a string of each guaranteed value of the current cubes neighbours which is then removed from the current cubes potential
    #if the potential of the current cube is a guaranteed value(length 1), the cube updates within the main board to said value
    peers = ""
    for i in range(9):
        for j in range(9):
            peers = ""
            if board[i][j] == 0:
                potential[constraint_board[i][j]] = "123456789"
            else:
                potential[constraint_board[i][j]] = "0"
            if len(potential[constraint_board[i][j]]) != 1:
                for x in range(9):
                    #checks to avoid duplicate numbers within peers
                    if board[i][x] != 0 and (str(board[i][x]) in list(peers)) == False:
                        peers = peers+str(board[i][x])
                    if board[x][j] != 0 and (str(board[x][j]) in list(peers)) == False:
                        peers = peers+str(board[x][j])
                    #updates the cubes potential values to "123456789"-peers by comparing each character's ascii value within "123456789" and peers and replacing any matches with "None"(removing it from the string)
                    potential[constraint_board[i][j]] = potential[constraint_board[i][j]].translate({ord(i): None for i in peers})
                    if len(potential[constraint_board[i][j]]) == 1:
                        board[i][j] = int(potential[constraint_board[i][j]])
           
def findemptybox(board):
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)

    return False

def backtracking(board):
    #finds an empty box, places '1' into the box and tests to see if the board is valid
    #if the board is valid, the value is permanently placed into said box, if not, the value i+1 is tested
    global start
    start = time.time()
    if constraint_mode:
        constraint_propagation(board)
    
    find = findemptybox(board)
    
    if find == False:
        global end
        end = time.time()
        global solution
        solution = board
        return True
    else:
        row, col = find

    for i in range(1,10):
        if validpos(board, i, (row, col)) == True:
            board[row][col] = i

            if backtracking(board) == True:
                return True

            board[row][col] = 0

    return False

def validpos(board, num, pos):
    #pos given as (x,y) pos[0] = x = column
    #pos[1] = y = row
    
    #col
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    #row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    #3x3
    xaxis = pos[1] // 3
    yaxis = pos[0] // 3

    for i in range(xaxis*3, xaxis*3 + 3):
        for j in range(yaxis*3, yaxis*3 + 3):
            if board[j][i] == num and (j,i) != pos:
                return False
    
    return True

class Button:
    
    def __init__(self, width, height, xpos, ypos, text):
        self.width = width
        self.height = height
        self.xpos = xpos
        self.ypos = ypos
        self.text = text

    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), (self.xpos, self.ypos, self.width, self.height))

        font = pygame.font.SysFont("comicsans", 50)
        text = font.render(self.text, 1, (0,0,0))
        #centers the text
        window.blit(text, (self.xpos + (self.width/2 - text.get_width()/2), self.ypos + (self.height/2 - text.get_height()/2)))

    def clicked(self, pos):
        if pos[0] > self.xpos and pos[1] > self.ypos and pos[0] < self.xpos + self.width and pos[1] < self.ypos + self.height:
            return True
        return False
    
class Grid:
    
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
        self.width = width
        self.height = height
        self.board2 = None
        self.currentpos = None

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def get_cubes(self):
        return self.cubes
    
    def copyboard(self):
        #creates a copy of the board (makes code less chunky when checking board array)
        self.board2 = [[self.cubes[i][j].value for j in range(9)] for i in range(9)]


    def place(self, val):
        row, col = self.currentpos
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.copyboard()
            #checks if number is valid before placing it
            if validpos(self.board2, val, (row,col)) == True and backtracking(self.board2) == True:
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.copyboard()
                return False

    def temp(self, val):
        #temp value to check if valid
        row, col = self.currentpos
        self.cubes[row][col].set_temp(val)

    def draw(self, window):
        #grid
        gap = self.width / 9
        for i in range(10):
            if i % 3 == 0 and i != 0:
                bold = 5
            else:
                bold = 1
            pygame.draw.line(window, (0,0,0), (0, i*gap), (self.width, i*gap), bold)
            pygame.draw.line(window, (0, 0, 0), (i*gap, 0), (i*gap, self.height), bold)

        #cubes
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].draw(window)

    def select(self, row, col):
        #unselects others and selects current box
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].currentpos = False

        self.cubes[row][col].currentpos = True
        self.currentpos = (row, col)

    def clear(self):
        row, col = self.currentpos
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        #gets the box where the user clicks into integer values
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return False

    def is_finished(self):
        for i in range(9):
            for j in range(9):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.currentpos = False

    def draw(self, window):
        
        font = pygame.font.SysFont("comicsans", 50)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value != 0:
            text = font.render(str(self.value), 1, (0,0,0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.currentpos:
            pygame.draw.rect(window, (0,255,0), (x,y, gap,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def get_col(self):
        return self.col

    def get_row(self):
        return self.row

def redraw_window(window, board):
    
    window.fill((255,255,255))
    font = pygame.font.SysFont("comicsans", 40)
    board.draw(window)
    constraintbutton.draw(window)
    backtrackingbutton.draw(window)

    
def complete_board(window, board):
    #uses the same draw subroutine in grid class
    window.fill((255,255,255))
    gap = board.get_width() / 9
    for i in range(10):
        if i % 3 == 0 and i != 0:
            bold = 4
        else:
            bold = 1
        pygame.draw.line(window, (0,0,0), (0, i*gap), (board.get_width(), i*gap), bold)
        pygame.draw.line(window, (0, 0, 0), (i*gap, 0), (i*gap, board.get_height()), bold)
    font = pygame.font.SysFont("comicsans", 40)
    #same draw suborutine for cubes but uses the solved array instead
    for i in range(9):
        for j in range(9):
            current = solution[i][j]
            x = board.get_cubes()[i][j].get_col() * gap
            y = board.get_cubes()[i][j].get_row() * gap
            text = font.render(str(current),1,(255,0,0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
    constraintbutton.draw(window)
    backtrackingbutton.draw(window)

def main():
    print("""Rules:
1. Each row should have numbers 1-9 inclusive without duplicates.
2. Each column should have numbers 1-9 inclusive without duplicates.
3. Each grid should have numbers 1-9 inclusive without duplicates.
Click on a cube you wish to update, input a number then press enter for it to take effect.
Once you want the board to be solved, click either "Backtrack" or "Constraint".
""")
    window = pygame.display.set_mode((600,700))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 600, 600)
    global constraintbutton
    global backtrackingbutton
    constraintbutton = Button(250, 90, 300, 610, "Constraint")
    backtrackingbutton = Button(250, 90, 0, 610, "Backtrack")
    numb = 0
    errors = 0
    run = True
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    numb = 1
                if event.key == pygame.K_2:
                    numb = 2
                if event.key == pygame.K_3:
                    numb = 3
                if event.key == pygame.K_4:
                    numb = 4
                if event.key == pygame.K_5:
                    numb = 5
                if event.key == pygame.K_6:
                    numb = 6
                if event.key == pygame.K_7:
                    numb = 7
                if event.key == pygame.K_8:
                    numb = 8
                if event.key == pygame.K_9:
                    numb = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    numb = 0
                if event.key == pygame.K_RETURN:
                    i, j = board.currentpos
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp) != True:
                            errors += 1
                        numb = 0

                        if board.is_finished() == True:
                            print("Game over")
                            pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                global constraint_mode
                constraint_mode = False
                pos = pygame.mouse.get_pos()
                constraintpressed = constraintbutton.clicked(pos)
                backtrackingpressed = backtrackingbutton.clicked(pos)

                if backtrackingpressed or constraintpressed:
                    if constraintpressed:
                        constraint_mode = True
                    complete_board(window, board)
                    pygame.display.update()
                    print("Total errors:",errors)
                    print("Time taken:",end-start)
                    run = False
                
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    numb = 0

        if board.currentpos and numb != 0:
            board.temp(numb)
            
        if run:
            redraw_window(window,board)
            pygame.display.update()

main()
