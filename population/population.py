import random
from individual import Individual


class Population(list):
    def __init__(self, constants):
        super().__init__()
        self._constants = constants

    @classmethod
    def create_population(cls, constants):
        population = cls(constants)
        population.extend(
            [Individual(constants) for _ in range(constants.POPULATION_SIZE)]
        )
        return population

    def get_fitness_values(self):
        return [ind.fitness for ind in self]

    def tournament(self):
        offspring = Population(self._constants)
        population_len = len(self)
        for _ in range(population_len):
            i1, i2, i3 = random.sample(range(population_len), 3)
            best_individual = max(
                [self[i1], self[i2], self[i3]], key=lambda ind: ind.fitness
            )
            offspring.append(best_individual.clone())
        return offspring

    def crossing(self):
        for child1, child2 in zip(self[::2], self[1::2]):
            if random.random() < self._constants.P_CROSSOVER:
                self._one_point_crossing(child1, child2)

    @staticmethod
    def _one_point_crossing(child_1: Individual, child_2: Individual):
        s = random.randint(2, len(child_1.gens) - 3)
        child_1.gens[s:], child_2.gens[s:] = child_2.gens[s:], child_1.gens[s:]

    def mutation(self):
        for mutant in self:
            if random.random() < self._constants.P_MUTATION:
                self._mut_flip_bit(mutant)

    @staticmethod
    def _mut_flip_bit(mutant, indpb=0.01):
        for index, gen in enumerate(mutant.gens):
            if random.random() < indpb:
                mutant.gens[index] = 0 if mutant.gens[index] == 1 else 1
