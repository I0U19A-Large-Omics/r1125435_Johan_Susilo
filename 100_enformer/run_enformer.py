import argparse
import asyncio
import time
from fake_enformer import async_predict
from pathlib import Path
import vcfpy


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Parse annotated VCF and fetch Enformer scores concurrently.")
    parser.add_argument("--vcf", required=True, help="Path to input VCF file")
    parser.add_argument("--out", required=True, help="Path to output prediction score TSV")
    parser.add_argument("--concurrency", type=int, default=50, help="Max concurrent requests to the fake_enformer server")
    return parser.parse_args()


async def fetch_score(coordinate: str, semaphore: asyncio.Semaphore):
    """Fetch the score for a single coordinate while respecting the concurrency limit."""
    async with semaphore:
        score = await async_predict(coordinate)
        print(f"Finished: {coordinate}")
        return coordinate, score

def process_vcf(vcf_path: str) -> set:
    """Extracts unique SNP coordinates from a VCF using vcfpy."""
    reader = vcfpy.Reader.from_path(vcf_path)
    unique_coordinates = set()

    for record in reader:
        # Skip if not bi-allelic
        if not record.ALT or not record.REF:
            continue

        chrom = record.CHROM
        pos = record.POS
        ref = record.REF
        
        # vcfpy stores ALT as a list of Substitution objects; extract the string value
        alt = record.ALT[0].value

        # fake_enformer requires the chromosome to start with 'chr'
        if not chrom.startswith('chr'):
            chrom = f"chr{chrom}"

        # Format exactly as fake_enformer expects
        coordinate = f"hg38:{chrom}:{pos}:{ref}:{alt}"
        unique_coordinates.add(coordinate)
        
    return unique_coordinates
  
async def main():
    args = parse_args()
    
    # Prepare output directory
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract coordinates
    print(f"Reading VCF: {args.vcf}")
    unique_coordinates = process_vcf(args.vcf)
    print(f"Extracted {len(unique_coordinates)} unique SNPs.")

    # Setup Concurrency
    print(f"Initializing asyncio execution with a max concurrency of {args.concurrency}...")
    semaphore = asyncio.Semaphore(args.concurrency) 
    tasks = [fetch_score(coord, semaphore) for coord in unique_coordinates]
    
    # Start timer for profiling requirement
    start_time = time.time()
    
    # Execute all tasks concurrently
    print("Sending requests to fake_enformer... please wait.")
    results = await asyncio.gather(*tasks)
    
    # Stop timer
    end_time = time.time()
    duration = end_time - start_time
    
    # Save to TSV
    with open(out_path, "w") as out_f:
        out_f.write("coordinate\tscore\n") # Write Header
        for coord, score in results:
            out_f.write(f"{coord}\t{score}\n")
            
    print(f"Done! Saved to {out_path}")
    print(f"Wall-clock time: {duration:.2f} seconds (Concurrency level: {args.concurrency})")


if __name__ == "__main__":
    asyncio.run(main())