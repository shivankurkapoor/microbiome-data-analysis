chmod 775 /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash/Create_OTU_Table.sh
source  activate qiime1
~/anaconda2/envs/qiime1/bin/python ~/anaconda2/envs/qiime1/bin/make_otu_table.py -o /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/otu_table.biom -i /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/combined_aligned_otus_modified.txt
/home/leelab/anaconda2/bin/python /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/betadiversity.py --task=make_phylo_tree --modified_fasta=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/combined_aligned_modified.fasta --output=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity --script_path=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash --biom=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/otu_table.biom