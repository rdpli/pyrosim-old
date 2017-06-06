import pickle
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

EXP_NAMES = ["Control", "Compression"]

data = []
for exp_num in range(2):
    for run in range(30):
        r = open('/home/sam/Projects/pyrosim/data/Dev_Compress_{0}_Run_{1}.p'.format(exp_num, run), 'r')
        final_pop = pickle.load(r)
        sorted_inds = sorted(final_pop.individuals_dict, key=lambda k: final_pop.individuals_dict[k].fitness)
        data += [(EXP_NAMES[exp_num], run, final_pop.individuals_dict[sorted_inds[-1]].fitness)]
        r.close()

e = [f for (n, r, f) in data if n == EXP_NAMES[0]]
d = [f for (n, r, f) in data if n == EXP_NAMES[1]]

print np.mean(e), np.mean(d)
print np.std(e), np.std(d)
print mannwhitneyu(e, d)
print ttest_ind(e, d)


df = pd.DataFrame(data=data, columns=["Group", "Run", "Fitness"])

g = sns.factorplot(x="Group", y="Fitness", data=df, size=4, kind="bar", capsize=.2, errwidth=2, linewidth=.5,
                   palette="muted")

g.despine(left=False, right=False, top=False)

g.set_ylabels("Fitness", fontsize=16)
g.set_xlabels("", fontsize=0)
g.set_xticklabels(["Control", "Developmental\nCompression"], fontsize=14)
# g.set_yticklabels(fontsize=12)


plt.savefig("plots/Dev_Compression_Preliminary_Results.pdf")


