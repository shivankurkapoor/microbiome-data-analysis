'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
'''
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Polygon
from utils import tableau20

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


def transform_ticks(ticks):
    new_ticks = []
    for i in range(0, len(ticks) - 1, 2):
        t1 = ticks[i]
        t2 = ticks[i + 1]
        new_ticks.append((t1 + t2) / 2.0)
    return new_ticks


def gen_plots(group, sigFeatures, sigFeaturesIdx, data, index, output):
    if sigFeatures:
        group = group.strip().split(',')
        group = map(lambda x: x.strip(), group)
        bp_data = []
        for feature in sigFeatures:
            data_g1 = list(data[(data.group == group[0])][feature])
            data_g2 = list(data[(data.group == group[1])][feature])
            bp_data.append(data_g1)
            bp_data.append(data_g2)

        fig, ax1 = plt.subplots(figsize=(20, 10))
        fig.canvas.set_window_title('A Boxplot Example')
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

        numDists = len(sigFeatures)
        features = sigFeatures
        N = 500

        bp = plt.boxplot(bp_data, notch=0, vert=1, whis=1.5)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='red')

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                       alpha=0.5)

        # Hide these grid behind plot objects
        ax1.set_axisbelow(True)
        ax1.set_title('Comparison of significant features among groups', size=16)
        ax1.set_xlabel('Features', size=12)
        #ax1.set_ylabel('q-value', size=12)

        # Now fill the boxes with desired colors
        boxColors = [tableau20[0], tableau20[5]]
        numBoxes = numDists * 2
        medians = list(range(numBoxes))

        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxX = []
            boxY = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = list(zip(boxX, boxY))
            # Alternate between Dark Khaki and Royal Blue
            k = i % 2
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
            ax1.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                plt.plot(medianX, medianY, 'k')
                medians[i] = medianY[0]
            # Finally, overplot the sample averages, with horizontal alignment
            # in the center of each box
            plt.plot([np.average(med.get_xdata())], [np.average(bp_data[i])],
                     color='w', marker='*', markeredgecolor='k')

        # Set the axes ranges and axes labels
        ax1.set_xlim(0.5, numBoxes + 0.5)
        top = max(np.max(np.asarray(bp_data))) + 0.05
        bottom = min(np.min(np.asarray(bp_data))) - 0.05
        ax1.set_ylim(bottom, top)
        old_ticks = ax1.get_xticks()
        ticks = transform_ticks(ax1.get_xticks())
        ax1.xaxis.set(ticks=ticks)
        xtickNames = plt.setp(ax1, xticklabels=np.repeat(features, 1))
        plt.setp(xtickNames, rotation=45, fontsize=12)

        # Due to the Y-axis scale being different across samples, it can be
        # hard to compare differences in medians across the samples. Add upper
        # X-axis tick labels with the sample medians to aid in comparison
        # (just use two decimal places of precision)
        # pos = np.arange(numBoxes) + 1
        # upperLabels = [str(np.round(s, 2)) for s in medians]
        # weights = ['bold', 'semibold']
        # for tick, label in zip(range(numBoxes), old_ticks):
        #     k = tick % 2
        #     ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
        #              horizontalalignment='center', size='8', weight=weights[k],
        #              color=boxColors[k])

        # Finally, add a basic legend
        plt.figtext(0.80, 0.08, ' Group: ' + group[0] + ' ',
                    backgroundcolor=boxColors[0], color='black', weight='roman',
                    size='9')
        plt.figtext(0.80, 0.045, ' Group: ' + group[1] + ' ',
                    backgroundcolor=boxColors[1],
                    color='white', weight='roman', size='9')
        plt.figtext(0.80, 0.010, '*', color='white', backgroundcolor='silver',
                    weight='roman', size='7')
        plt.figtext(0.815, 0.010, ' Average Value', color='black', weight='roman',
                    size='9')

        plt.savefig(os.path.join(output, 'plot' + str(index) + '.png'), dpi=80)
