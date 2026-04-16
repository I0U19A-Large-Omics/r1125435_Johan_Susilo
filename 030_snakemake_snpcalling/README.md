# 🧬 Snakemake SNP Calling Pipeline

## 📌 Overview
This repository contains a Snakemake workflow for an end-to-end **SNP calling pipeline**.  

It processes raw `.fastq` sequencing data and performs:

- Quality control (QC)
- Read alignment to a reference genome (hg38)
- Variant calling
- Variant annotation (SnpEff-based)
- Conversion of VCF results into a final `.tsv` file for analysis

---

## 📂 Repository Structure
- Snakefile # Main Snakemake workflow
- extract_vcf.py # Custom VCF → TSV parser (SnpEff-aware)
- README.md # Pipeline documentation
- .gitignore # Prevents large intermediate files from being tracked

## ⚙️ Prerequisites

This pipeline is designed for the **VSC (Flemish Supercomputer Center)** environment and must be run inside an interactive SLURM session.

---

## 🚀 Setup Instructions

### 1. Setup Conda environment

```bash
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH
```

### 2. Start an interactive SLURM session (WICE cluster)

```bash
srun -n 1 -c 2 --mem 4G --time=2:00:00 \
     --export=ALL \
     -A lp_edu_large_omics \
     -p interactive \
     --cluster wice \
     --pty bash -
```

### 3. run snakemake 
```bash
snakemake --snakefile /path/to/project/Snakefile \
          --directory /scratch/yourname/where it contain fastq files \
          --cores 2
```