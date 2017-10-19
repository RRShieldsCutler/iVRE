## Enterococcal secondary metabolome analysis

##### Repository associated with the biosynthetic gene cluster analysis of Enterococcal species associated with HCT patients.

#### License
    Copyright (C) 2017, Robin Shields-Cutler

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.


#### Methods relevant to the analysis
These analyses were carried out, and have only been tested, on Mac OSX 10.11.6, except where noted below.

Genome files were downloaded via FTP from the NCBI Reference Sequence Database. For information on which strains, see the strain mapping data file in this repo, which contains the RefSeq ID and annotated strain name for each assembly (i.e. not all are "complete" level genomes). Strain names and mappings to NCBI Refseq identifiers are provided in the data directory in this repo.

A local Linux server installation of antiSMASH v3.0 was used to predict biosynthetic gene clusters (BGCs)<sup>1</sup>, using the following basic command line structure:

```shell
run_antismash.py
                [genome_fna]
                --outputfolder [results_dir]
                --inclusive --clusterblast --asf --disable-BioSQL
		 --disable-svg --disable-embl --disable-write_metabolicmodel
                --disable-xls --disable-html --disable-BiosynML
```

The extracted amino acid coding sequences were concatenated and compared "all-vs-all" using the command line tool for BLAST in [Anaconda](https://anaconda.org/bioconda/blast). We generated a custom blast protein database from the amino acid sequences and queried the database with the same set of sequences (e-value cutoff of 7x10<sup>-10</sup>). [Custom C software](https://github.com/RRShieldsCutler/iVRE/tree/master/lib/), was used to evaluate the identity and compositional similarity between every two BGCs, generating an all-vs-all square matrix, where each row/column is a single BGC and the matrix value represents the identity score scaled by the amount of homologous gene overlap. Therefore, a perfect self-self match scores 100, while very dissimilar pathways would score 0.

From here, the matrix was converted to long format in R, then de-replicated, fully annotated using the above strain map, and filtered at a specific similarity threshold in a custom Python script, [here](https://github.com/RRShieldsCutler/iVRE/blob/master/lib/annotate_arrange_network.py). The resulting table was used to generate the networks in [Cytoscape v3.4.0](http://www.cytoscape.org/).
______________

References:  
<sup>1</sup> Weber T, Blin K, Duddela S, Krug D, Kim HU, Bruccoleri R, Lee SY, Fischbach MA, Müller R, Wohlleben W, Breitling R. (2015). antiSMASH 3.0—a comprehensive resource for the genome mining of biosynthetic gene clusters. Nucleic acids research, 43(W1), W237-W243.
