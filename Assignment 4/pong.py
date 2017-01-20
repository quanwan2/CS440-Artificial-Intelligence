import numpy as np
import math
import sys
import random
################################################
# Constant in alpha
C = 100
# Discount Factor
gamma = 0.8
# Storing all Q(s,a) values
Q_values = {}
# Storing the number of times seeing (s,a)
N = {}
# Possible actions for paddle
actions = [0., +0.04, -0.04]
# Paddle length
paddle_height = 0.2
###############################################
def discretization_map( (x,y,v_x,v_y,paddle_y) ):
    tmp1 = min(np.floor(12*x),11)
    tmp2 = min(np.floor(12*y),11)
    ###
    if v_x > 0:
        tmp3 = 1
    else:
        tmp3 = -1
    ###
    if v_y > 0.015:
        tmp4 = 1
    elif v_y < -0.015:
        tmp4 = -1
    else:
        tmp4 = 0
    ###
    tmp5 = min(np.floor(12*paddle_y)/(1-paddle_height),11)
    # Return the corresponding discrete state
    return (tmp1,tmp2,tmp3,tmp4,tmp5)

# Initialization
def init():
    N = {}
    Q_values = {}

# Calculate the intersection coordinate
def get_intersection(x1,y1,x2,y2):
    return (y1-y2)/(x1-x2) * (1-x1) + y1

# Discretize the action of paddle
def discretization(action):
    if action == 0.04:
        return 1
    elif action == 0:
        return 0
    else:
        return -1

# Given a state, get the best possible action
def get_best_action(state):
    if state is None:
        raise Exception("Error -- None State")
    best_action = None
    max_Q = -sys.maxint
    for action in actions:
        key = ( discretization_map(state), action )
        if key not in N or N[key] < 10 or key not in Q_values:
            best_action = action
            return best_action
        if Q_values[key] > max_Q:
            max_Q = Q_values[key]
            best_action = action
    return best_action

# Given a state and action, get the next state and reward
def get_next_state(curr_state, best_action):
    if curr_state is None:
        raise Exception("Error -- None State")
    next_state = None
    (b_x,b_y,v_x,v_y,p_y) = curr_state
    reward = 0.
    # best_action = get_best_action( discretization_map(curr_state) )
    p_y += best_action
    if p_y < 0.:
        p_y = 0.
    if p_y > 0.8:
        p_y = 0.8
    b_x += v_x
    b_y += v_y
    if b_x < 0.:
        b_x = -b_x
        v_x = -v_x
    if b_y < 0.:
        b_y = -b_y
        v_y = -v_y
    if b_y > 1.:
        b_y = 2.-b_y
        v_y = -v_y
    if b_x > 1.0:
        intersection = get_intersection( curr_state[0], curr_state[1], b_x, b_y )
        if intersection <= p_y+paddle_height and intersection >= p_y:
            reward = 1.0
            b_x = 2. - b_x
            flag = True
            # Guarantee that abs(v_x) is larger than 0.03
            while flag:
                U = random.uniform(-0.015, 0.015)
                V = random.uniform(-0.03, 0.03)
                tmp_x = -v_x + U
                tmp_y = v_y + V
                if abs(tmp_x) <= 0.03:
                    flag = True
                else:
                    flag = False
            v_x = tmp_x
            v_y = tmp_y
        else:
            return (None, -1.0)
    # It seems that no wierd thing happens here
    if abs(v_y) > 1 or abs(v_x) > 1:
        print "Rare Circumstances"
    next_state = (b_x, b_y, v_x, v_y, p_y)
    return (next_state, reward)

def get_Q(state):
    if state is None:
        return -1.0
    max_Q = -sys.maxint
    for action in actions:
        key = ( discretization_map(state), action )
        if key not in Q_values:
            Q = 0.
        else:
            Q = Q_values[key]
        max_Q = max(max_Q, Q)
    return max_Q

def QLearning():
    init()
    bounce = 0
    count = 0
    while count < 100000:
        if count%1000 == 0:
            print count
            if count > 0:
                print bounce/1000.0
                bounce = 0
        current_state = (0.5,0.5,0.03,0.01,0.4)
        reward = 0.0
        flag = True
        while flag:
            best_action = get_best_action(current_state)
            key = ( discretization_map(current_state), best_action )
            current_state, reward = get_next_state(current_state, best_action)
            if current_state is None:
                flag = False
            if key not in N:
                N[key] = 1
                alpha = 1.0
                Q_values[key] = alpha*( reward+gamma*get_Q(current_state) )
            else:
                N[key] += 1
                alpha = 1.0*C/(C+N[key])
                Q_values[key] = Q_values[key] + alpha*( reward+gamma*get_Q(current_state) - Q_values[key] )
            if reward > 0:
            #    print "Bounce"
                bounce += 1
        count += 1
    return Q_values
################################################
def main():
    init()
    QLearning()
    # Begin testing
    i = 0
    bounce = 0
    while i < 1000:
        current_state = (0.5,0.5,0.03,0.01,0.4)
        while current_state:
            best_action = get_best_action(current_state)
            key = ( discretization_map(current_state), best_action )
            current_state, reward = get_next_state(current_state, best_action)
            if reward > 0:
                bounce += 1
        i += 1
    print "The average number of bounce is:"
    print bounce/1000.0
    print len(Q_values)
    print len(N)
################################################
main()
