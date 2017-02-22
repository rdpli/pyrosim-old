from replicators import Population
import pickle

POP_SIZE = 30
GENS = 1000
NUM_ENV = 4
EVAL_TIME = 500
DEVO = False

pop = Population(POP_SIZE, num_env=NUM_ENV, development=DEVO)

for gen in range(GENS):
    pop.create_children_through_mutation()
    pop.add_random_inds(1)
    pop.increment_ages()
    pop.evaluate()
    pop.reduce()
    pop.print_non_dominated()
    pop.gen += 1


f = open('robot.p', 'w')
pickle.dump(pop, f)
f.close()


r = open('robot.p', 'r')
final_pop = pickle.load(r)

sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(blind=False, eval_time=EVAL_TIME, pause=True)

r.close()




