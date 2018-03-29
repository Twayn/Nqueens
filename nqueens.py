import random

# A program for solving eight queens problem using genetic algorithm
# Parameters:
# pos_size - size of initial population
# cross_prob - probability of crossing
# mut_prob - probability of mutation
# min_fitnes - minimum value of fitness function
# If in the population there is an element with the value of the fitness function is less
# than min_fitnes script stops.
# IMPORTANT: The element with minimum fitness function value is the fittest element
# max_epochs - the number of iterations of genetic algorithm
#
# Return values:
# 1)The number of itearations until an element with a fitness function value less than the min_fitnes is found
# or max_epochs if not found
# 2)The minimum value of fitness function
# 3) The element with the minimum value of fitness function

class Solver_8_queens:
    queen_cell = "Q"
    empty_cell = "+"
    length = 8
    result = None
    cells_number = length * length
    one = 1
    zero = 0

    def __init__(self, pop_size=500, cross_prob=0.20, mut_prob=0.05):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness=2, max_epochs=100):
        population = self.create_initial_population()

        for i in range(max_epochs):
            print("iteration: {}".format(i))
            if self.check_exit_condition(population, min_fitness):
                return i, fitness_value(self.result), self.board_to_string(board_value(self.result))

            population = self.selection_by_roulette_method(population)
            population = self.cross_and_mutate(population)

        element_with_min_fitness = self.find_element_with_min_fitnes(population)
        return max_epochs, element_with_min_fitness[0], element_with_min_fitness[1]

    # return the fittest element in population and its visualization
    def find_element_with_min_fitnes(self, population):
        # Max number of issues
        min_fitnes = self.length*self.length-1
        element_with_min_fitnes = None
        for i in range(len(population)):
            element = population[i]
            if fitness_value(element) < min_fitnes:
                min_fitnes = fitness_value(element)
                element_with_min_fitnes = board_value(element)

        return min_fitnes, self.board_to_string(element_with_min_fitnes)

    def check_exit_condition(self, population, min_fitness):
        for i in range(len(population)):
            element = population[i]
            if fitness_value(element) <= min_fitness:
                self.result = element
                return True
        return False

    def cross_and_mutate(self, population):
        result_population = []
        # generate new population with the same size as original
        # by crossing random parents from old population
        while len(result_population) < self.pop_size:
            if random.uniform(self.zero, self.one) <= self.cross_prob:
                random_parents_numbers = random.sample(range(self.zero, self.pop_size), 2)
                parent0 = population[random_parents_numbers[0]]
                parent1 = population[random_parents_numbers[1]]
                childs = self.single_point_crossing(queens_value(parent0), queens_value(parent1))
                for i in range(len(childs)):
                    result_population.append(childs[i])
            else:
                rnd = random.randint(self.zero, self.pop_size-1)
                result_population.append(queens_value(population[rnd]))

        result_population = self.mutate(result_population)
        return self.envelope(result_population)

    # mutate by replacing random queen position by another
    # check that there were always 8 queens on different positions
    def mutate(self, population):
        for i in range(len(population)):
            if random.uniform(self.zero, self.one) <= self.mut_prob:
                population_element = population[i]
                self.mutate_element(population_element)
                while not is_queens_on_different_positions(population_element):
                    self.mutate_element(population_element)
        return population

    def mutate_element(self, population_element):
        mutate_position = random.randint(self.one, self.length-1)
        mutate_value = random.randint(self.zero, self.cells_number-1)
        population_element[mutate_position] = bin(mutate_value)

    def single_point_crossing(self, parent0, parent1):
        crossing_position = random.randint(self.one, self.length-1)

        child0 = []
        child1 = []

        for i in range(self.length):
            if i < crossing_position:
                child0.append(parent0[i])
                child1.append(parent1[i])
            else:
                child0.append(parent1[i])
                child1.append(parent0[i])

        # check that there were always 8 queens on different positions
        result_childs = []
        if is_queens_on_different_positions(child0):
            result_childs.append(child0)
        if is_queens_on_different_positions(child1):
            result_childs.append(child1)
        return result_childs

    def selection_by_roulette_method(self, population):
        new_population = []

        roulette_range = calc_roulette_range(population)

        for i in range(len(population)):
            rnd = random.uniform(self.zero, roulette_range)
            accumulator = 0

            for z in range(len(population)):
                element = population[z]
                accumulator = accumulator + 1 / fitness_value(element)
                if accumulator > rnd:
                    new_population.append(element)
                    break

        return new_population

    def create_initial_population(self):
        population = []
        for i in range(self.pop_size):
            population.append(self.create_arranged_board())
        return population

    # Creates visual board and count board issues for population
    def envelope(self, population):
        new_population = []
        for i in range(len(population)):
            new_population.append(self.init_queens_enviroment(population[i]))
        return new_population

    # Generate chess board with random arranged queens
    def create_arranged_board(self):
        # Random queens positions
        queens = random.sample(range(self.zero, self.cells_number), self.length)
        queens = to_binary_array(queens)
        return self.init_queens_enviroment(queens)

    # Creates visual board and count board issues
    def init_queens_enviroment(self, queens):
        board = self.create_empty_board()

        # Initialize queen positions
        for i in range(len(queens)):
            board[to_int(queens[i]) // self.length][to_int(queens[i]) % self.length] = self.queen_cell

        total_issues = self.count_board_issues(queens)
        return board, queens, total_issues

    # Count number of queens on the same directions with another queens
    # Fitness function
    def count_board_issues(self, queens):
        total_issues = 0
        for i in range(len(queens)):
            total_issues = total_issues + self.count_element_issues(to_int(queens[i]), queens)
        return total_issues

    def count_element_issues(self, element, queens):
        element_issues = 0

        x1 = element // self.length
        y1 = element % self.length

        for i in range(len(queens)):
            x2 = to_int(queens[i]) // self.length
            y2 = to_int(queens[i]) % self.length
            # Another element
            if x1 != x2 or y1 != y2:
                # Diagonal issue
                if abs(x1 - x2) == abs(y2 - y1):
                    element_issues = element_issues + 1
                # Straight issue
                if x1 == x2 or y1 == y2:
                    element_issues = element_issues + 1

        return element_issues

    def create_empty_board(self):
        n = self.length
        m = self.length
        empty_board = [[self.empty_cell] * m for i in range(n)]
        return empty_board

    def board_to_string(self, board):
        result = ""
        for i in range(self.length):
            result = result + ' '.join(board[i])
            result = result + "\n"
        return result


def calc_roulette_range(population):
    result = 0
    for i in range(len(population)):
        result = result + 1 / fitness_value(population[i])

    return result


def is_queens_on_different_positions(population_element):
    population_element_set = set(population_element)
    if len(population_element) == len(population_element_set):
        return True
    else:
        return False


def board_value(population_element):
    return population_element[0]


def queens_value(population_element):
    return population_element[1]


def fitness_value(population_element):
    return population_element[2]


def to_binary_array(array):
    result = []
    for i in range(len(array)):
        result.append(bin(array[i]))
    return result


def to_int(value):
    return int(value, 2)


if __name__ == '__main__':
    solver_8_queens = Solver_8_queens(pop_size=500, cross_prob=0.20, mut_prob=0.05)
    best_fit, epoch_num, visualization = solver_8_queens.solve(max_epochs=100, min_fitness=2)

    print("Iterations: {}".format(best_fit))
    print("Fitnes: {}".format(epoch_num))
    print(visualization)
