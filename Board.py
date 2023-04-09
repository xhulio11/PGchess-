import pygame

# Seeting global variables 
BLACK = (25, 25, 25)
WHITE = (100, 100, 100)
CIRCLE_COLOR = (154,103,27) 
BOARD_WIDTH = 1900
BOARD_HEIGHT = 1000  
SQUARE_WIDTH = BOARD_WIDTH/8
SQUARE_HEIGHT = BOARD_HEIGHT/8
RADIUS = (SQUARE_WIDTH + SQUARE_HEIGHT)/4 - 10
CIRCLE_WIDTH = 0
PIECE_OFFSET = 30 
FPS = 15

#This class implements chess Board
class Board():
    def __init__(self,):
        # Calling superclass (pygame) and intializing it
        pygame.init()

        self.x_board_previous = 0
        self.y_board_previous = 0
        self.legal_moves = []
        self.game_active = True
        self.pieces = {}
        self.player = '2'
        self.move = 0
        self.position = [['r2','n2','b2','q2','k2','b2','n2','r2'],
                         ['p2','p2','p2','p2','p2','p2','p2','p2'],
                         ['o' ,'o', 'o', 'o', 'o', 'o', 'o' ,'o',],
                         ['o' ,'o', 'o', 'o', 'o', 'o', 'o' ,'o',],
                         ['o' ,'o', 'o', 'o', 'o', 'o', 'o' ,'o',],
                         ['o' ,'o', 'o', 'o', 'o', 'o', 'o' ,'o',],
                         ['p1','p1','p1','p1','p1','p1','p1','p1'],
                         ['r1','n1','b1','q1','k1','b1','n1','r1']]
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT), pygame.RESIZABLE)
        self.x = 0
        self.y = 0
        self.load_assets()


    def draw_board(self,):
        print("HEIGHT", BOARD_HEIGHT)
        # Create a chess board with alternating black and white squares
        for i in range(8):
            for j in range(8):
                if (i + j) % 2:
                    color  = BLACK
                else:
                    color = WHITE
                pygame.draw.rect(self.screen, color, (i*BOARD_WIDTH/8, j*BOARD_HEIGHT/8, BOARD_WIDTH/8, BOARD_HEIGHT/8))
        # Show legal Moves
        for x,y in self.legal_moves:
            pygame.draw.circle(self.screen,CIRCLE_COLOR,(SQUARE_WIDTH*x + SQUARE_WIDTH/2,SQUARE_HEIGHT*y + SQUARE_HEIGHT/2),RADIUS,CIRCLE_WIDTH)
        # Show Pieces 
        for y,row in enumerate(self.position):
            for x,value in enumerate(row):
                if value == 'o':
                    continue
                else:
                    # Print all the pieces that exist an the board
                    self.screen.blit(self.pieces[value], ((BOARD_WIDTH/8)*x + PIECE_OFFSET/2 ,(BOARD_HEIGHT/8)*y + PIECE_OFFSET/2))

        pygame.display.update()


    def control_input(self,):
        # Initializing the board
        self.draw_board()

        """ 
        mouse_clicked:
        --------------------------------------
        This variable is used to move pieces.
        When it is False and mouse is clicked
        in a square where a piece exist then it
        becomes true. When mouse button is 
        pressed again then it can enable the 
        if statement to change the position 
        of the board
        """
        mouse_clicked = False
        

        while self.game_active:
           
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_active = False
                    pygame.quit()

                elif event.type == pygame.VIDEORESIZE:
                    global BOARD_HEIGHT 
                    BOARD_HEIGHT = event.h
                    global BOARD_WIDTH
                    BOARD_WIDTH = event.w
                    global RADIUS 
                    global SQUARE_HEIGHT
                    global SQUARE_WIDTH
                    SQUARE_WIDTH = BOARD_WIDTH/8
                    SQUARE_HEIGHT = BOARD_HEIGHT/8
                    RADIUS = (SQUARE_WIDTH + SQUARE_HEIGHT)/4 - 10

                    self.load_assets()    
                    self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT), pygame.RESIZABLE)
                    self.draw_board()


                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    x_board = int(x/SQUARE_WIDTH)
                    y_board = int(y/SQUARE_HEIGHT)
                    
                    # If mouse button is clicked first time then store the position
                    if(not mouse_clicked and self.position[y_board][x_board] != 'o'):
                        self.x_board_previous = x_board
                        self.y_board_previous = y_board
                        mouse_clicked = True
                        self.show_moves(x_board,y_board)
                        self.draw_board()
                        continue 
                    # if mouse button is clicked second time then check if the move is valid
                    if(mouse_clicked):
                        self.legal_moves.clear()
                        mouse_clicked = False
                        # Increase move and check who's turn is
                        self.move = self.move + 1
                        if self.move % 2 == 1:
                            self.player = '1'
                        elif self.move % 2 == 0:
                            self.player = '2'

                        # Check if move is valid and if it is update the board
                        if(self.move_valid(x_board,y_board,self.player)):
                            self.position[y_board][x_board] = self.position[self.y_board_previous][self.x_board_previous]
                            self.position[self.y_board_previous][self.x_board_previous] = 'o'
                            self.draw_board()
                        else:
                            # If move is not valid, then don't count the move
                            self.legal_moves.clear()
                            self.draw_board()
                            self.move = self.move - 1
                            if(self.move % 2 == 1):
                                self.player == '1'
                            else:
                                self.player == '2'
                        print("----------2C-------")
                        print("move:",self.move)
                        print("player:",self.player)
                        print("--------------------")
                        

    # This functions uploads all the image assets and stores them into a dictionary 
    # depending on what they are representing (pawn, king, queen etc)
    def load_assets(self,):
        pieces = ["bishop","king","knight","pawn","queen","rook"]
        self.pieces = {}
        for piece in pieces:

            image1 = pygame.image.load("w_" + piece + "_svg_NoShadow.png")
            image1 = pygame.transform.scale(image1,(BOARD_WIDTH/8 - PIECE_OFFSET, BOARD_HEIGHT/8 - PIECE_OFFSET))
            image1.set_colorkey((255,255,255))
                
            image2 = pygame.image.load("b_" + piece + "_svg_NoShadow.png")
            image2 = pygame.transform.scale(image2,(BOARD_WIDTH/8 - PIECE_OFFSET, BOARD_HEIGHT/8 - PIECE_OFFSET))
            image2.set_colorkey((255,255,255))
            
            if(piece == "bishop"):
                self.pieces["b1"] = image1
                self.pieces["b2"] = image2
            elif(piece == "king"):
                self.pieces["k1"] = image1
                self.pieces["k2"] = image2
            elif(piece == "knight"):
                self.pieces["n1"] = image1
                self.pieces["n2"] = image2
            elif(piece == "pawn"):
                self.pieces["p1"] = image1
                self.pieces["p2"] = image2
            elif(piece == "queen"):
                self.pieces["q1"] = image1
                self.pieces["q2"] = image2
            else:
                self.pieces["r1"] = image1
                self.pieces["r2"] = image2
            

    # This function checks if the move that the player is trying to do is correct
    # It checks a variety of inputs
    def move_valid(self,x,y,player):
        
        piece = self.position[self.y_board_previous][self.x_board_previous] 
        x_p = self.x_board_previous
        y_p = self.y_board_previous
        
        # If player 1 is trying to play when it is not his turn then return False.
        # Same for plpayer 2
        if ((self.position[y_p][x_p].find('1') == 1 and player != '1') or
           (self.position[y_p][x_p].find('2') == 1 and player != '2')): 
            return False

        # If white/black piece is trying to move to a square where
        # a white/black piece is already there 
        if self.position[y][x].find(player) == self.position[y_p][x_p].find(player):
            return False 

        # If the move is about the movement of the piece on the same
        # place, then do nothing 
        if(x == self.x_board_previous and y == self.y_board_previous):
            return False
        
        # If piece is a pawn 
        if piece == 'p' + player:

            if player == '1':
                # If pawn is the first time it moves then it can move 2 squares
                if (x == x_p and y == y_p - 2 == 4) and self.position[y][x] == 'o':
                    print("2 Move")
                    return True
                # If pawn can move upowards or can capture something in the right or in the left
                if((x == x_p and y == y_p - 1 >= 0 and self.position[y][x] == 'o') or
                        (x == x_p + 1 < 8 and y == y_p - 1 > 0 and self.position[y][x] != 'o' and self.position[y][x].find(player) == -1) or
                        (x == x_p - 1 > 0 and y == y_p - 1 > 0 and self.position[y][x] != 'o' and self.position[y][x].find(player) == -1)):
                    return True
                return False 
            
            elif player == '2':
                # If pawn is the first time it moves then it can move 2 squares
                if x == x_p and y == y_p + 2 == 3 and self.position[y][x] == 'o':
                    return True
                # If pawn can move downwards or can capture something in the right or in the left
                if((x == x_p and y == y_p + 1 < 8 and self.position[y][x] == 'o') or
                        (x == x_p + 1 < 8 and y == y_p + 1 < 8 and self.position[y][x] != 'o' and self.position[y][x].find(player) == -1) or
                        (x == x_p - 1 >= 0 and y == y_p + 1 < 8 and self.position[y][x] != 'o' and self.position[y][x].find(player) == -1)):
                    return True
                return False 
        # If piece is a rook for white 
        elif piece == 'r' + player :
            # Rooks can't move diogonally 
            if ((x_p > x and y_p > y or x_p < x and y_p < y) or (x_p > x and y_p < y or x_p < x and y_p > y)):
                return False 
            
            # White Rooks can't move to a place where is already a white/black piece by one place
            if ((x_p + 1 == x or x_p - 1 == x or y_p + 1 == y or y_p - 1 == y) and self.position[y][x].find(player) == 1):
                return False 
            # Checking if there are pieces on movement to the right
            for i in range(x_p + 1, x):
                if self.position[y][i] != 'o':
                    return False 
            # Checking if there are pieces on movement to the left
            for i in range(x_p - 1, x, -1):
                if self.position[y][i] != 'o':
                    return False
            # Checking if there are pieces on movement to the bottom
            for i in range(y_p + 1, y):
                if self.position[i][x] != 'o':
                    return False 
            # Checking if there are pieces on movement to the top
            for i in range(y_p - 1, y, -1):
                if self.position[i][x] != 'o':
                    return False 
            return True 
        # If piece is a white or black Night
        elif piece == 'n' + player:
            # Checking the movement of the knight is right 
            # Checking if the new square belongs to the player that moves the knight or not 
            if (((x == x_p - 1 >= 0 and y == y_p - 2 >= 0) or (x == x_p - 1 >= 0 and y == y_p + 2 <  8) or
                 (x == x_p + 1 <  8 and y == y_p - 2 >= 0) or (x == x_p + 1 <  8 and y == y_p + 2 <  8) or
                 (x == x_p - 2 >= 0 and y == y_p + 1 >= 0) or (x == x_p - 2 >= 0 and y == y_p - 1 <  8) or
                 (x == x_p + 2 <  8 and y == y_p + 1 >= 0) or (x == x_p + 2 <  8 and y == y_p - 1 <  8))and
                 ((self.position[y][x].find(player) != self.position[y_p][x_p].find(player))or
                 (self.position[y][x] == 'o'))):
                return True 
            else:
                return False
        # If piece is a white or black Bishop
        elif piece == 'b' + player:

            # Bishops moves only diagonaly
            if(abs(x - x_p) != abs(y - y_p)):
                return False
            # Bishop moves diagonaly down-right 
            i = y_p + 1
            j = x_p + 1 
            while(i < y and j < x):
                if self.position[i][j] != 'o':
                    return False
                i = i + 1
                j = j + 1

            # Bishop moves diagonaly down-left
            i = y_p + 1
            j = x_p - 1 
            while(i < y and j > x):
                if self.position[i][j] != 'o':
                    return False
                i = i + 1
                j = j - 1

            # Bishop moves diagonaly up-right
            i = y_p - 1
            j = x_p + 1
            while(i > y and j < x):
                if self.position[i][j] != 'o':
                    return False
                i = i - 1
                j = j + 1

            # Bishop moves diagonaly up-left
            i = y_p - 1
            j = x_p - 1
            while(i > y and j > x):
                if self.position[i][j] != 'o':
                    return False
                i = i - 1
                j = j - 1
            return True 
        # If Queen is white/black 
        elif piece == 'q' + player:
            #Does Queen moves like a bishop?
            if(abs(x - x_p) == abs(y - y_p)):
                # Bishop moves diagonaly down-right 
                i = y_p + 1
                j = x_p + 1 
                while(i < y and j < x):
                    if self.position[i][j] != 'o':
                        return False
                    i = i + 1
                    j = j + 1

                # Bishop moves diagonaly down-left
                i = y_p + 1
                j = x_p - 1 
                while(i < y and j > x):
                    if self.position[i][j] != 'o':
                        return False
                    i = i + 1
                    j = j - 1

                # Bishop moves diagonaly up-right
                i = y_p - 1
                j = x_p + 1
                while(i > y and j < x):
                    if self.position[i][j] != 'o':
                        return False
                    i = i - 1
                    j = j + 1

                # Queen moves diagonaly up-left
                i = y_p - 1
                j = x_p - 1
                while(i > y and j > x):
                    if self.position[i][j] != 'o':
                        return False
                    i = i - 1
                    j = j - 1
                return True 
            # Queen moves like a rook
            elif (x_p == x or y_p == y):
                # White Queen can't move to a place where is already a white/black piece by one place
                if ((x_p + 1 == x or x_p - 1 == x or y_p + 1 == y or y_p - 1 == y) and self.position[y][x].find(player) == 1):
                    return False 
                # Checking if there are pieces on movement to the right
                for i in range(x_p + 1, x):
                    if self.position[y][i] != 'o':
                        return False 
                # Checking if there are pieces on movement to the left
                for i in range(x_p - 1, x, -1):
                    if self.position[y][i] != 'o':
                        return False
                # Checking if there are pieces on movement to the bottom
                for i in range(y_p + 1, y):
                    if self.position[i][x] != 'o':
                        return False 
                # Checking if there are pieces on movement to the top
                for i in range(y_p - 1, y, -1):
                    if self.position[i][x] != 'o':
                        return False 
                return True
            else:
                return False
        elif piece == 'k' + player:
            if(abs(x_p - x) <= 1 and abs(y_p - y) <= 1 ):
                return True
            elif(x - x_p == 2 and y == y_p and self.position[y][7] == 'r' + player ):
                self.position[y][5] = 'r' + player
                self.position[y][7] = 'o'
                return True
            else:
                return False
        return True


    def show_moves(self,x,y):
        piece = self.position[y][x]
        
        # Show legal moves for Pawn
        if piece == 'p1' :
            # for white
            if y == 6:
                for i in range(y-1,y-3,-1):
                    if self.position[i][x] == 'o':
                        self.legal_moves.append((x,i))
            else:
                # Showing legal move upwards
                if self.position[y-1][x] == 'o':
                    self.legal_moves.append((x,y-1))
                # Showing legal move up-left
                if self.position[y-1][x-1] != 'o' and self.position[y][x][1] != self.position[y-1][x-1][1]:
                    self.legal_moves.append((x-1,y-1))
                # Showing legal move up-right
                if self.position[y-1][x+1] != 'o' and self.position[y][x][1] != self.position[y-1][x+1][1]:
                    self.legal_moves.append((x+1,y-1))
        elif piece == 'p2':
            # for black
            if y == 1:
                for i in range(y+1,y+3):
                    if self.position[i][x] == 'o':
                        self.legal_moves.append((x,i))
            else:
                # Showing legal move downwards
                if self.position[y+1][x] == 'o':
                    self.legal_moves.append((x,y+1))
                # Showing legal move down-left
                if self.position[y+1][x-1] != 'o' and self.position[y][x][1] != self.position[y+1][x-1][1]:
                    self.legal_moves.append((x-1,y+1))
                # Showign legal move down-right
                if self.position[y+1][x+1] != 'o' and self.position[y][x][1] != self.position[y+1][x+1][1]:
                    self.legal_moves.append((x+1,y+1))
        # Show legal moves for Rook and Queen
        if piece[0] == 'r' or piece[0] == 'q':
            #showing legal moves to the right
            for i in range(x+1,8):
                if self.position[y][i] == 'o':
                    self.legal_moves.append((i,y))
                else:
                    if self.position[y][i][1] != piece[1]:
                        self.legal_moves.append((i,y))
                    break                 
            #showing legal moves to the left
            for i in range(x-1,-1,-1):
                if self.position[y][i] == 'o':
                    self.legal_moves.append((i,y))
                else:
                    if self.position[y][i][1] != piece[1]:
                        self.legal_moves.append((i,y))
                    break    
            #showing legal moves upwards
            for i in range(y-1,-1,-1):
                if self.position[i][x] == 'o':
                    self.legal_moves.append((x,i))
                else:
                    if self.position[i][x][1] != piece[1]:
                        self.legal_moves.append((x,i))
                    break 
            #showing legal moves downwards
            for i in range(y+1,8):
                if self.position[i][x] == 'o':
                    self.legal_moves.append((x,i))
                else:
                    if self.position[i][x][1] != piece[1]:
                        self.legal_moves.append((x,i))
                    break
        # Legal moves for Bishop and Queen
        if piece[0] == 'b' or piece[0] == 'q':
            #showing legal moves up-right
            i = x
            j = y
            while(i < 7 and j > 0):
                i += 1
                j -= 1
                if self.position[j][i] == 'o':
                    self.legal_moves.append((i,j))
                else:
                    if self.position[j][i][1] != piece[1]:
                        self.legal_moves.append((i,j))
                    break
            #showing legal moves up-left
            i = x
            j = y
            while(i > 0 and j > 0):
                i -= 1
                j -= 1
                if self.position[j][i] == 'o':
                    self.legal_moves.append((i,j))
                else:
                    if self.position[j][i][1] != piece[1]:
                        self.legal_moves.append((i,j))
                    break
            #showing legal moves down-right
            i = x
            j = y
            while(i < 7 and j < 7):
                i += 1
                j += 1
                if self.position[j][i] == 'o':
                    self.legal_moves.append((i,j))
                else:
                    if self.position[j][i][1] != piece[1]:
                        self.legal_moves.append((i,j))
                    break
            #showing legal moves down-left
            i = x
            j = y
            while(i > 0 and j < 7):
                i -= 1
                j += 1
                if self.position[j][i] == 'o':
                    self.legal_moves.append((i,j))
                else:
                    if self.position[j][i][1] != piece[1]:
                        self.legal_moves.append((i,j))
                    break
        # Legal moves for Knight
        if piece[0] == 'n':
            pass 




