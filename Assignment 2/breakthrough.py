import sys
import copy
import time

######################## State For Keeping Track of Board Game (Everything) ####################################

class state:
    def __init__(self, white_positions, black_positions):
        self.white_positions = white_positions
        self.black_positions = black_positions

    # Given a position, evaluate whether it is a valid move

    # Each game, we assume that white is max strategy.
    def move_piece(self, min_or_max, index, direction):
        if min_or_max == 'max':
            # Out of Bound
            if index >= len(self.white_positions):
                return False
            elif self.white_positions[index][1] == 0: # Winner Condition
                return False
            else:
                peice_position = self.white_positions[index]
                ##### Left Dir
                if direction == 'LEFT' and peice_position[0] >= 1:
                    if ( peice_position[0]-1, peice_position[1]-1 ) in self.white_positions:
                        return False
                    self.white_positions[index] = ( self.white_positions[index][0]-1, self.white_positions[index][1]-1 )
                    # Eating Black Piece
                    if ( self.white_positions[index][0], self.white_positions[index][1] ) in self.black_positions:
                        self.black_positions.remove( (self.white_positions[index][0], self.white_positions[index][1]) )
                    return True
                ##### Right Dir
                if direction == 'RIGHT' and peice_position[0] <= 6:
                    if ( peice_position[0]+1, peice_position[1]-1 ) in self.white_positions:
                        return False
                    self.white_positions[index] = ( self.white_positions[index][0]+1, self.white_positions[index][1]-1 )
                    if ( self.white_positions[index][0], self.white_positions[index][1] ) in self.black_positions:
                        self.black_positions.remove( (self.white_positions[index][0], self.white_positions[index][1]) )
                    return True
                ##### Down Dir
                if direction == 'S':
                    if ( peice_position[0], peice_position[1]-1 ) in self.white_positions or ( peice_position[0], peice_position[1]-1 ) in self.black_positions:
                        return False
                    self.white_positions[index] = ( self.white_positions[index][0], self.white_positions[index][1]-1 )
                    return True
                else:
                    return False
        if min_or_max == 'min':
            # Out of Bound
            if index >= len(self.black_positions):
                return False
            elif self.black_positions[index][1] == 7:
                return False
            else:
                peice_position = self.black_positions[index]
                if direction == 'LEFT' and peice_position[0] <= 6:
                    if ( peice_position[0]+1, peice_position[1]+1 ) in self.black_positions:
                        return False
                    self.black_positions[index] = ( self.black_positions[index][0]+1, self.black_positions[index][1]+1 )
                    if ( self.black_positions[index][0], self.black_positions[index][1] ) in self.white_positions:
                        self.white_positions.remove( (self.black_positions[index][0], self.black_positions[index][1]) )
                    return True
                if direction == 'RIGHT' and peice_position[0] >= 1:
                    if ( peice_position[0]-1, peice_position[1]+1 ) in self.black_positions:
                        return False
                    self.black_positions[index] = ( self.black_positions[index][0]-1, self.black_positions[index][1]+1 )
                    if ( self.black_positions[index][0], self.black_positions[index][1] ) in self.white_positions:
                        self.white_positions.remove((self.black_positions[index][0], self.black_positions[index][1]))
                    return True
                if direction == 'S':
                    if (peice_position[0], peice_position[1]+1) in self.black_positions or (peice_position[0], peice_position[1]+1) in self.white_positions:
                        return False
                    # if (peice_position[0], peice_position[1]+1) in self.white_positions:
                    #     return False
                    self.black_positions[index] = ( self.black_positions[index][0], self.black_positions[index][1]+1 )
                    return True
                else:
                    return False

######################## Heuristic Functions For Different Strategies ####################################

##### Offensive strategy #####
def evaluate_offensive(state):

    w1, w2, white_to_border, white_pieces_captured = 1, 2, 7, 0
    white_captured_positions = set()
    w3, w4, black_to_border, black_pieces_captured = 1, 2, 7, 0
    black_captured_positions = set()

    for white_piece in state.white_positions:
        if white_piece[1] < white_to_border:
            white_to_border = white_piece[1]
        if (white_piece[0] - 1) >= 0 and (white_piece[1] - 1) >= 0:
            white_captured_positions.add((white_piece[0] - 1, white_piece[1] - 1))
        if (white_piece[0] + 1) <= 7 and (white_piece[1] - 1) >= 0:
            white_captured_positions.add((white_piece[0] + 1, white_piece[1] - 1))
    for pos in white_captured_positions:
        if pos in state.black_positions:
            white_pieces_captured += 1

    for black_piece in state.black_positions:
        if ( 7 - black_piece[1] ) < black_to_border:
            black_to_border = 7 - black_piece[1]
        if (black_piece[0] - 1) >= 0 and (black_piece[1] + 1) <= 7:
            black_captured_positions.add((black_piece[0] - 1, black_piece[1] + 1))
        if (black_piece[0] + 1) <= 7 and (black_piece[1] + 1) <= 7:
            black_captured_positions.add((black_piece[0] + 1, black_piece[1] + 1))
    for pos in black_captured_positions:
        if pos in state.white_positions:
            black_pieces_captured += 1

    # As said above, we always want to maximize white score, minimize black score.
    score1 = 1.0 * w1 * ( 7-white_to_border ) + 1.0 * w2 * white_pieces_captured
    score2 = 1.0 * w3 * ( 7-black_to_border ) + 1.0 * w4 * black_pieces_captured
    return (score1 - score2)


##### Defensive strategy #####
def evaluate_defensive(state):

    # Here our goal becomes to set more blocks to black as well as the black to white distance. i.e. prevent them from coming to white border
    w1, w2, white_black_blocks, white_black_distance = 1, 1, 0, 7
    w3, w4, black_white_blocks, black_white_distance = 1, 1, 0, 7
    #####
    for white_piece in state.white_positions:
        if ( white_piece[1] - 1 ) >= 0 and (white_piece[0], white_piece[1] - 1) in state.black_positions:
            white_black_blocks += 1
        if white_piece[1] < white_black_distance:
            white_black_distance = white_piece[1]
    for black_piece in state.black_positions:
        if ( black_piece[1] + 1 ) <= 7 and (black_piece[0], black_piece[1] + 1) in state.white_positions:
            black_white_blocks += 1
        if ( 7 - black_piece[1] ) < black_white_distance:
            black_white_distance = 7 - black_piece[1]

    #####
    score1 = 1.0 * w1 * black_white_distance + 2.0 * w2 * white_black_blocks
    score2 = 1.0 * w3 * white_black_distance + 1.0 * w4 * black_white_blocks
    return (score1 - score2)
######################## TreeNode Structure of Game Tree ####################################
class treeNode:
    def __init__(self, min_or_max):
        self.min_or_max = min_or_max
######################## More Helper Functions ####################################

##### Change Strategy #####
def change_strategy(strategy):
    if strategy == 'O':
        return 'D'
    else:
        return 'O'
#####
##### End of Game
def is_winning_case(node, state):
    if len(state.white_positions) == 0 or len(state.black_positions) == 0:
        return True
    for white_piece in state.white_positions:
        if white_piece[1] == 0:
            return True
    for black_piece in state.black_positions:
        if black_piece[1] == 7:
            return True
    return False

#####
##### Print the board #####
def print_state(state):
    mat = [ [' ' for i in range(8)] for j in range(8) ]
    for white_piece in state.white_positions:
        mat[white_piece[1]][white_piece[0]] = 'W'
    for black_piece in state.black_positions:
        mat[black_piece[1]][black_piece[0]] = 'B'

    for row in mat:
        print ' =================================='
        line = ''
        for character in row:
            line += ( ' | ' + character)
        print line, ' | '
    print ' =================================='

######################## Minimax Search --- As on the lecture note ####################################
def minimax_search(node, state, depth, strategy, count, flag):
    if depth == 0 or is_winning_case(node, state):
        if strategy == 'O':
            return evaluate_offensive(state), None, None, count
        elif strategy == 'D':
            return evaluate_defensive(state), None, None, count
    # MAX ROUND
    if node.min_or_max == 'max':
        H = -sys.maxint
        next_node = None
        next_state = None
        for index in range(16):
            for direction in ['LEFT', 'RIGHT', 'S']:
                # Deepcopy is needed here
                current_state = copy.deepcopy(state)
                if current_state.move_piece('max', index, direction):
                    tmp_state = copy.deepcopy(current_state)
                    child = treeNode('min')
                    if flag:
                        current_strategy = change_strategy(strategy)
                    else:
                        current_strategy = strategy
                    (current_h, c, s, count) = minimax_search( child, current_state, depth-1, current_strategy, count+1, flag )
                    # node.children.append(child)
                    if current_h > H:
                        H = current_h
                        next_node = child
                        next_state = copy.deepcopy(tmp_state)
    # MIN ROUND
    if node.min_or_max == 'min':
        H = sys.maxint
        next_node = None
        next_state = None
        for index in range(16):
            for direction in ['LEFT', 'RIGHT', 'S']:
                current_state = copy.deepcopy(state)
                if current_state.move_piece('min', index, direction):
                    tmp_state = copy.deepcopy(current_state)
                    child = treeNode('max')
                    if flag:
                        current_strategy = change_strategy(strategy)
                    else:
                        current_strategy = strategy
                    (current_h, c, s, count) = minimax_search( child, current_state, depth-1, current_strategy, count+1, flag )
                    if current_h < H:
                        H = current_h
                        next_node = child
                        next_state = copy.deepcopy(tmp_state)
    return (H, next_node, next_state, count)

######################## Alpha-beta Search --- As on the lecture note ####################################

def alpha_beta_search(node, state, minTuple, maxTuple, depth, strategy, count, flag):

    if depth == 0 or is_winning_case(node, state):
        if strategy == 'O':
            return evaluate_offensive(state), None, None, count
        elif strategy == 'D':
            return evaluate_defensive(state), None, None, count
    if node.min_or_max == 'max':
        H, next_node, next_state = minTuple
        # Map each h value to lots of move
        Hdict = {}
        for index in range(16):
            for direction in ['LEFT', 'RIGHT', 'S']:
                current_state = copy.deepcopy(state)
                if current_state.move_piece('max', index, direction):
                    child = treeNode('min')
                    if flag:
                        current_strategy = change_strategy(strategy)
                    else:
                        current_strategy = strategy

                    if current_strategy == 'O':
                        heursitic = (evaluate_offensive(current_state))
                    else:
                        heursitic = (evaluate_defensive(current_state))

                    if -heursitic in Hdict:
                        Hdict[-heursitic].append( (child, current_state, current_strategy) )
                    else:
                        Hdict[-heursitic] = [(child, current_state, current_strategy)]
        # We can end up earlier than simple minimax search.
        for heursitic in sorted( Hdict.keys() ):
            for move in Hdict[heursitic]:
                tmp_state = copy.deepcopy(move[1])
                (current_h, c, s, count) = alpha_beta_search(move[0], move[1], (H, next_node, next_state), maxTuple, depth-1, move[2], count+1, flag)
                if current_h > H:
                    H = current_h
                    next_node = move[0]
                    next_state = tmp_state
                if H >= maxTuple[0]:
                    return (maxTuple[0], maxTuple[1], maxTuple[2], count)
    # Symmetric Part
    if node.min_or_max == 'min':
        H, next_node, next_state = maxTuple
        Hdict = {}
        for index in range(16):
            for direction in ['LEFT', 'RIGHT', 'S']:
                current_state = copy.deepcopy(state)
                if current_state.move_piece('min', index, direction):
                    tmp_state = copy.deepcopy(current_state)
                    child = treeNode('max')
                    if flag:
                        current_strategy = change_strategy(strategy)
                    else:
                        current_strategy = strategy
                    if current_strategy == 'O':
                        heursitic = ( evaluate_offensive(current_state) )
                    elif current_strategy == 'D':
                        heursitic = (evaluate_defensive(current_state))
                    if heursitic in Hdict:
                        Hdict[heursitic].append( (child, current_state, current_strategy) )
                    else:
                        Hdict[heursitic] = [ (child, current_state, current_strategy) ]
        # End up earlier.
        for heursitic in sorted(Hdict.keys()):
            for move in Hdict[heursitic]:
                tmp_state = copy.deepcopy(move[1])
                (current_h, c, s, count) = alpha_beta_search(move[0], move[1], minTuple, (H, next_node, next_state), depth-1, move[2], count+1, flag)
                if current_h < H:
                    H = current_h
                    next_node = move[0]
                    next_state = copy.deepcopy(tmp_state)
                if H <= minTuple[0]:
                    return (minTuple[0], minTuple[1], minTuple[2], count)
    return (H, next_node, next_state, count)


########################## Main Function ################################
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ('Please use: python breakThrough.py  (A, B, C, D)  (1, 2, 3, or 4)')
        exit(1)

    # Assume white uses max strategy
    root = treeNode('max')
    matchup = sys.argv[1]
    agent_type = int(sys.argv[2])

    types = {}
    types[1] = 'Offensive VS Defensive: Offensive First'
    types[2] = 'Offensive VS Defensive: Defensive First'
    types[3] = 'Offensive VS Offensive'
    types[4] = 'Defensive VS Defensive'
    print '\n'
    print '========================================================'
    print matchup, types[agent_type]
    print '========================================================'
    if agent_type in [1, 3]:
        start_strategy = 'O'
    else:
        start_strategy = 'D'

    depth1 = 3 # minimax depth
    depth2 = 5 # alpha-beta depth

    minTuple = (-sys.maxint, None, None)
    maxTuple = (sys.maxint, None, None)

    w, height = 8, 8
    white_positions, black_positions = [], []
    for i in range(w):
        for j in range(2):
            white_positions.append( (i, height-1-j) )
    for i in range(w):
        for j in range(2):
            black_positions.append( (i, j) )
    start_state = state(white_positions, black_positions)

    current_node, current_state, current_strategy = root, start_state, start_strategy
    turn = 1
    count_max, count_min = 0, 0
    t_max, t_min = 0, 0
    if agent_type <= 2:
        flag = True
    else:
        flag = False

    while current_node is not None:
        prev_agent, prev_state = current_node.min_or_max, current_state
        start_time = time.time()
        if (matchup == 'A') or (matchup == 'C' and turn%2 == 1) or (matchup == 'D' and turn%2 == 0):
            (u, current_node, current_state, count) = minimax_search(current_node, current_state, depth1, current_strategy, 0, flag)
            player = 'Minimax'
        else:
            (u, current_node, current_state, count) = alpha_beta_search(current_node, current_state, minTuple, maxTuple, depth2, current_strategy, 0, flag)
            player = 'Alpha-beta'
        time_elapsed = time.time() - start_time

        ##### Statistics #####
        if ( turn%2 == 0 ):
            count_min += count
            t_min += time_elapsed
        else:
            count_max += count
            t_max += time_elapsed


        if current_node is not None:
            turn += 1
            """
            print 'Agent is: ' + player
            print 'Strategy: ', current_strategy, ' Number of nodes explored: ', count
            print 'min_or_max: ', prev_agent
            print_state(current_state)
            """

        if flag:
            current_strategy = change_strategy(current_strategy)

    winner = 'Black'
    if prev_agent == 'min':
        winner = 'White'

    ### Game is over.
    print '============================================='
    print 'Game Results'
    print_state(prev_state)
    print '*********************************************'
    print 'Winner:{}'.format(winner)
    print 'Total number of moves: ', turn
    print '*********************************************'
    print 'Number of pieces captured by White: ', 16 - len(prev_state.black_positions), 'Number of pieces captured by Black: ', 16 - len(prev_state.white_positions)
    print 'Number of nodes expanded by White -> total: ', count_max, ' average: ', count_max/((turn+1)/2), 'average time taken by White: ', t_max*1.0/((turn+1)/2)
    print 'Number of nodes expanded by Black -> total: ', count_min, ' average: ', count_min/((turn)/2), 'average time taken by Black: ', t_min*1.0/((turn)/2)
    print '============================================='
