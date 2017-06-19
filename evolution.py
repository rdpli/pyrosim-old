import pickle
import random
import numpy as np
from replicators import Population


POP_SIZE = 30
GENS = 1000
NUM_ENV = 2
EVAL_TIME = 1000
FIT_STAT = np.sum


for run in range(30):

    random.seed(run)
    np.random.seed(run)

    for compress in [False, True]:

        pop = Population(POP_SIZE, num_env=NUM_ENV, development_type=1, fitness_stat=FIT_STAT,
                         compress_multiple_brains=compress)

        for gen in range(GENS):
            pop.create_children_through_mutation()
            pop.add_random_inds(1)
            pop.increment_ages()
            pop.evaluate()
            pop.reduce()
            pop.print_non_dominated()
            pop.gen += 1

        f = open('~/scratch/Dev_Compression/Dev_Compress_{0}_Run_{1}.p'.format(int(compress), run), 'w')
        pickle.dump(pop, f)
        f.close()


# r = open('data/Dev_1_Run_1.p', 'r')
# final_pop = pickle.load(r)
#
# sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
# final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(blind=False, eval_time=EVAL_TIME, pause=True)
#
# r.close()




