import sys
import pickle
import numpy as np
from replicators import Population


SEED = int(sys.argv[1])

POP_SIZE = 30
GENS = 1000
NUM_ENV = 4
EVAL_TIME = 1000
FIT_STAT = np.min
SPEED = 0.1


for develop in [True, False]:

    pop = Population(POP_SIZE, num_env=NUM_ENV, development=develop, fitness_stat=FIT_STAT, speed=SPEED)

    for gen in range(GENS):
        pop.create_children_through_mutation()
        pop.add_random_inds(1)
        pop.increment_ages()
        pop.evaluate()
        pop.reduce()
        pop.print_non_dominated()
        pop.gen += 1

    exp_name = "Devo" if develop else "Evo"
    f = open('data/Exp_{0}_Run_{1}.p'.format(exp_name, SEED), 'w')
    pickle.dump(pop, f)
    f.close()


# r = open('data/Exp_Devo_Run_0.p', 'r')
# final_pop = pickle.load(r)
#
# sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
# final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(blind=False, eval_time=EVAL_TIME, pause=True)
#
# r.close()




