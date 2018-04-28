'''
Author : Shivankur Kapoor
Contact : kapoors@usc.edu
'''
import pandas as pd
import os
import numpy as np
import subprocess
from boxplot import *
from utils import *
from argparse import ArgumentParser


def transform(df):
    cols = df.columns
    df = df.as_matrix()
    group = df[:, 0]
    data = df[:, 1:]
    st = np.sum(data, axis=1, dtype=float)
    data = data / st[:, None]
    data = pd.DataFrame(data, columns=cols[1:])
    data['group'] = group
    return data


def run_beta_reg(input, output, rscript, alpha):
    try:
        subprocess.check_call(['Rscript',os.path.join(rscript,'betaregression.R'), input, output], shell = False)
    except Exception as e:
        print 'Error in running beta regression ', e

    data = transform(pd.read_csv(input))
    if os.path.isfile(output):
        display_result = []
        df = pd.read_csv(output, index_col=0)
        df = df.fillna('NaN')
        families = set()
        for index, row in df.iterrows():
            try:
                group = row['groups'].strip()
                sigFeatures = row['sigFeatures'].strip()
                sigFeaturesIdx = []
                if sigFeatures != 'NaN':
                    sigFeatures = sigFeatures.split(',')
                    sigFeatures = map(lambda x: x.strip(), sigFeatures)
                    sigFeaturesIdx = range(len(sigFeatures))
                pValues = map(lambda x: float(x), row['pValues'].split(','))
                qValues = map(lambda x: float(x), row['qValues'].split(','))

                for i, idx in enumerate(sigFeaturesIdx):
                    display_dict = {}
                    display_dict.update({'Groups' : group})
                    p = pValues[idx]
                    q = qValues[idx]
                    family = sigFeatures[i]
                    families.add(family)
                    display_dict.update({'Family' : family, 'p-value' : p, 'q-value' : q})
                    display_result.append(display_dict)

                display_sig_features = []
                display_sig_features_idx = []
                for i, qv in enumerate(qValues):
                    if qv < alpha:
                        display_sig_features.append(sigFeatures[i])
                        display_sig_features_idx.append(i)

                gen_plots(group, display_sig_features, display_sig_features_idx, data, index, output.rsplit(os.sep,1)[0])

            except Exception as e:
                print 'Error while reading R output ', e
        display_result_df = pd.DataFrame(display_result)
        display_result_df = display_result_df.sort_values(by = ['q-value'])
        cols = ['Groups', 'Family', 'p-value', 'q-value']
        display_result_df.to_csv(os.path.join(output.rsplit(os.sep,1)[0], 'beta_regression.csv'),columns=cols, index=False)

    else:
        print 'Missing output file from beta regression'
        exit(1)


def gen_data_matrix(family_file_dict, output):
    families = set()
    family_data_dict = dict(family_file_dict)
    for group in family_file_dict:
        for sample, file in family_file_dict[group].items():
            with open(file, 'r') as f:
                family_dict = {}
                for line in f.readlines():
                    family, _, count = line.strip().split(' ')
                    families.add(family.replace('\"', ''))
                    family_dict[family.replace('\"', '')] = int(count)
                family_data_dict[group][sample] = family_dict

    data_list = []
    for group in family_data_dict:
        for sample, data_dict in family_data_dict[group].items():
            rec_dict = {'group': group}
            for family in families:
                rec_dict.update({family: data_dict.get(family, 0)})
            data_list.append(rec_dict)

    cols = ['group'] + list(families)
    df = pd.DataFrame(data_list, columns=cols)
    path = os.path.join(output, 'input.csv')
    df.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    parser = ArgumentParser(description="Beta Regression")

    '''
    Defining Arguments
    '''
    parser.add_argument("--input_dir", dest="root", default="")
    parser.add_argument("--r_scripts", dest="RScript", default="")
    parser.add_argument("--alpha", dest="alpha", default=0.05, type=float)

    '''
    Parsing Arguments
    '''
    args = parser.parse_args()

    print args.root
    print args.RScript
    print args.alpha

    try:
        assert args.root != ''
        assert args.RScript != ''
    except AssertionError as e:
        print 'Invalid input', e

    family_file_dict = {}
    for _, groups, _ in os.walk(args.root):
        for group in groups:
            for _, samples, _ in os.walk(os.path.join(args.root, group)):
                for sample in samples:
                    if group not in family_file_dict:
                        family_file_dict[group] = {}
                    family_file_dict[group][sample] = os.path.join(args.root, group, sample, 'family.txt')

    file = gen_data_matrix(family_file_dict, args.root)
    run_beta_reg(file, os.path.join(args.root, 'result.csv'), args.RScript, args.alpha)
