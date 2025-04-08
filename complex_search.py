"" "This is python implementation of 8-queens "
"problem using hill-climbing algorithm" ""

from utility.node import Node
from utility.problem import ComplexProblem
import argparse


def main():
    parser = argparse.ArgumentParser(description="8-Queens Problem Solver")
    parser.add_argument(
        "algorithm", type=str, default="hill_climbing", help="The algorithm choices"
    )
    parser.add_argument("epoch", type=int, default=10, help="The number of rolling")
    args = parser.parse_args()

    queen_1 = Node("Q1", 0, 3)
    queen_2 = Node("Q2", 1, 2)
    queen_3 = Node("Q3", 2, 1)
    queen_4 = Node("Q4", 3, 4)
    queen_5 = Node("Q5", 4, 3)
    queen_6 = Node("Q6", 5, 2)
    queen_7 = Node("Q7", 6, 1)
    queen_8 = Node("Q8", 7, 2)

    # queen_1 = Node("Q1", 0, 3)
    # queen_2 = Node("Q2", 1, 6)
    # queen_3 = Node("Q3", 2, 5)
    # queen_4 = Node("Q4", 3, 6)
    # queen_5 = Node("Q5", 4, 4)
    # queen_6 = Node("Q6", 5, 4)
    # queen_7 = Node("Q7", 6, 0)
    # queen_8 = Node("Q8", 7, 7)

    queen_group = [
        queen_1,
        queen_2,
        queen_3,
        queen_4,
        queen_5,
        queen_6,
        queen_7,
        queen_8,
    ]
    queen_problem = ComplexProblem(max_x=7, max_y=7)

    if args.algorithm == "hill_climbing":
        solution_state, value = queen_problem.hill_cimbing(queen_group, args.epoch)
        for c in solution_state:
            print(f"nama: {c.get_name()}, posX: {c.get_posX()}, posY: {c.get_posY()}")
        print(f"value dari state paling optimal adalah: {value}")

    elif args.algorithm == "genetic":
        queen_problem.genetic_algorithm(args.epoch, population_size=5)


if __name__ == "__main__":
    main()
