from collections import deque
from utility.node import Node
import math
import random
import copy


class ComplexProblem:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def get_maxX(self):
        return self.max_x

    def get_maxY(self):
        return self.max_y

    # function for getting total number of queens horizontally
    def horizontal_search(self, q, queen_group, reached):
        sum = 0
        hc = 0

        for x in queen_group:
            if q != x:
                if x.get_posY() == q.get_posY():
                    sum += 1
                    reached.append(x)
        if sum >= 2:
            sum += 1
            hc = (math.factorial(sum)) / (math.factorial(2)) * math.factorial(sum - 2)

        elif sum == 1:
            hc = 1

        else:
            hc = sum

        return hc, reached

    # function for getting total number of queens diagonally
    def diagonal_search(self, q, queen_group, reached):
        sum_pos = 0
        sum_neg = 0
        dc = 0

        for x in queen_group:
            if q != x:
                m = (x.get_posY() - q.get_posY()) / (x.get_posX() - q.get_posX())
                if m == 1:
                    sum_pos += 1
                    reached.append(x)
                elif m == -1:
                    sum_neg += 1
                    reached.append(x)

        if sum_pos >= 2:
            sum_pos += 1
            dc += (
                (math.factorial(sum_pos))
                / (math.factorial(2))
                * math.factorial(sum_pos - 2)
            )

        elif sum_pos == 1:
            dc += 1
        else:
            dc += sum_pos

        if sum_neg >= 2:
            sum_neg += 1
            dc += (
                (math.factorial(sum_neg))
                / (math.factorial(2))
                * math.factorial(sum_neg - 2)
            )
        elif sum_neg == 1:
            dc += 1
        else:
            dc += sum_neg

        return dc, reached

    # function for getting the total number of
    # confronted queens in horizontal & diagonal direction
    def valuation(self, queen_group):
        reached_h = deque()
        reached_d = deque()
        sum = 0

        for q in queen_group:
            # print(f"queen saat ini: {q.get_name()}")

            if q not in reached_d:
                dc, reached_d = self.diagonal_search(q, queen_group, reached_d)
                # print(f"diagonal cost saat ini: {dc}")
                sum = sum + dc
            if q not in reached_h:
                hc, reached_h = self.horizontal_search(q, queen_group, reached_h)
                # print(f"horizontal cost saat ini: {hc}")
                sum = sum + hc

            # print(f"jumlah queen berlawanan saat ini: {sum}")

        return sum

    # function for getting the highest neighbour state
    # value by moving single queen in its column
    def moving_state(self, queen_group, current_value):

        h = current_value
        current_group = copy.deepcopy(queen_group)
        candidate_group = None

        for q in current_group:
            for i in range(self.get_maxY()):
                value = self.valuation(current_group)
                if value < h:
                    h = value
                    candidate_group = copy.deepcopy(current_group)

                q.set_posY(q.get_posY() + 1)
                if q.get_posY() >= self.get_maxY():
                    q.set_posY(0)

        if candidate_group is None:
            return current_group, h
        else:
            return candidate_group, h

    # Hill-Climbing Algorithm
    def hill_cimbing(self, queen_group, epoch):

        current_group = queen_group
        current_value = self.valuation(current_group)

        for i in range(epoch):
            print(f"epoch ke-{i}")
            next_group, next_value = self.moving_state(current_group, current_value)

            if next_value < current_value:
                current_value = next_value
                current_group = next_group

        return current_group, current_value

    def generate_population(self, population_size):

        population = []
        w_total = 0

        for i in range(population_size):
            individual = list(range(self.get_maxY() + 1))
            random.shuffle(individual)
            queen_group = []
            for i in range(len(individual)):
                queen_i = Node("Q1", i, individual[i])
                queen_group.append(queen_i)
            sum = 1 / (self.valuation(queen_group))
            w_total += sum
            population.append((individual, sum))

        return population, w_total

    def parents_candidate(self, population, w_total, k=10):
        parents = []
        for x in population:
            y = list(x)
            y[1] = y[1] / w_total
            parents.append(tuple(y))

        indv = [item[0] for item in parents]
        weight = [item[1] for item in parents]

        random_elements = random.choices(indv, weights=weight, k=k)
        return random_elements

    def cross_over(self, parents_cand):

        half = len(parents_cand) // 2
        a_half = parents_cand[:half]
        b_half = parents_cand[half:]
        crossover = []

        for i in range(half):
            cutoff = random.randint(1, 6)
            temp = a_half[i][:cutoff]
            a_half[i][:cutoff] = b_half[i][:cutoff]
            b_half[i][:cutoff] = temp
            crossover.append(a_half[i])
            crossover.append(b_half[i])

        return crossover

    def mutation(self, crossover, mutation_rate=0.06):

        yes_no = ["yes", "no"]
        weight = [mutation_rate, 1 - mutation_rate]

        for x in crossover:
            for i in range(len(x)):
                choice = random.choices(yes_no, weights=weight, k=1)
                c = choice[0]
                # print(c)
                if c == "yes":
                    mutation = random.randint(0, 7)
                    # print(mutation)
                    x[i] = mutation

        return crossover

    def best_individu(self, mutation):

        best = 0
        best_indv = []

        for x in mutation:
            queen_group = []
            for i in range(len(x)):
                queen_i = Node("Q1", i, x[i])
                queen_group.append(queen_i)

            sum = 1 / (self.valuation(queen_group))

            if sum > best:
                best = sum
                best_indv.clear()
                for n in x:
                    best_indv.append(n)

        return best_indv, best

    def genetic_algorithm(self, epoch, population_size=5):
        parents_cand = None
        top_indv = []
        score = 0

        for i in range(epoch):
            print(f"epoch ke- {i}")
            if parents_cand is None:
                population, w_total = self.generate_population(population_size)
                parents_cand = self.parents_candidate(population, w_total)

            # print("===================")
            # print(parents_cand)
            crossover = self.cross_over(parents_cand)

            # print("+++++++++++++++")
            # print(crossover)
            mutation = self.mutation(crossover)

            # print("-------------")
            # print(mutation)

            parents_cand.clear()
            for m in mutation:
                parents_cand.append(m)

            best_indv, best = self.best_individu(mutation)

            if best > score:
                score = best
                top_indv.clear()

                for x in best_indv:
                    top_indv.append(x)
            # print("****************")
            # print(best_indv)
            # print(best)

        print(f"Individu terbaik adalah: {top_indv}, dengan skor: {score}")
