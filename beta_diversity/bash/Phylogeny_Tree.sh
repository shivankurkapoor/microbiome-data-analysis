chmod 775 /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash/Phylogeny_Tree.sh
source  activate qiime1
~/anaconda2/envs/qiime1/bin/python ~/anaconda2/envs/qiime1/bin/make_phylogeny.py -o /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/phylo.tre -i /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/combined_aligned_modified.fasta
/home/leelab/anaconda2/bin/python /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/betadiversity.py --task=beta_diversity --phylo_tree=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/phylo.tre --output=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity --script_path=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash --biom=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/otu_table.biom