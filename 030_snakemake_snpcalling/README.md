# Snakemake SNP Calling Pipeline

## Overview
This repository contains a Snakemake pipeline that automates a full Single Nucleotide Polymorphism (SNP) calling workflow. It takes raw `.fastq` files, performs quality control, maps the reads to a reference genome (hg38), calls variants, annotates their biological effects, and extracts the results into a final, human-readable `.tsv` file.

## Repository Contents
* `Snakefile`: The master Snakemake pipeline containing all execution rules.
* `extract_vcf.py`: A custom Python parser designed to extract fields and SnpEff annotations from a VCF file into a TSV format (replaces SnpSift).
* `.gitignore`: Prevents heavy intermediate genomic data (e.g., `.bam`, `.vcf`) from being accidentally pushed to this repository.
* `README.md`: This instruction file.

## Prerequisites
This pipeline is designed to be run on the VSC (Flemish Supercomputer Center) in an interactive session.

Before running the pipeline, ensure the class Conda environment is active in your path:
```bash
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH