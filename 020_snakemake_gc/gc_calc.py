import sys
import os

def calculate_gc(fasta_file):
    #create three variables to keep track of your counts.
    g_count = 0
    c_count = 0
    total_bases = 0
    
    #open the 'fasta_file' in read mode and loop through each line in the file. 
    with open(fasta_file, "r") as file:
      for line in file:
        if line.startswith(">"):
           continue
        else:
         #use uppercase for DNA sequence, so we don't miss the lowercase g and c characters.
          line = line.upper()   
          line = line.strip()  #remove any leading/trailing whitespace.
         
          g_count += line.count("G")
          c_count += line.count("C")
          total_bases += len(line)

      if total_bases > 0:
          percentage = (g_count + c_count) / total_bases * 100
          return percentage
      else:
          return 0.


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    
    #extract just the file name and remove the '.fa' extension
    basename = os.path.basename(input_filepath).replace('.fa', '')
    percentage = calculate_gc(input_filepath) # run calculation
    
    # Format the text
    final_text = f"{basename}\t{percentage}\n"
    
    #open output file and write the final text to the file.
    with open(output_filepath, 'w') as out_file:
        out_file.write(final_text)