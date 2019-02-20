# Index assignment for the matrix representation of the game board
player_1 = 1
player_2 = 2
empty = 0

# Game board size
size = 8

player_1_piece="X"
player_2_piece="O"
empty_space=" "

space_character= { player_1: player_1_piece,
                    player_2: player_2_piece,
                    empty: empty_space }

row_names=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
row_map=dict(zip(row_names,range(size)))

column_names=map(str,range(1,size+1))
column_map=dict(zip(column_names,range(size)))

left_move=0
right_move=1

player_1_left_move=(1,1)
player_1_right_move=(1,-1)

player_2_left_move=(-1,-1)
player_2_right_move=(-1,1)

moves={ player_1: {left_move: player_1_left_move, 
                   right_move:player_1_right_move},
        player_2: {left_move: player_2_left_move, 
                   right_move: player_2_right_move}}


def make_game_board(size=8):
    # Make an empty board
    board=[[empty]*size for i in range(size)]
    
    # Even Columns
    for i in range(0,size,2):
        board[1][i]=player_1
        board[-1][i]=player_2
        board[-3][i]=player_2
        
    # Odd Columns
    for i in range(1,size,2):
        board[0][i]=player_1
        board[2][i]=player_1
        board[-2][i]=player_2
    
    return board



def print_message(message,verbose=True):
    if verbose:
        print message

def move_piece(board,player,location,move,verbose=True):
    x,y=location
    
    # Check if player's piece is at location
    if not board[x][y] == player:
        print_message("Player does not have piece at location.",verbose)
        return False

    # Fetch the offset for the move
    x_offset,y_offset = moves[player][move]
    
    # Make sure the move is on the board:
    move_possible= x+x_offset < size and \
                    x+x_offset >= 0 and \
                    y+y_offset < size and \
                    y+y_offset >= 0
                
                
    jump_possible= x+2*x_offset < size and \
                    x+2*x_offset >= 0 and \
                    y+2*y_offset < size and \
                    y+2*y_offset >= 0
    
    if not (move_possible or jump_possible):
        print_message("Move is off of board.",verbose)
        return False
        
    # Try the move
    # Is the target space empty
    if move_possible and \
        board[x+x_offset][y+y_offset]==empty:
    
        # Make the move
        # Empty the spot
        board[x][y]=empty
        # Place player in new spot
        board[x+x_offset][y+y_offset]=player
        print_message("Moved.",verbose)            

        return True
    # Does the target space have an opponent's piece, and the space after empty
    elif jump_possible and \
            board[x+x_offset][y+y_offset]!=player and \
            board[x+2*x_offset][y+2*y_offset]==empty:

        # Make the move
        # Empty the spot
        board[x][y]=empty
        # Remove the oppoent's piece
        board[x+x_offset][y+y_offset]=empty
        # Move player to new spot
        board[x+2*x_offset][y+2*y_offset]=player
        print_message("Took opponent's piece.",verbose)
        
        return True
    else:
        print_message("Move not possible.",verbose)
        return False


def draw_board(board):
    print " ",
    for j in range(8):
        print column_names[j],
    print
    
    for i in range(8):
        print row_names[i],
        for j in range(8):
            print space_character[board[i][j]],
        print

def parse_location(l_string):
    if not isinstance(l_string,str):
        print_message("Bad Input. Location must be string.")
        return False
    
    if len(l_string)!=2:
        print_message("Bad Input. Location must be 2 characters.")
        return False
    
    row=l_string[0].upper()
    col=l_string[1].upper()
    
    if not row in row_names:
        print_message("Bad Row.")
        return False

    if not col in column_names:
        print_message("Bad Column.")
        return False

    return row_map[row],column_map[col]
    
def parse_move(m_string):
    if not isinstance(m_string,str):
        print_message("Bad Input. Location must be string.")
        return -1
    
    if len(m_string)!=1:
        print_message("Bad Input. Location must be 1 character.")
        return -1
    
    if m_string.upper()=="L":
        return left_move

    if m_string.upper()=="R":
        return right_move

    print_message("Bad Move. must be R/L.")
    
    return -1

def nice_move_piece(board,player,location,move):
    loc=parse_location(location)
    mov=parse_move(move)

    if loc and mov!=-1:
        return move_piece(board,player,loc,mov)
    else:
        return print_message("Bad move.")

def take_move(board,player):
    good_move=False
    
    while not good_move:
        loc_str =raw_input("Input location:")
        mov_str =raw_input("Input move (L/R):")
            
        good_move = nice_move_piece(board,player,loc_str,mov_str)

def count_pieces(board,player):
    n=0
    for i in range(8):
        for j in range(8):
            if board[i][j]==player:
                n+=1                
    return n


def game_won(board):
    player_1_n=count_pieces(board,player_1)
    player_2_n=count_pieces(board,player_2)

    if player_1_n==0:
        return player_2
    if player_1_n==0:
        return player_1

    return False

def checkers_game():
    
    print "Welcome to Checkers."
    print "--------------------"

    # Make a game board
    board_0=make_game_board()
    
    # Start with player 1
    player=player_1
    
    this_game_won=False
    while not this_game_won:
        # Draw the board
        draw_board(board_0)
        
        # Make a move
        print "Player",player,"move:"
        take_move(board_0,player)

        # Check if the game has been won
        this_game_won=game_won(board_0)

        # Switch players
        if player==player_1:
            player=player_2
        else:
            player=player_1
            
        
    print "Winner is player:",this_game_won
          
