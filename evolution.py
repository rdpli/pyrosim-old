from replicators import Population
import pickle

POP_SIZE = 20
GENS = 300
NUM_ENV = 1
EVAL_TIME = 500

pop = Population(POP_SIZE)

for gen in range(GENS):
    pop.create_children_through_mutation()
    pop.add_random_inds(1)
    pop.increment_ages()
    pop.evaluate(NUM_ENV)
    pop.reduce()
    pop.print_non_dominated()
    pop.gen += 1


f = open('robot.p', 'w')
pickle.dump(pop, f)
f.close()


r = open('robot.p', 'r')
final_pop = pickle.load(r)

sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
for e in range(NUM_ENV):
    final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(env_type=e, blind=False, eval_time=EVAL_TIME, pause=True)

r.close()




