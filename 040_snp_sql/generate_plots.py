import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path


def main(db_path, output_dir):
  
  Path(output_dir).mkdir(parents=True, exist_ok=True)
  
  conn = sqlite3.connect(db_path)
  
  # 1st figure, SNP impact severity per sample
  query = """
  -- counting unique SNPs per sample per impact, not all multiplied rows
  SELECT c.sample_id, e.impact, COUNT(DISTINCT s.snp_id) as snp_count
  FROM snps s
  JOIN calls c
    ON s.snp_id = c.snp_id
  JOIN effects e
    ON s.snp_id = e.snp_id
  GROUP BY c.sample_id, e.impact;  
    
  """
  
  df = pd.read_sql_query(query, conn)
  
  # to order the x axis of impact position
  order = ["HIGH", "MODERATE", "LOW", "MODIFIER"]
  
   # plotting figure 1
  sns.set_theme(style="whitegrid", palette="colorblind")
  plt.figure(figsize=(10, 6))
  ax1 = sns.barplot(data=df, 
              x="impact", 
              y="snp_count", 
              hue="sample_id", 
              order=order
              )
  
  # plot title and other settings
  ax1.set_title("SNP Impact Severity per Sample", fontsize=14, pad=15)
  ax1.set_xlabel("Impact Category", fontsize=12)
  ax1.set_ylabel("Distinct SNP Count", fontsize=12)
  ax1.set_ylim(0, None) # Ensure y-axis starts at zero
  
  plt.savefig(f"{output_dir}/fig1_impact_severity.svg")
  plt.close()
  
  # 2nd figure, Which genes are most affected by HIGH or MODERATE impact variants?
  # justification: horizontal bar chart of top gene with high/moderate impact
  # identifies biological targets must likely to have functional changes
  
  query_genes = """
    -- select gene column
    SELECT gene, COUNT(*) as variant_count
    FROM effects
    WHERE impact IN ('HIGH', 'MODERATE')
    GROUP BY gene
    -- show top 5 genes
    ORDER BY variant_count DESC
    LIMIT 10;
    
  """
  df_genes = pd.read_sql_query(query_genes, conn)

  # plotting figure 2
  plt.figure(figsize=(10, 6))
  sns.set_theme(style="whitegrid", palette="colorblind")
  
  ax2 = sns.barplot(
    data=df_genes, 
    x="variant_count", 
    y="gene")
  
  ax2.set_title("Top 10 Genes Affected by High/Moderate Impact Variants", fontsize=14, pad=15)
  ax2.set_xlabel("Number of Significant Variants", fontsize=12)
  ax2.set_ylabel("Gene Name", fontsize=12)
  ax2.set_xlim(0, None)   # ensure x-axis starts at 0

  plt.savefig(f"{output_dir}/fig2_gene_impacts.svg", format='svg')
  plt.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--db", required=True, help="Path to SQLite DB")
  parser.add_argument("--outdir", required=True, help="Output directory for figures")
  args = parser.parse_args()
  main(args.db, args.outdir)
  
  