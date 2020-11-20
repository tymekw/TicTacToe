import random


def get_min_max_board(board):
    min_max_board = [i for i in range(0, 9)]
    counter = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == 'X':
                min_max_board[counter] = 'X'
            if board[i][j] == 'O':
                min_max_board[counter] = 'O'
            counter += 1
    return min_max_board


def get_empty_spots(min_max_board):
    empty_spots = []
    for i in range(0, 9):
        if min_max_board[i] != 'X' and min_max_board[i] != 'O':
            empty_spots.append(i)
    return empty_spots


def get_board_from_min_max(min_max_board):
    new_board = [[" " for i in range(0, 3)],
                 [" " for i in range(3, 6)],
                 [" " for i in range(6, 9)]]
    counter = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if min_max_board[counter] == counter:
                new_board[i][j] = ' '
            if min_max_board[counter] == 'X':
                new_board[i][j] = 'X'
            if min_max_board[counter] == 'O':
                new_board[i][j] = 'O'
            counter += 1
    return new_board


def minmax(min_max_board, player, ai_player):
    if ai_player == 'X':
        human = 'O'
    else:
        human = 'X'

    # available spots
    empty_spots = get_empty_spots(min_max_board)

    # check terminal states and add value
    new_board = get_board_from_min_max(min_max_board)
    if check_winner(new_board) == human:
        score = -10
        return score
    elif check_winner(new_board) == ai_player:
        score = 10
        return score
    elif not empty_spots:
        score = 0
        return score

    # collects all objects
    moves = []

    for i in range(0, len(empty_spots)):
        #move = {'index': min_max_board[empty_spots[i]]}
        move = {}
        move['index'] = min_max_board[empty_spots[i]]

        min_max_board[empty_spots[i]] = player

        if player == ai_player:
            result = minmax(min_max_board, human, ai_player)
            move['score'] = result
        else:
            result = minmax(min_max_board, ai_player, ai_player)
            move['score'] = result

        # reset board
        min_max_board[empty_spots[i]] = empty_spots[i]

        moves.append(move)

    best_move = None
    if player == ai_player:
        best_score = -10000
        for i in range(0, len(moves)):
            #print(moves[i].get('score'))
            if moves[i].get('score') > best_score:
                best_score = moves[i].get('score')
                best_move = moves[i].get('index')
    else:
        best_score = 10000
        for i in range(0, len(moves)):
            #print(moves[i].get('score'))
            if moves[i].get('score') < best_score:
                best_score = moves[i].get('score')
                best_move = moves[i].get('index')
    return best_move



# creates new board same as board given
def copy_board(board):
    new_board = [[" " for i in range(0, 3)],
             [" " for i in range(3, 6)],
             [" " for i in range(6, 9)]]
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == ' ':
                new_board[i][j] = ' '
            if board[i][j] == 'X':
                new_board[i][j] = 'X'
            if board[i][j] == 'O':
                new_board[i][j] = 'O'
    return new_board


# returns clean board
def clean_board():
    board = [[" " for i in range(0, 3)],
             [" " for i in range(3, 6)],
             [" " for i in range(6, 9)]]
    return board


# prints board
def print_board(board):
    print("---------")
    for row in board:
        print('|', " ".join(row), '|')
    print("---------")


# reads coordinates from user
def read_coordinates(board):
    xy = input("Enter coordinates: ")
    if len(xy) > 1:
        x = xy[0]
        y = xy[2]
    else:
        print("You should enter numbers!")
        return read_coordinates(board)
    try:
        y = int(y)
        x = int(x)
    except ValueError:
        print("You should enter numbers!")
        return read_coordinates(board)
    my_y = int(x) - 1
    if 1 <= y <= 3 and 1 <= x <= 3:
        if y == 1:
            my_x = 2
        elif y == 2:
            my_x = 1
        elif y == 3:
            my_x = 0
        if board[my_x][my_y] == 'X' or board[my_x][my_y] == 'O':
            print("This cell is occupied! Choose another one!")
            return read_coordinates(board)
    else:
        print("Coordinates should be from 1 to 3!")
        return read_coordinates(board)
    return [my_x, my_y]


# check who should make move x or o
def user(board):
    x = 0
    o = 0
    for i in range(0, 3):
        x += board[i].count("X")
        o += board[i].count("O")
    if x <= o:
        return "X"
    elif x > o:
        return "O"


# updates board after move
def update_board(board, user, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    board[x][y] = user
    return board


# looks for 3 x or o in row
def check_rows(board):
    for row in board:
        if row.count("X") == 3:
            return "X"
        if row.count("O") == 3:
            return "O"
    return None


# looks for 3 x or o in column
def check_columns(board):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == 'X':
            return "X"
        if board[0][i] == board[1][i] == board[2][i] == 'O':
            return "O"
    return None


# looks for 3 x or 0 in diagonals
def check_diagonal(board):
    if board[0][0] == board[1][1] == board[2][2] == 'X':
        return 'X'
    if board[0][2] == board[1][1] == board[2][0] == 'X':
        return 'X'
    if board[0][0] == board[1][1] == board[2][2] == 'O':
        return 'O'
    if board[0][2] == board[1][1] == board[2][0] == 'O':
        return 'O'
    return None


# checks board for winner
def check_winner(board):
    if check_columns(board):
        return check_columns(board)
    elif check_rows(board):
        return check_rows(board)
    elif check_diagonal(board):
        return check_diagonal(board)
    else:
        return None


# checks if there is a draw
def is_game_finished(board):
    for row in board:
        if " " in row:
            return False
    return True


# combines draw and win
def check_end_of_game(board):
    if check_winner(board):
        print(check_winner(board), "wins")
        return True
    if is_game_finished(board):
        print("Draw")
        return True


# returns coordinates from AI lvl easy
def get_computer_coordinates_easy(board):
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    if board[x][y] == ' ':
        return [x, y]
    else:
        return get_computer_coordinates_easy(board)


# looks for win in next move
def winning_coordinates(board, usr):
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == ' ':
                board[i][j] = usr
                if check_winner(board):
                    board[i][j] = ' '
                    return [i, j]
                board[i][j] = ' '
    return None


# looks for lose in next move of opponent
def avoid_losing_coordinates(board, usr):
    if usr == 'O':
        opponent = 'X'
    else:
        opponent = 'O'
    if winning_coordinates(board, opponent):
        return winning_coordinates(board, opponent)
    return None


# returns coordinates from AI lvl medium
def get_computer_coordinates_medium(board, usr):
    if winning_coordinates(board, usr):
        return winning_coordinates(board, usr)
    elif avoid_losing_coordinates(board, usr):
        return avoid_losing_coordinates(board, usr)
    else:
        return get_computer_coordinates_easy(board)


# returns coordinates from AI lvl hard
def get_computer_coordinates_hard(board, usr, aiPlayer):
    if winning_coordinates(board, usr):
        return winning_coordinates(board, usr)
    elif avoid_losing_coordinates(board, usr):
        return avoid_losing_coordinates(board, usr)
    else:
        min_max_board = get_min_max_board(board)
        print(min_max_board)
        best_move = minmax(min_max_board, usr, aiPlayer)
        print(best_move)
        if best_move == 0:
            return [0, 0]
        elif best_move == 1:
            return [0, 1]
        elif best_move == 2:
            return [0, 2]
        elif best_move == 3:
            return [1, 0]
        elif best_move == 4:
            return [1, 1]
        elif best_move == 5:
            return [1, 2]
        elif best_move == 6:
            return [2, 0]
        elif best_move == 7:
            return [2, 1]
        elif best_move == 8:
            return [2, 2]




# makes user move
def user_move(board):
    x, y = read_coordinates(board)
    usr = user(board)
    update_board(board, usr, [x, y])


# makes computer move
def computer_move(board, level):
    usr = user(board)
    if level == 'easy':
        print("Making move level \"easy\"")
        move = get_computer_coordinates_easy(board)
    if level == 'medium':
        print("Making move level \"medium\"")
        move = get_computer_coordinates_medium(board, usr)
    if level == 'hard':
        print("Making move level \"hard\"")
        move = get_computer_coordinates_hard(board, usr, usr)
        print(move)
    update_board(board, usr, [move[0], move[1]])


def play_user_vs_computer(who_got_x, who_got_o):
    board = clean_board()
    print_board(board)
    while True:
        if who_got_x == 'user':
            level = who_got_o
            user_move(board)
            print_board(board)
            if check_end_of_game(board):
                return False
            computer_move(board, level)
            print_board(board)
            if check_end_of_game(board):
                return False
        else:
            level = who_got_x
            computer_move(board, level)
            print_board(board)
            if check_end_of_game(board):
                return False
            user_move(board)
            print_board(board)
            if check_end_of_game(board):
                return False


def play_user_vs_user():
    board = clean_board()
    print_board(board)
    while True:
        user_move(board)
        print_board(board)
        if check_end_of_game(board):
            return False


def play_computer_vs_computer(who_plays_x, who_plays_o):
    board = clean_board()
    print_board(board)
    while True:
        computer_move(board, who_plays_x)
        print_board(board)
        if check_end_of_game(board):
            return False
        computer_move(board, who_plays_o)
        print_board(board)
        if check_end_of_game(board):
            return False


try:
    select, who_plays_x, who_plays_o = input().split(" ")
except BaseException:
    print("Bad parameters!")
while True:
    if select == 'start':
        if who_plays_o and who_plays_x:
            if who_plays_o == 'user' and who_plays_x == 'user':
                if not play_user_vs_user():
                    break
            elif who_plays_o != 'user' and who_plays_x != 'user':
                if not play_computer_vs_computer(who_plays_x, who_plays_o):
                    break
            elif who_plays_o != 'user':
                if not play_user_vs_computer('user', who_plays_o):
                    break
            elif who_plays_x != 'user':
                if not play_user_vs_computer(who_plays_x, 'user'):
                    break
        else:
            print("Bad parameters!")
    elif select == "exit":
        break
