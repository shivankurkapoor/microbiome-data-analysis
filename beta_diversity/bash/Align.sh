chmod 775 /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash/Align.sh
source  activate qiime1
~/anaconda2/envs/qiime1/bin/python ~/anaconda2/envs/qiime1/bin/align_seqs.py -m muscle -o /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity -i /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/combined.fasta
/home/leelab/anaconda2/bin/python /home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/betadiversity.py --task=pick_otus --combined_file=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/combined.fasta --output=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity --script_path=/home/leelab/PycharmProjects/BioInfoPipeLine/BetaDiversity/Bash