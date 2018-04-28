chmod 775 /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash/Alpha_Diversity.sh
source  activate qiime1
~/anaconda2/envs/qiime1/bin/python ~/anaconda2/envs/qiime1/bin/alpha_diversity.py -m simpson_reciprocal,shannon,simpson -o /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/result.txt -i /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/otu_table.biom
/home/leelab/anaconda2/bin/python /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/betadiversity.py --task=alpha_plots --output=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity