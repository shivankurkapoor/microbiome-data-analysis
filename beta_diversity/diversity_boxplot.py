"""
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from plotutils import *


def boxplot(df, measure, output, name):
    data = []
    groups = sorted(list(set(df['group'])))
    for group in groups:
        df_ = df[df.group == group]
        l = map(lambda x: float(x), list(df_[measure]))
        data.append(l)

    # multiple box plots on one figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data)
    for median in bp['medians']:
        median.set(color='black', linewidth=2, linestyle='--')
    for i in range(len(groups)):
        x = np.random.normal(i + 1, 0.05, size=len(data[i]))
        sp = ax.plot(x, data[i], filled_markers[i])
    ax.set_ylabel(name)
    ax.set_xticklabels(groups)
    fig.savefig(os.path.join(output, measure + '.png'), bbox_inches='tight', dpi=100)
