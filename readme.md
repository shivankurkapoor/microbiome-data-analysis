# Microbiome Data Analysis

## Introduction
Three kinds of data analysis performed on the microbiome data. The first is Beta Regression that detects abundance differences cross different groups using zero-inflated beta regression. The second is Beta Diversity that computes the differences between microbial communities (among different groups) based on phylogenetic information. And the third is Alpha Diversity that captures the microbial diversity within each group.

## Beta Regression
The approach used for performing differential abundant analysis has been described in detail in \[1\]. The methodology has been summarized below:
1. Data Input - The input for this analysis is a <img src="https://tex.s2cms.ru/svg/n%5Ctimes%20p%20" alt="n\times p " /> matrix <img src="https://tex.s2cms.ru/svg/C" alt="C" />, where n are the number of samples and p are families of the taxonomy hierarchy into which microbial data has been classified. Each entry <img src="https://tex.s2cms.ru/svg/C_%7Bi%2Cj%7D" alt="C_{i,j}" /> is the number of reads from sample <img src="https://tex.s2cms.ru/svg/i" alt="i" /> that mapped to family <img src="https://tex.s2cms.ru/svg/j" alt="j" />. Each sample is also associated with an outcome measurement that denotes the group to which that sample belongs. A sample input file can be found [here](https://github.com/shivankurkapoor/microbiome-data-analysis/blob/master/beta_regression/input.csv)
2. Model - The authors have proposed a zero-inflated beta regression model with the assumption that the proportional dependent variable (normalized features) can be characterized by beta distribution. As it is evident from the attached sample that the input matrix is sparse, meaning the number of reads is zero for many sample and family combinations. These excess zero counts are also handled by the zero-inflated beta regression model. The exact model formulation has been described in \[1\].

3. Steps - 
	* Feature Screening - Features with total counts less than <img src="https://tex.s2cms.ru/svg/2%5Ctimes%20n" alt="2\times n" /> where <img src="https://tex.s2cms.ru/svg/n" alt="n" /> is the sample size are removed.
	* Data Normalization - Since it is highly likely that different samples have different total reads, so to ensure that counts are comparable normalization is performed by converting the absolute reads to proportions representing the relative contribution of each feature to each of the samples. Data normalization is performed by dividing the read for each sample and family (<img src="https://tex.s2cms.ru/svg/C_%7Bi%2Cj%7D" alt="C_{i,j}" />) by <img src="https://tex.s2cms.ru/svg/T_%7Bi%7D" alt="T_{i}" />, where <img src="https://tex.s2cms.ru/svg/T_%7Bi%7D" alt="T_{i}" /> is the total counts of sample <img src="https://tex.s2cms.ru/svg/i" alt="i" />. After normalization data ranges between <img src="https://tex.s2cms.ru/svg/0" alt="0" /> and <img src="https://tex.s2cms.ru/svg/1" alt="1" />.
	* Data Transformation - This step is optional and can be controlled using input parameter in the program. When the distributions of the proportions are extremely left skewed, i.e. most of the non-zero proportions are very small, the assumption of beta distribution may not be satisfied. In such cases square root transformation <img src="https://tex.s2cms.ru/svg/%5Csqrt%20x" alt="\sqrt x" /> is performed on the data. After transformations, the proportions still range between <img src="https://tex.s2cms.ru/svg/0" alt="0" /> and <img src="https://tex.s2cms.ru/svg/1" alt="1" /> but with distribution better fitting a beta distribution.
	* Zero-inflated Beta Regression – Zero-inflated Beta regression is performed between each normalized feature (response variable) and outcome (explanatory variable). <img src="https://tex.s2cms.ru/svg/p-values" alt="p-values" /> of regression coefficients are obtained in each regression.
	* Multiple Hypothesis Testing Correction – <img src="https://tex.s2cms.ru/svg/q-%20values" alt="q- values" /> are calculated from p-values \[2\]. Features (Families) with q-values less than or equal to significant levels are chosen.


## Beta Diversity
Beta diversity is used to compare microbiome samples to one another. A beta diversity metric calculates the distances among all pair of samples. In our analysis, beta diversity has been calculated using UniFrac distances. This method, UniFrac, measures the phylogenetic distances between sets of taxa in a phylogenetic tree as the fraction of the branch length of the tree that leads to the descendants from either one environment or the other, but not both. This method has been described in \[3\].

Beta Diversity has been calculated using QIIME \[4\]. The input for calculating the beta diversity are the collapsed and annotated fasta files for each sample in each group. Sample input file is attached [here](https://github.com/shivankurkapoor/microbiome-data-analysis/blob/master/beta_diversity/input.txt)   
 
The steps for calculating beta diversity are as follows:
1. Combine – The input annotated fasta files belonging to different groups and samples are combined into a single fasta file. The sequence id of each sequence is prepended with sample and group information as <img src="https://tex.s2cms.ru/svg/SequenceId_%7BNew%7D" alt="SequenceId_{New}" /> <img src="https://tex.s2cms.ru/svg/%3D" alt="=" /> <img src="https://tex.s2cms.ru/svg/GroupId" alt="GroupId" /> <img src="https://tex.s2cms.ru/svg/%2B" alt="+" /> <img src="https://tex.s2cms.ru/svg/'%5C_'" alt="'\_'" /> <img src="https://tex.s2cms.ru/svg/%2B" alt="+" /> <img src="https://tex.s2cms.ru/svg/SampleId" alt="SampleId" /> <img src="https://tex.s2cms.ru/svg/%2B" alt="+" /> <img src="https://tex.s2cms.ru/svg/'%5C_'" alt="'\_'" /> <img src="https://tex.s2cms.ru/svg/SequenceId_%7B%7D" alt="SequenceId_{}" />
2. Align – The sequences in the combined fasta file are aligned using MUSCLE \[5\].
3. Pick OTUs – The OTU picking step assigns similar sequences to operational taxonomic units, or OTUs, by clustering sequences based on a user defined similarity threshold. Sequences which are similar at or above the threshold level are taken to represent the presence of a taxonomic unit. Mothur \[6\] is used to perform clustering with default clustering algorithm as furthest-neighbor. Sequence similarity threshold has been set to the default value of <img src="https://tex.s2cms.ru/svg/0.97" alt="0.97" />. The output consists of two files (i.e. seqs_otus.txt and seqs_otus.log). The .txt file is composed of tab-delimited lines, where the first field on each line corresponds to an (arbitrary) cluster identifier, and the remaining fields correspond to sequence identifiers assigned to that cluster. Sequence identifiers correspond to those provided in the input FASTA file. The content of a sample output txt file is attached [here](https://github.com/shivankurkapoor/microbiome-data-analysis/blob/master/beta_diversity/sample.txt)  
4. Modify OTUs – The OTUs in the previous step are generated using the collapsed fasta files. The OTU file is modified using the absolute reads information obtained from the sequence identifiers. The first part of the sequence identifier contains the absolute reads for that sequence as follows: <img src="https://tex.s2cms.ru/svg/M0096743000000000-A3JHG1110524653220331352481569%3A6%3A1569%3A340" alt="M0096743000000000-A3JHG1110524653220331352481569:6:1569:340" /></br>                                                     The number in the red denotes the number of times this particular sequence is repeated. Using this information, the OTU txt file is modified to repeat the sequence identifiers against each OTU number as many time as denoted in the id. To differentiate the repeating identifiers, each id is appended with <img src="https://tex.s2cms.ru/svg/'.'" alt="'.'" /> followed by the count of repetition. 
       For e.g. <img src="https://tex.s2cms.ru/svg/Group2.Sample2_M0096743000000000-A3JHG11106736712748%3A1%3A11%3A9.0" alt="Group2.Sample2_M0096743000000000-A3JHG11106736712748:1:11:9.0" /></br>
		The number 	in the red denotes the count of the repetition.
5. Create OTU table – This step generates a .biom file, where columns correspond to samples and rows corresponds to OTUs and the number of times a sample appears in a particular OTU.
6. Make Phylogeny Tree – This step produces a phylogeny tree with the set of sequences representative of the OTUs. The first sequence for each OTU in the output OTU txt file is selected as representative sequence. 
7. Jackknifed Beta Diversity – Beta diversity is calculated by resampling the data from the biom file and phylogenetic measures from phylogeny tree. This resampling is required to account for the fact that the number of sequences in each sample will affect the species diversity. Jackknifed Beta Diversity is performed by a workflow script in QIIME and consists of the following sub steps:
	* Computes a beta diversity distance matrix for the complete dataset
	* Performs multiple rarefactions at a single depth
	* Computes distance matrices for all the rarefied OTU tables. Both weighted and unweighted Unifrac distance matrices [3] are calculated. 
	* Build UPGMA trees for the rarefactions
	* Compare all the trees to determine the consensus tree and support value for each branch
	* Performs principal ordinate analysis on the rarefied distance matrices
	* Generate plots of the principal ordinates

## Alpha Diversity
Alpha diversity corresponds to the species diversity within a group. There are various measures to calculate alpha diversity \[7\]. In our analysis, we have used Simpson’s Index, Shannon Entropy and Simpson Reciprocal as alpha diversity measures.

1. Simpson Index:
           <img src="https://tex.s2cms.ru/svg/1-%5Csum%20p_i%5E%7B2%7D" alt="1-\sum p_i^{2}" />

     where <img src="https://tex.s2cms.ru/svg/p_%7Bi%7D" alt="p_{i}" /> is the proportion of the community represented by OUT <img src="https://tex.s2cms.ru/svg/i" alt="i" />
2. Shannon Entropy: <img src="https://tex.s2cms.ru/svg/H%3D-%5Csum_%7Bi%3D1%7D%5E%7Bs%7Dp_ilog_2p_i" alt="H=-\sum_{i=1}^{s}p_ilog_2p_i" />

     where <img src="https://tex.s2cms.ru/svg/s" alt="s" /> is the numbers of OTUs and <img src="https://tex.s2cms.ru/svg/p_i" alt="p_i" /> is the proportion of the community represented by OUT <img src="https://tex.s2cms.ru/svg/i" alt="i" />

3. Simpson Reciprocal: <img src="https://tex.s2cms.ru/svg/%5Cdfrac%7B1%7D%7B%5Csum%20p_i%5E%7B2%7D%7D" alt="\dfrac{1}{\sum p_i^{2}}" />	

    where <img src="https://tex.s2cms.ru/svg/p_i" alt="p_i" /> is the proportion of the community represented by OUT <img src="https://tex.s2cms.ru/svg/i" alt="i" />

Paper
https://linkinghub.elsevier.com/retrieve/pii/S2590177X19300393

References
1. Zero-Inflated Beta Regression for Differential Abundance Analysis with Metagenomics Data -[https://www.ncbi.nlm.nih.gov/pubmed/26675626](https://www.ncbi.nlm.nih.gov/pubmed/26675626)
2. Statistical significance of genomewide studies -  [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC170937](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC170937)
3. UniFrac: A New Phylogenetic Method for Comparing Microbial Communities - [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1317376/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1317376/)
4. QIIME - [http://qiime.org/](http://qiime.org/)
5. MUSCLE - [https://en.wikipedia.org/wiki/MUSCLE_(alignment_software)](https://en.wikipedia.org/wiki/MUSCLE_(alignment_software))
6. Mothur - [https://www.ncbi.nlm.nih.gov/pubmed/19801464](https://www.ncbi.nlm.nih.gov/pubmed/19801464)
7. Alpha Diversity Measure - [http://scikit-bio.org/docs/latest/generated/skbio.diversity.alpha.html](http://scikit-bio.org/docs/latest/generated/skbio.diversity.alpha.html)
