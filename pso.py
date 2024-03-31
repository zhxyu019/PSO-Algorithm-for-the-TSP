import random
import math
import matplotlib.pyplot as plt

class Town:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, town):
        return math.hypot(self.x - town.x, self.y - town.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

def load_towns(size):
    towns = []
    with open(f'test_data/towns_{size}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            towns.append(Town(x, y))
    return towns

def route_cost(tour):
    return sum([town.distance(tour[index - 1]) for index, town in enumerate(tour)])

class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.best_route = route
        self.current_cost = cost if cost else self.calculate_cost()
        self.best_cost = cost if cost else self.calculate_cost()
        self.velocity = []

    def clear_velocity(self):
        self.velocity.clear()

    def update_costs_and_best(self):
        self.current_cost = self.calculate_cost()
        if self.current_cost < self.best_cost:
            self.best_route = self.route
            self.best_cost = self.current_cost

    def calculate_cost(self):
        return route_cost(self.route)


class ParticleSwarmOptimization:

    def __init__(self, iterations, population_size, global_best_probability=1.0, personal_best_probability=1.0, towns=None):
        self.towns = towns
        self.global_best = None
        self.best_cost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.global_best_probability = global_best_probability
        self.personal_best_probability = personal_best_probability

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    def random_route(self):
        return random.sample(self.towns, len(self.towns))

    def initial_population(self):
        random_population = [self.random_route() for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]

    def greedy_route(self, start_index):
        unvisited = self.towns[:]
        del unvisited[start_index]
        route = [self.towns[start_index]]
        while len(unvisited):
            index, nearest_town = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_town)
            del unvisited[index]
        return route

    def run(self):
        self.global_best = min(self.particles, key=lambda p: p.best_cost)
        print(f"initial cost is {self.global_best.best_cost}")
        plt.ion()
        plt.draw()
        for t in range(self.iterations):
            self.global_best = min(self.particles, key=lambda p: p.best_cost)
            if t % 20 == 0:
                plt.figure(0)
                plt.plot(pso.best_cost_iter, 'g')
                plt.ylabel('Distance')
                plt.xlabel('Generation')
                fig = plt.figure(0)
                fig.suptitle('Particle Swarm Optimization Iteration')
                x_list, y_list = [], []
                for town in self.global_best.best_route:
                    x_list.append(town.x)
                    y_list.append(town.y)
                x_list.append(pso.global_best.best_route[0].x)
                y_list.append(pso.global_best.best_route[0].y)
                fig = plt.figure(1)
                fig.clear()
                fig.suptitle(f'Particle Swarm Optimization TSP iteration {t}')

                plt.plot(x_list, y_list, 'ro')
                plt.plot(x_list, y_list, 'g')
                plt.draw()
                plt.pause(.001)
            self.best_cost_iter.append(self.global_best.best_cost)

            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                global_best = self.global_best.best_route[:]
                new_route = particle.route[:]

                for i in range(len(self.towns)):
                    if new_route[i] != particle.best_route[i]:
                        swap = (i, particle.best_route.index(new_route[i]), self.personal_best_probability)
                        temp_velocity.append(swap)
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]

                for i in range(len(self.towns)):
                    if new_route[i] != global_best[i]:
                        swap = (i, global_best.index(new_route[i]), self.global_best_probability)
                        temp_velocity.append(swap)
                        global_best[swap[0]], global_best[swap[1]] = global_best[swap[1]], global_best[swap[0]]

                particle.velocity = temp_velocity

                for swap in temp_velocity:
                    if random.random() <= swap[2]:
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]

                particle.route = new_route
                particle.update_costs_and_best()


if __name__ == "__main__":
    towns = load_towns(16)
    pso = ParticleSwarmOptimization(iterations=100, population_size=100, personal_best_probability=0.9, global_best_probability=0.02, towns=towns)
    pso.run()
    print(f'cost: {pso.global_best.best_cost}\t| global best route: {pso.global_best.best_route}')

    x_list, y_list = [], []
    for town in pso.global_best.best_route:
        x_list.append(town.x)
        y_list.append(town.y)
    x_list.append(pso.global_best.best_route[0].x)
    y_list.append(pso.global_best.best_route[0].y)
    fig = plt.figure(1)
    fig.suptitle('Particle Swarm Optimization TSP')

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list)
    plt.show(block=True)