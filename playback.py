import pickle
import numpy as np
from scipy.stats import mannwhitneyu

# EVAL_TIME = 500
#
# r = open('/home/sam/data/False_robot_0.p', 'r')
# final_pop = pickle.load(r)
#
# sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
# final_pop.individuals_dict[sorted_inds[-1]].start_evaluation(blind=False, eval_time=EVAL_TIME, pause=True)
#
# r.close()


data = []
for exp_name in range(3):
    for run in range(1, 31):
        r = open('/home/sam/Archive/skriegma/Neurogenesis/data/Dev_{0}_Run_{1}.p'.format(exp_name, run), 'r')
        final_pop = pickle.load(r)
        sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
        data += [(exp_name, run, final_pop.individuals_dict[sorted_inds[-1]].fitness)]
        r.close()

e = [f for (n, r, f) in data if n == 0]
d = [f for (n, r, f) in data if n == 1]

print np.mean(e), np.mean(d)
print np.std(e), np.std(d)
print mannwhitneyu(e, d)

