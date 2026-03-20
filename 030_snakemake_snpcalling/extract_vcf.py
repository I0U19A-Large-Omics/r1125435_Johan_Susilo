import sys

def extract_vcf_fields(vcf_in, tsv_out):
    with open(vcf_in, 'r') as f_in, open(tsv_out, 'w') as f_out:
        
        # 1. Write our custom header exactly as SnpSift would
        f_out.write("CHROM\tPOS\tID\tREF\tALT\tFILTER\tANN[*].EFFECT\n")

        for line in f_in:
            # Skip all the VCF metadata and the original header line
            if line.startswith('#'):
                continue 

            # 2. Split the main VCF row into its standard columns
            cols = line.strip().split('\t')
            chrom, pos, vid, ref, alt, qual, filt, info = cols[:8]

            # 3. Parse the complex INFO column
            effects = []
            info_items = info.split(';')
            
            for item in info_items:
                if item.startswith('ANN='):
                    # Strip away the 'ANN=' prefix
                    raw_annotations = item[4:]
                    
                    # Split by comma (in case there are multiple effects)
                    for ann in raw_annotations.split(','):
                        # SnpEff separates data with pipes '|'
                        # Format: Allele | Annotation (Effect) | Impact | Gene Name | ...
                        parts = ann.split('|')
                        if len(parts) > 1:
                            effects.append(parts[1]) # Grab the Effect
            
            # Join multiple effects back together with commas
            effect_str = ",".join(effects) if effects else ""

            # 4. Write our neatly extracted row to the TSV
            f_out.write(f"{chrom}\t{pos}\t{vid}\t{ref}\t{alt}\t{filt}\t{effect_str}\n")

# Run the function using arguments passed from the command line
if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_vcf_fields(input_file, output_file)