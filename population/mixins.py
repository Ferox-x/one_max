import numpy as np

from enum import Enum


class PopulationInterface(list):
    def __init__(self, constants):
        super().__init__()
        self.constants = constants

    def _create_population_with_constants(self):
        raise NotImplementedError("Переопределите метод создания пустой популяции.")


class SelectionMixin(PopulationInterface):
    class SelectionTypeChoice(Enum):
        TOURNAMENT = 1
        PROPORTIONAL = 2
        LINEAR = 3
        EXPONENTIAL = 4

    def selection(self):
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.TOURNAMENT.value:
            return self.tournament()
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.PROPORTIONAL.value:
            return self.proportional()
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.LINEAR.value:
            return self.linear_selection()
        if self.constants.SELECTION_TYPE == self.SelectionTypeChoice.EXPONENTIAL.value:
            return self.exponential_selection()
        else:
            raise NotImplementedError(
                f"Передан неопределённый тип отбора: {self.constants.SELECTION_TYPE}"
            )

    def linear_selection(self):
        sorted_population = sorted(self, key=lambda x: x.fitness, reverse=True)
        total_rank = len(self)

        probabilities = np.array(
            [
                (2.0 - (2.0 * (i - 1) / (total_rank - 1))) / total_rank
                for i in range(1, total_rank + 1)
            ]
        )

        selected_parents_indices = np.random.choice(
            total_rank, total_rank, p=probabilities
        )
        offspring = self._create_population_with_constants()
        selected_parents = [sorted_population[i] for i in selected_parents_indices]
        offspring.extend(selected_parents)
        return offspring

    def exponential_selection(self):
        sorted_population = sorted(self, key=lambda x: x.fitness, reverse=True)
        selection_pressure = 0.25
        total_rank = len(self)

        probabilities = np.array(
            [
                ((2 - selection_pressure) / total_rank)
                + (
                    2
                    * (i - 1)
                    * (selection_pressure - 1)
                    / ((total_rank - 1) * (total_rank))
                )
                for i in range(1, total_rank + 1)
            ]
        )

        selected_parents_indices = np.random.choice(
            total_rank, total_rank, p=probabilities
        )
        offspring = self._create_population_with_constants()
        selected_parents = [sorted_population[i] for i in selected_parents_indices]
        offspring.extend(selected_parents)
        return offspring

    def tournament(self):
        offspring = self._create_population_with_constants()
        population_len = len(self)
        tournament_size = self.constants.TOURNAMENT_SIZE

        for _ in range(population_len):
            members = np.random.choice(
                range(population_len), tournament_size, replace=False
            )
            best_individual = max(
                [self[_] for _ in members], key=lambda ind: ind.fitness
            )
            offspring.append(best_individual.clone())

        return offspring

    def proportional(self):
        offspring = self._create_population_with_constants()
        population_len = len(self)
        individual_chances = np.arange(len(self))

        for _ in range(population_len):
            roulette_circle = np.repeat(
                individual_chances, [ind.fitness for ind in self]
            )
            individual_index = np.random.choice(roulette_circle)
            offspring.append(self[individual_index])

        return offspring


class CrossingMixin(PopulationInterface):
    class CrossingTypeChoice(Enum):
        ONE_POINT = 1
        TWO_POINT = 2
        EQUAL = 3

    def crossing(self):
        for child1, child2 in zip(self[::2], self[1::2]):
            if np.random.random() < self.constants.P_CROSSOVER:
                if (
                    self.constants.CROSSING_TYPE
                    == self.CrossingTypeChoice.ONE_POINT.value
                ):
                    self._one_point_crossing(child1, child2)
                elif (
                    self.constants.CROSSING_TYPE
                    == self.CrossingTypeChoice.TWO_POINT.value
                ):
                    self._two_point_crossing(child1, child2)
                elif (
                    self.constants.CROSSING_TYPE == self.CrossingTypeChoice.EQUAL.value
                ):
                    self._equal_crossing(child1, child2)
                else:
                    raise NotImplementedError(
                        f"Передан неопределённый тип скрещивания: {self.constants.CROSSING_TYPE}"
                    )

    @staticmethod
    def _one_point_crossing(child_1, child_2):
        point = np.random.randint(2, len(child_1.gens) - 3)
        child_1.gens[point:], child_2.gens[point:] = (
            child_2.gens[point:],
            child_1.gens[point:],
        )

    @staticmethod
    def _two_point_crossing(child_1, child_2):
        half_len = len(child_1.gens) // 2
        point_one = np.random.randint(0, half_len)
        point_two = np.random.randint(point_one + 1, len(child_1.gens))
        child_1.gens[point_one:point_two], child_2.gens[point_one:point_two] = (
            child_2.gens[point_one:point_two],
            child_1.gens[point_one:point_two],
        )

    def _equal_crossing(self, child_1, child_2):
        for gen_index in range(self.constants.GENS_SIZE):
            if np.random.random() < self.constants.EQUAL_SELECTION_CHANCE:
                child_1.gens[gen_index], child_2.gens[gen_index] = (
                    child_2.gens[gen_index],
                    child_1.gens[gen_index],
                )


class MutationMixin(PopulationInterface):
    class PowerOfMutationChoices(Enum):
        DEFAULT = 1
        LOW = 2
        HIGH = 3

    def mutation(self):
        for mutant in self:
            if np.random.random() < self.constants.P_MUTATION:
                self._flip_bit(mutant)

    def _flip_bit(self, mutant):
        if self.constants.MUTATION_POWER == self.PowerOfMutationChoices.LOW.value:
            chance_per_gen = (
                1 / self.constants.GENS_SIZE * self.constants.LOW_MUTATION_POWER
            )
        elif self.constants.MUTATION_POWER == self.PowerOfMutationChoices.DEFAULT.value:
            chance_per_gen = 1 / self.constants.GENS_SIZE
        elif self.constants.MUTATION_POWER == self.PowerOfMutationChoices.HIGH.value:
            chance_per_gen = (
                1 * self.constants.HIGH_MUTATION_POWER / self.constants.GENS_SIZE
            )
        else:
            raise NotImplementedError(
                f"Передан неопределённый тип силы мутации: {self.constants.MUTATION_POWER}"
            )

        for index, gen in enumerate(mutant.gens):
            if np.random.random() < chance_per_gen:
                mutant.gens[index] = 0 if mutant.gens[index] == 1 else 1
