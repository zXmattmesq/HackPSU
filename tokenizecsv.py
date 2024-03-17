import csv

def process_row(row):
    pairs = row.split('\n')
    processed_pairs = []
    incomplete_pairs = []  # For storing rows with gaps
    for pair in pairs:
        parts = pair.split(' , ', 1)
        if len(parts) == 2:
            query, answer = parts
            processed_pairs.append((query.strip(), answer.strip()))
        else:
            # Assuming a gap means either query or answer is missing.
            incomplete_pairs.append(pair.strip())
    return processed_pairs, incomplete_pairs

def process_csv(input_file_path, output_file_path, incomplete_output_path):
    with open(input_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', encoding='utf-8', newline='') as outfile, \
         open(incomplete_output_path, mode='w', encoding='utf-8', newline='') as incomplete_file:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        incomplete_writer = csv.writer(incomplete_file)
        
        writer.writerow(['Query', 'Answer'])
        
        for row in reader:
            if row:
                processed_pairs, incomplete_pairs = process_row(row[0])
                for pair in processed_pairs:
                    writer.writerow(pair)
                for incomplete_pair in incomplete_pairs:
                    # Writing incomplete pairs to another file or handling them differently
                    incomplete_writer.writerow([incomplete_pair])

# Replace with your actual file paths
input_file_path = 'output.csv'
output_file_path = 'tokenizeddd.csv'
incomplete_output_path = 'incomplete.csv'

process_csv(input_file_path, output_file_path, incomplete_output_path)