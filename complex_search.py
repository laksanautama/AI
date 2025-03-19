""'This is python implementation of 8-queens '
'problem using hill-climbing algorithm'""

from collections import deque
import math

class ComplexProblem():
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
    
    def get_maxX(self):
        return self.max_x
    
    def get_maxY(self):
        return self.max_y
    
    #function for getting total number of queens horizontally
    def horizontal_search(self, q, queen_group, reached):
        sum = 0
        hc = 0

        for x in queen_group:
            if q != x:
                if x.get_posY() == q.get_posY():
                    sum+=1
                    reached.append(x)
        if sum >= 2:
            sum+=1
            hc = (math.factorial(sum))/(math.factorial(2))*math.factorial(sum-2)
        
        elif sum == 1:
            hc = 1

        else:
            hc = sum

        return hc, reached

    #function for getting total number of queens diagonally
    def diagonal_search(self, q, queen_group, reached):
        sum_pos = 0
        sum_neg = 0
        dc = 0

        for x in queen_group:
            if q!= x:
                m = (x.get_posY()-q.get_posY())/(x.get_posX()-q.get_posX())
                if(m == 1):
                    sum_pos+=1
                    reached.append(x)
                elif(m == -1):
                    sum_neg+=1
                    reached.append(x)

        if sum_pos >= 2:
            sum_pos+=1
            dc+= (math.factorial(sum_pos))/(math.factorial(2))*math.factorial(sum_pos-2)
        
        elif sum_pos == 1:
            dc+= 1    
        else:
            dc+= sum_pos

        if sum_neg >= 2:
            sum_neg+=1
            dc+= (math.factorial(sum_neg))/(math.factorial(2))*math.factorial(sum_neg-2)
        elif sum_neg == 1:
            dc+=1
        else:
            dc+= sum_neg

        return dc, reached

    #function for getting the total number of 
    # confronted queens in horizontal & diagonal direction
    def valuation(self, queen_group):
        reached = deque()
        sum = 0
        
        for q in queen_group:
            print(f"queen saat ini: {q.get_name()}")

            if q not in reached:
                dc, reached = self.diagonal_search(q, queen_group, reached)
                hc, reached = self.horizontal_search(q, queen_group, reached)
                print(f"diagonal cost saat ini: {dc}")
                print(f"horizontal cost saat ini: {hc}")
                sum = sum + dc + hc

            print(f"sum saat ini: {sum}")

        return sum

    #function for getting the highest neighbour state 
    #value by moving single queen in its column
    def moving_state(self, queen_group):
        h = math.inf
        state_candidate = None

        for q in queen_group:
            orig_posY = q.get_posY()

            for i in range(7):
                q.set_posY(q.get_posY()+1)
                value = valuation(queen_group)

                if value <= h:
                    h = value
                    state_candidate = queen_group
                
                if q.get_posY() == self.get_maxY():
                    q.set_posY(orig_posY)

        return state_candidate
    
    #Hill-Climbing Algorithm
    def hill_cimbing(self, queen_group):
        p = True

        while p:
            current_value = self.valuation(queen_group)
            queen_group, value = self.moving_state(queen_group)
        
        
        pass 
    

class Queen():
    def __init__(self, name, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
    
    def set_posX(self, x):
        self.pos_x = x

    def set_posY(self, y):
        self.pos_y = y

    def get_posX(self):
        return self.pos_x

    def get_posY(self):
        return self.pos_y
    
    def get_name(self):
        return self.name
    
#====== DUMMY FUNC==========#

def main():
    queen_1 = Queen("Q1", 0, 3)
    queen_2 = Queen("Q2", 1, 2)
    queen_3 = Queen("Q3", 2, 1)
    queen_4 = Queen("Q4", 3, 4)
    queen_5 = Queen("Q5", 4, 3)
    queen_6 = Queen("Q6", 5, 2)
    queen_7 = Queen("Q7", 6, 1)
    queen_8 = Queen("Q8", 7, 2)


    queen_group = [queen_1, queen_2, queen_3, queen_4, queen_5, 
                   queen_6, queen_7, queen_8]
    queen_problem = ComplexProblem(max_x=7, max_y=7)

    solution = queen_problem.moving_state(queen_group)
    # grp = moving_state(queen_group)
    for c in solution:
        print(f"nama: {c.get_name()}, posX: {c.get_posX()}, posY: {c.get_posY()}")
    

    # cost = valuation(queen_group)
    # print(f"best cost: {cost}")

if __name__ == "__main__":
    main()
     