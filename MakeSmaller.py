import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK stopwords if not already downloaded
import nltk
nltk.download('stopwords')

# Define function to remove non-unicode characters
def remove_non_unicode(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

# Define function to remove stop words and tokenize rows, and write to files
def tokenize_rows(input_file, output_prefix, batch_size=10000):
    stop_words = set(stopwords.words('english'))

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header

        batch_count = 0
        current_batch = []

        for row in reader:
            query = row[0]
            answer = row[1]
            
            # Remove non-unicode content
            query = remove_non_unicode(query)
            answer = remove_non_unicode(answer)
            
            tokenized_query = [word for word in word_tokenize(query) if word.lower() not in stop_words]
            tokenized_answer = [word for word in word_tokenize(answer) if word.lower() not in stop_words]
            current_batch.append((tokenized_query, tokenized_answer))

            if len(current_batch) == batch_size:
                output_file = f"{output_prefix}_{batch_count}.csv"
                with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow(["Tokenized_Query", "Tokenized_Answer"])
                    writer.writerows(current_batch)
                batch_count += 1
                current_batch = []

        # Write remaining rows
        if current_batch:
            output_file = f"{output_prefix}_{batch_count}.csv"
            with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(["Tokenized_Query", "Tokenized_Answer"])
                writer.writerows(current_batch)
                
tokenize_rows("tokenizeddd.csv", "tokenized_data")
