import argparse
import sqlite3
import logging
from pathlib import Path
from typing import List, Tuple, Any

import pandas as pd
import vcfpy

def parse_args() -> argparse.Namespace:
  """Parse command-line arguments."""
  parser = argparse.ArgumentParser(description="Parse annotated VCF into SQLite DB.")
  parser.add_argument("--vcf", required=True, help="Path to input VCF file")
  parser.add_argument("--db", required=True, help="Path to output SQLite database")
  return parser.parse_args()

def process_vcf(vcf_path:str) -> Tuple[pd.DataFrame, pd.DataFrame,pd.DataFrame]:
  """Extracts SNPs, Effects, and Calls from a VCF into Pandas DataFrames."""
  reader =  vcfpy.Reader.from_path(vcf_path)
  
  # clean sample names (removing path and .bam extension)
  sample_name = [
    s.split("/")[-1].replace(".bam", "")
    for s in reader.header.samples.names
  ]
  
  snps, effects, calls = [], [], []
  
  logging.info(f"Parsing VCF: {vcf_path} with {len(sample_name)} samples...")
  
  for i, record in enumerate(reader):
    
    # skip or log multi-allelics if strictly expecting bi-allelic
    if not record.ALT or not record.REF:
      continue

    # snps table
    alt = record.ALT[0].value
    snp_id = f"{record.CHROM}_{record.POS}_{record.REF}_{alt}"
    
    snps.append([
      snp_id, 
        record.CHROM, 
        record.POS, 
        record.REF, 
        alt, 
    ])
    
    # effects table
    ann_list = record.INFO.get("ANN", [])
    for ann in ann_list:
      parts = ann.split("|")
      
      if len(parts) >= 7: # check
        effects.append([
              snp_id,
              parts[3], # gene
              parts[1], # effect
              parts[2], # impact
              parts[6] # transcript

        ]) 
    
    # calls table
    for j, call in enumerate(record.calls):
      
      pl_raw = call.data.get("PL")
      pl_str = ",".join(map(str, pl_raw)) if pl_raw else None
      
      calls.append([
            snp_id,
            sample_name[j],
            call.data.get("GT"),
            pl_str
        ])
      
  reader.close()
  
  df_snps = pd.DataFrame(
    snps,
    columns=["snp_id", "chrom", "pos", "ref", "alt"]
  )

  df_effects = pd.DataFrame(
      effects,
      columns=["snp_id", "gene", "effect", "impact", "transcript"]
  )

  df_calls = pd.DataFrame(
      calls,
      columns=["snp_id", "sample_id", "genotype", "pl"] 
  )
  
  return df_snps, df_effects, df_calls

def main():
  args = parse_args()
  
  out_path = Path(args.db)
  out_path.parent.mkdir(parents=True, exist_ok=True)
  
  df_snps, df_effects, df_calls = process_vcf(args.vcf)
  
  with sqlite3.connect(args.db) as conn:
    df_snps.to_sql("snps", conn, if_exists="replace", index=False)
    df_effects.to_sql("effects", conn, if_exists="replace", index=False)
    df_calls.to_sql("calls", conn, if_exists="replace", index=False)
    
    # add indexes for relational querying performance
    conn.execute("CREATE INDEX IF NOT EXISTS idx_snp_id ON snps(snp_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_eff_snp_id ON effects(snp_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_snp_id ON calls(snp_id);")
        
if __name__ == "__main__":
  main()
  
  