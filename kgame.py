import random

# This is the title of the game
KGAME_TITLE = "The K-Game (Python Edition)"

# This is the file name of the saved game state
KGAME_SAVE_FILE = "kgame.sav"

# Number of tiles per side
KGAME_SIDES = 4

# Output buffer size in bytess
KGAME_OUTPUT_BUFLEN = ((18*40)+1)

# Arrow keys
dirs = { 'UP': 1, 'DOWN': 2, 'LEFT': 3, 'RIGHT': 4 }

# Keys accepted by game
inputs = { 'LOAD': 5, 'SAVE': 6, 'EXIT': 7}


def kgame_init(game):
    game['score'] = 0
    game['board'] = [[' ' for x in range(KGAME_SIDES)] for y in range(KGAME_SIDES)]


def kgame_add_random_tile(game):
    # goes through each tile and counts it until full to stop infinite loop
    count = 0;
    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):
            if game['board'][i][j] != ' ':
           	 count += 1

    if count == 16: return

    while True:
        row = random.randint(0, KGAME_SIDES-1) # make sure that its inside the board
        col = random.randint(0, KGAME_SIDES-1)
        if game['board'][row][col] == ' ':
            break

    # place to the random position 'A' or 'B' tile
    game['board'][row][col] = 'A'
    if random.randint(0, 2) == 1:
        game['board'][row][col] = 'B'


def kgame_render(game):
 # prints top of board
   output_buffer = ""
   for i in range(0, KGAME_SIDES):
       output_buffer += "+"
       output_buffer += "-"
   output_buffer += "+\n"

#prints the middle of the board
   for i in range(0, KGAME_SIDES):
       for j in range(0, KGAME_SIDES):
           output_buffer += "|"
           output_buffer += game['board'][i][j] # gets the char and location of it
       output_buffer += "|\n"
 # prints the bottom half of the board
       for j in range(0, KGAME_SIDES):
           output_buffer += "+-"
       output_buffer += "+\n"

#prints the score
   output_buffer += "\n"
   output_buffer += "Score: " + str(game['score']) + "\n"

   return output_buffer




def kgame_is_won(game):
# checks if the game is won by checking if there is a 'K' value on the board
    for i in range(0, KGAME_SIDES):
        for j in range(0,KGAME_SIDES):
            if game['board'][i][j] == 'K':
                return True

    return False;



def kgame_is_move_possible(game):

    for i in range(0, KGAME_SIDES):
        for j in range(0, KGAME_SIDES):

            # checks vertical and horizonal if board is full
            if j < 3:
                if game['board'][i][j] == game['board'][i][j + 1] and game['board'][i][j] != ' ':
                    return True

            if i < 3:
                if game['board'][i][j] == game['board'][i + 1][j] and game['board'][i][j] != ' ':
                    return True

            if game['board'][i][j] == ' ':
                return True

    return False


#rotates the board so that you can just turn and move instead of going through each iteration
def kgame_rotate(game):
    temp = [[' ' for x in range(KGAME_SIDES)] for y in range(KGAME_SIDES)]
    for i in range(KGAME_SIDES):
        for j in range(KGAME_SIDES):
            temp[i][j] = game['board'][i][j] #creates and temp board and set to current board

    for x in range(KGAME_SIDES):
        for z in range(KGAME_SIDES):
            game['board'][x][z] = temp[KGAME_SIDES - 1 - z][x] #rotates board clockwise


#movement of the pieces from shifting to merging
def kgame_movement(game):

#shifts the board right
        for i in range(KGAME_SIDES):
            for j in range(KGAME_SIDES-1):
                for b in range(KGAME_SIDES-1):
                    if game['board'][i][b + 1] == ' ': #checks if empty spaces and shifts it
                        temp = game['board'][i][b+1]
                        game['board'][i][b+1] = game['board'][i][b]
                        game['board'][i][b] = temp


#merges the pieces

        for x in range(KGAME_SIDES):
            for y in range(KGAME_SIDES-1, 0, -1):
                #checks if two pieces are can be merged
                if(game['board'][x][y-1] == game['board'][x][y] and game['board'][x][y] != ' ' and game['board'][x][y]!= ' '):
                    game['board'][x][y] = chr(ord(game['board'][x][y])+1) #gets next character
                    game['score'] += kgame_getScore(chr(ord(game['board'][x][y]))) # gets score
                    game['board'][x][y-1] = ' ' # makes  previous space empty after merging

#shifts the board to right again so that non-empty spaces can be moved into spaces created from merging
        for i in range(KGAME_SIDES):
            for j in range(KGAME_SIDES-1):
                for b in range(KGAME_SIDES-1):
                    if game['board'][i][b + 1] == ' ':
                        temp = game['board'][i][b+1]
                        game['board'][i][b+1] = game['board'][i][b]
                        game['board'][i][b] = temp

        kgame_add_random_tile(game) # add a new tile after every move


#updates game
def kgame_update(game, direction):
    #rotation is set to right so simply get it to move
    if(direction == dirs['RIGHT']):
        kgame_movement(game)
        return True
    #rotates twice so right -> left = 2 rotations
    if(direction == dirs['LEFT']):
        kgame_rotate(game)
        kgame_rotate(game)
        kgame_movement(game)
        kgame_rotate(game)
        kgame_rotate(game)
        return True
    #rotates till UP from right
    if(direction == dirs['UP']):
        kgame_rotate(game)
        kgame_movement(game)
        kgame_rotate(game)
        kgame_rotate(game)
        kgame_rotate(game)
        return True
    #rotates till DOWN from right
    if(direction == dirs['DOWN']):
        kgame_rotate(game)
        kgame_rotate(game)
        kgame_rotate(game)
        kgame_movement(game)
        kgame_rotate(game)
        return True

    return False

#gets score values and adds it to game score when returned
def kgame_getScore(score):
    if(score == 'A'):
        return 2;
    if(score == 'B'):
        return 4;
    if(score == 'C'):
        return 8;
    if(score == 'D'):
        return 16;
    if(score == 'E'):
        return 32;
    if(score == 'F'):
        return 64;
    if(score == 'G'):
        return 128;
    if(score == 'H'):
        return 256;
    if(score == 'I'):
        return 512;
    if(score == 'J'):
        return 1024;
    if(score == 'K'):
        return 2048;



def kgame_save(game):
    if game == None: # check if game is not running
        return False
    try:
        savefile = open(KGAME_SAVE_FILE, "w")
        if savefile == None: # check if there actually is a save file
            return False
        for row in range(KGAME_SIDES):
            for col in range(KGAME_SIDES):
                savefile.write(game['board'][row][col]) # goes through and writes to the file

        savefile.write(str(game['score'])) #writes score
        savefile.close()
        return True
    except: 'something went wrong'


def kgame_load(game):
    count = 0;

    if game == None: # check that game is not running
        return False

    loadfile = open(KGAME_SAVE_FILE, "r")
    if loadfile == None: # check if there actually is a save file
        return False
    filereader = loadfile.read(); # read the file


    for i in range(KGAME_SIDES):
        for j in range(KGAME_SIDES):

            game['board'][i][j] = str(filereader[count]) # gets file format
            count += 1

    game['score'] = int(filereader[count:]) # reads until the end

    loadfile.close()
    return True
