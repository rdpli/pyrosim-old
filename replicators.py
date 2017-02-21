import numpy as np
from copy import deepcopy
from pyrosim import PYROSIM
from vehicles import Vehicle
from environments import Environment


class Individual(object):
    def __init__(self, idx, speed, eval_time, body_length, num_legs, development):
        self.sim = None
        self.speed = speed
        self.eval_time = eval_time
        self.body_length = body_length
        self.num_legs = num_legs
        self.development = development
        if development:
            self.genome = np.random.random((2, num_legs + 1, 2 * num_legs)) * 2 - 1
        else:
            self.genome = np.random.random((num_legs+1, 2*num_legs)) * 2 - 1
        self.id = idx
        self.fitness = 0
        self.age = 0
        self.dominated_by = []
        self.pareto_level = 0
        self.already_evaluated = False

    def __deepcopy__(self, memo):
        cls = self.__class__
        new = cls.__new__(cls)
        new.__dict__.update(deepcopy(self.__dict__, memo))
        return new

    def start_evaluation(self, env_type, eval_time, blind, pause):
        self.sim = PYROSIM(playPaused=pause, evalTime=eval_time, playBlind=blind)
        _robot = Vehicle(self.sim, self.genome, self.speed, self.eval_time, self.body_length, self.num_legs,
                         self.development)
        _env = Environment(env_type, self.sim, self.body_length, 1+2*self.num_legs)
        self.sim.Start()

    def compute_fitness(self):
        self.sim.Wait_To_Finish()
        dist = self.sim.Get_Sensor_Data(sensorID=self.num_legs)
        self.fitness += [dist[-1]]
        del self.sim
        self.already_evaluated = True

    def mutate(self, new_id, prob=None):
        if prob is None:
            prob = 1/float(self.genome.size)
        change = np.random.normal(scale=np.abs(self.genome))
        new_genome = np.clip(self.genome + change, -1, 1)
        mask = np.random.random(self.genome.shape) < prob
        self.genome[mask] = new_genome[mask]
        self.id = new_id
        self.already_evaluated = False

    def dominates(self, other):
        if self.fitness > other.fitness and self.age <= other.age:
            return True

        elif self.fitness == other.fitness and self.age < other.age:
            return True

        elif self.fitness == other.fitness and self.age == other.age and self.id < other.id:
            return True

        else:
            return False


class Population(object):
    def __init__(self, size, num_env=4, eval_time=500, speed=0.3, body_length=0.1, num_legs=4, development=False):
        self.size = size
        self.gen = 0
        self.individuals_dict = {}
        self.max_id = 0
        self.num_env = num_env
        self.eval_time = eval_time
        self.speed = speed
        self.body_length = body_length
        self.num_legs = num_legs
        self.development = development
        self.non_dominated_size = 0
        self.pareto_levels = {}
        self.add_random_inds(size)
        self.evaluate()

    def print_non_dominated(self):
        print self.pareto_levels[0]

    def evaluate(self, fitness_stat=np.mean, blind=True, pause=False):

        for key, ind in self.individuals_dict.items():
            if not ind.already_evaluated:
                ind.fitness = []

        for env_type in range(self.num_env):
            for key, ind in self.individuals_dict.items():
                if not ind.already_evaluated:
                    ind.start_evaluation(env_type, self.eval_time, blind, pause)

            for key, ind in self.individuals_dict.items():
                if not ind.already_evaluated:
                    ind.compute_fitness()

        todo = [key for key, ind in self.individuals_dict.items() if not ind.already_evaluated]
        while len(todo) > 0:
            to_remove = []
            for key in todo:
                this_ind = self.individuals_dict[key]
                if len(this_ind.fitness) == self.num_env:
                    ind.fitness = fitness_stat(ind.fitness)
                    to_remove += [key]
            todo = [key for key in todo if key not in to_remove]

    def create_children_through_mutation(self, fill_pop_from_non_dom=True):
        if fill_pop_from_non_dom:
            while len(self.individuals_dict) < self.size:
                for key, ind in self.individuals_dict.items():
                    child = deepcopy(ind)
                    child.mutate(self.max_id)
                    self.individuals_dict[self.max_id] = child
                    self.max_id += 1

        else:
            for key, ind in self.individuals_dict.items():
                child = deepcopy(ind)
                child.mutate(self.max_id)
                self.individuals_dict[self.max_id] = child
                self.max_id += 1

    def increment_ages(self):
        for key, ind in self.individuals_dict.items():
            ind.age += 1

    def add_random_inds(self, num_random=1):
        for _ in range(num_random):
            self.individuals_dict[self.max_id] = Individual(self.max_id, self.speed, self.eval_time, self.body_length,
                                                            self.num_legs, self.development)
            self.max_id += 1

    def update_dominance(self):
        for key, ind in self.individuals_dict.items():
            ind.dominated_by = []

        for key1, ind1 in self.individuals_dict.items():
            for key2, ind2 in self.individuals_dict.items():
                if key1 != key2:
                    if self.individuals_dict[key1].dominates(self.individuals_dict[key2]):
                        self.individuals_dict[key2].dominated_by += [key1]

        self.non_dominated_size = 0
        self.pareto_levels = {}
        for key, ind in self.individuals_dict.items():
            ind.pareto_level = len(ind.dominated_by)
            if ind.pareto_level in self.pareto_levels:
                self.pareto_levels[ind.pareto_level] += [(ind.id, ind.fitness, ind.age)]
            else:
                self.pareto_levels[ind.pareto_level] = [(ind.id, ind.fitness, ind.age)]
            if ind.pareto_level == 0:
                self.non_dominated_size += 1

    def reduce(self, keep_non_dom_only=True, pairwise=False):
        self.update_dominance()

        if keep_non_dom_only:  # completely reduce to non-dominated front (most pressure, least diversity)

            children = {}
            for idx, fit, age in self.pareto_levels[0]:
                children[idx] = self.individuals_dict[idx]
            self.individuals_dict = children

        elif pairwise:  # reduce by calculating pairwise dominance (least pressure, most diversity)

            while len(self.individuals_dict) > self.size and len(self.individuals_dict) > self.non_dominated_size:
                current_ids = [idx for idx in self.individuals_dict]
                np.random.shuffle(current_ids)
                inds_to_remove = []
                for idx in range(1, len(self.individuals_dict)):
                    this_id = current_ids[idx]
                    previous_id = current_ids[idx-1]
                    if self.individuals_dict[previous_id].dominates(self.individuals_dict[this_id]):
                        inds_to_remove += [this_id]
                for key in inds_to_remove:
                    del self.individuals_dict[key]

        else:  # add by pareto level until full

            children = {}
            for level in sorted(self.pareto_levels):
                sorted_level = sorted(self.pareto_levels[level], key=lambda x: x[1], reverse=True)
                for idx, fit, age in sorted_level:
                    if len(children) < self.size:
                        children[idx] = self.individuals_dict[idx]
            self.individuals_dict = children

