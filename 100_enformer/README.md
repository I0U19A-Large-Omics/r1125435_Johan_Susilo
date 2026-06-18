# 🧬 Concurrent Enformer Prediction Script

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Asyncio](https://img.shields.io/badge/Asyncio-Concurrency-brightgreen)
![HPC](https://img.shields.io/badge/HPC-VSC-orange)

## 📌 Overview
This repository contains `run_enformer.py`, a standalone, high-performance Python script designed to fetch prediction scores from the `fake_enformer` model for a large set of annotated SNPs. 

Because the `fake_enformer` API introduces an intentional 5–20 second delay per call to simulate model latency, a sequential approach is computationally unfeasible. This script resolves the I/O bottleneck by implementing **asynchronous concurrency** via `asyncio`. It efficiently schedules thousands of concurrent network requests while utilizing a semaphore to ensure the shared REST server is not overwhelmed.

---

## ⚙️ Environment Prerequisites

This pipeline requires the specific course Conda environment and must be executed within an **interactive session** on the VSC (Flemish Supercomputer Center). **Do not run this on the login node.**

### 1. Source the Conda Environment
Link the pre-configured environment to your path:
```bash
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH

```

### 2. Start an Interactive Session

If you haven't already, allocate resources on the cluster (example for WICE):

```bash
srun -n 1 -c 2 --mem 4G --time=2:00:00 \
     --export=ALL \
     -A lp_edu_large_omics \
     -p interactive \
     --cluster wice \
     --pty bash -

```

---

## 🚀 Execution

The script requires two primary arguments: `--vcf` (input file) and `--out` (destination).

Run the script using your specific data paths:

```bash
python /path/to/file/100_enformer/run_enformer.py \
  --vcf /path/to/file/snakemake_workspace/030.vcf/annotated_snps.vcf \
  --out /path/to/file/170.enformer

```

### 🎛️ Optional Parameters

* **`--concurrency`**: Controls the maximum number of simultaneous requests allowed by the semaphore. The default is `50`. If you wish to profile speedups and test different rate limits, you can append this flag (e.g., `--concurrency 10`).

---

## 📊 Expected Output

Upon execution, the script will silently parse the input VCF, extract unique bi-allelic coordinates, format them strictly to `hg38:chr:pos:ref:alt`, and process them in asynchronous batches.

A successful run will print the total unique SNPs identified, wait for the API calls to resolve, and save a `.tsv` file containing the `coordinate` and `score` columns. It will also output the final wall-clock duration for profiling purposes.
