import pickle

EVAL_TIME = 500

r = open('/home/sam/data/False_robot_0.p', 'r')
final_pop = pickle.load(r)

sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(blind=False, eval_time=EVAL_TIME, pause=True)

r.close()




