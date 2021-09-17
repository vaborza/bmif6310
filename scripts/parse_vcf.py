# Victor Borza
# Sep 17, 2021
#
# Parse VCF data per variant

import pandas as pd
import time
import numpy as np
import pickle

start_t = time.time() # Start timer

# Desired parameters
N_VARIANTS = 1000

# with 10 var, 2.94s; with 100 var, 12.24s and 17 MB, with 300 var, 35.34s and 50.72 MB

demo_df = pd.read_csv('../igsr_samples.tsv',sep='\t')
ancestry_df = pd.DataFrame(data=demo_df['Superpopulation code']).transpose()
ancestry_df.columns = demo_df['Sample name']

#print(ancestry_df)

with open('../ALL.chr1.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf') as infile:
    i = 1
    for line in infile:
        i = i + 1
        if i == 21:
            variants_df = pd.DataFrame(columns = line.split())
            variant_ancestry_cols = ancestry_df.columns & variants_df.columns
            variants_df = variants_df.append(ancestry_df[variant_ancestry_cols])
        if i > 21:
            variant_df = pd.DataFrame(line.split()).transpose()
            variant_df.columns = variants_df.columns.values
            variants_df = variants_df.append(variant_df,ignore_index=True)
        if i > (N_VARIANTS + 20):
            break
        if (i % 50) == 0:
            print('Batch done: ' + str(i))

variants_df = variants_df.drop(columns=['#CHROM','ID','QUAL','FILTER','FORMAT'])

# Turn allelic data into more friendly numbers

variants_df = variants_df.replace({'0\|0': '0'}, regex=True)
variants_df = variants_df.replace({'1\|0': '1'}, regex=True)
variants_df = variants_df.replace({'0\|1': '1'}, regex=True)
variants_df = variants_df.replace({'1\|1': '2'}, regex=True)

variants_df.to_pickle('../ancestry_map_1k_var.pkl')

print('Dataframe is this many megabytes big: ' + 
        str(variants_df.memory_usage(index=True,deep=True).sum()/1e6))
end_t = time.time()
print('Executed code in seconds: ' + str(end_t - start_t))

