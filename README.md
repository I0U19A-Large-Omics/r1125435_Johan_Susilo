# Omics Data Processing Workflows
**r1125435_Johan_Susilo**

## Project Overview
This repository contains example workflows for managing and analyzing omics data.  
The project demonstrates two approaches to sequence analysis:

1. A **manual SNP calling workflow** using a Jupyter notebook.
2. An **automated GC content calculation pipeline** implemented with Snakemake.

These workflows illustrate basic bioinformatics practices such as sequence handling, workflow automation, and reproducible analysis.

# Directory Description

## 010_manual_snpcall
Contains a notebook demonstrating manual SNP calling.

**File**

- `manual_snp_calling_workflow.ipynb`  
  Jupyter notebook showing step-by-step SNP identification and explanation of the process.

---

## 020_snakemake_gc
Contains a workflow for calculating GC content from FASTA files using Snakemake.

**Files**

- `Snakefile`  
  Defines workflow rules for running the GC content pipeline.

- `gc_calc.py`  
  Python script that reads FASTA sequences and calculates GC content.

# Purpose
This repository is intended as a learning project for practicing:

- handling omics sequence data
- building simple analysis scripts
- creating automated workflows
- organizing bioinformatics projects
