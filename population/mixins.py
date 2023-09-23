import random
import numpy as np


class PopulationInterface(list):

    def __init__(self, constants):
        super().__init__()
        self.constants = constants

    def _create_population_with_constants(self):
        raise NotImplementedError('Переопределите метод создания пустой популяции.')


class SelectionMixin(PopulationInterface):

    class SelectionTypeChoice:
        TOURNAMENT = 1
        PROPORTIONAL = 2

    def selection(self):
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.TOURNAMENT:
            return self.tournament()
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.PROPORTIONAL:
            return self.proportional()
        else:
            return self

    def tournament(self):
        offspring = self._create_population_with_constants()
        population_len = len(self)
        for _ in range(population_len):
            members = random.sample(range(population_len), self.constants.TOURNAMENT_SIZE)
            best_individual = max(
                [self[_] for _ in members], key=lambda ind: ind.fitness
            )
            offspring.append(best_individual.clone())
        return offspring

    def proportional(self):
        offspring = self._create_population_with_constants()
        population_len = len(self)
        for _ in range(population_len):
            roulette_circle = []
            for index, individual in enumerate(self):
                individual_chances = [index for _ in range(individual.fitness)]
                roulette_circle.extend(individual_chances)
            individual_index = random.choice(roulette_circle)
            offspring.append(self[individual_index])
        return offspring


class CrossingMixin(PopulationInterface):

    class CrossingTypeChoice:
        ONE_POINT = 1
        TWO_POINT = 2
        EQUAL = 3

    def crossing(self):
        for child1, child2 in zip(self[::2], self[1::2]):
            if random.random() < self.constants.P_CROSSOVER:
                if self.constants.CROSSING_TYPE == self.CrossingTypeChoice.ONE_POINT:
                    self._one_point_crossing(child1, child2)
                elif self.constants.CROSSING_TYPE == self.CrossingTypeChoice.TWO_POINT:
                    self._two_point_crossing(child1, child2)
                elif self.constants.CROSSING_TYPE == self.CrossingTypeChoice.EQUAL:
                    self._equal_crossing(child1, child2)

    @staticmethod
    def _one_point_crossing(child_1, child_2):
        point = random.randint(2, len(child_1.gens) - 3)
        child_1.gens[point:], child_2.gens[point:] = child_2.gens[point:], child_1.gens[point:]

    @staticmethod
    def _two_point_crossing(child_1, child_2):
        half_len = int(len(child_1.gens) / 2)
        point_one = random.randint(0, half_len)
        point_two = random.randint(point_one + 1, len(child_1.gens))
        child_1.gens[point_one:point_two], child_2.gens[point_one:point_two] = child_2.gens[point_one:point_two], child_1.gens[point_one:point_two]

    def _equal_crossing(self, child_1, child_2):
        for gen_index in range(self.constants.GENS_SIZE):
            if random.random() < self.constants.EQUAL_SELECTION_CHANCE:
                child_1.gens[gen_index], child_2.gens[gen_index] = child_2.gens[gen_index], child_1.gens[gen_index]


class MutationMixin(PopulationInterface):

    class PowerOfMutationChoices:
        DEFAULT = 1
        LOW = 2
        HIGH = 3

    def mutation(self):
        for mutant in self:
            if random.random() < self.constants.P_MUTATION:
                self._flip_bit(mutant)

    def _flip_bit(self, mutant):
        if self.constants.MUTATION_POWER == self.PowerOfMutationChoices.LOW:
            chance_per_gen = 1 / self.constants.GENS_SIZE * self.constants.LOW_MUTATION_POWER
        elif self.constants.MUTATION_POWER == self.PowerOfMutationChoices.DEFAULT:
            chance_per_gen = 1 / self.constants.GENS_SIZE
        elif self.constants.MUTATION_POWER == self.PowerOfMutationChoices.HIGH:
            chance_per_gen = 1 * self.constants.HIGH_MUTATION_POWER / self.constants.GENS_SIZE
        else:
            chance_per_gen = 1 / self.constants.GENS_SIZE
        for index, gen in enumerate(mutant.gens):
            if random.random() < chance_per_gen:
                mutant.gens[index] = 0 if mutant.gens[index] == 1 else 1
