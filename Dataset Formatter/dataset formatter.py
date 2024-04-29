## REMEMBER ! THE DATASET SEEMS TO BE QUITE WRONG !
## THE LINE COUNTS ON JAWI AND RUMI ARE NOT SYNCHRONIZED
## BECAUSE THE RUMI SEEMS TO BE CINSUMED MORE LINES THAN JAWI IN ACTUAL PDF
## SOLUTION : DO NOT SEPARATE THE LINE UNTIL THE IS ' . ' OR ' , '
## FOR NOW, I WILL PROCEED WITH CURRENT DATA. DON'T FORGET TO FIX IT LATER !

import re

# Function to remove non-ASCII characters
def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)

def reverse_sentence(sentence):
    words = sentence.split()  # Split sentence into words
    reversed_words = words[::-1]  # Reverse the order of words
    return " ".join(reversed_words)  # Concatenate reversed words with a period at the end

# Function to format the dataset
def format_dataset(data):
    lines = data.strip().split('\n')
    formatted_data = ""
    for line in lines:
        if line.strip():
            sentences = re.split(r'\.\s*', line.strip()) # Split line into sentences based on period
            # reversed_sentences = [reverse_sentence(sentence) for sentence in sentences[::-1]]
            formatted_data += " ".join(sentences) + "\n"  # Concatenate sentences with newline
    return formatted_data.strip()  # Remove trailing spaces

# Removing empty lines
def remove_empty_line(data):
    lines = data.strip().split('\n')
    formatted_data = ""
    for line in lines:
        if line.strip():
            formatted_data += line.strip() + "\n"  # Add non-empty lines with a newline
    return formatted_data.strip()  # Remove trailing spaces


# Read dataset from file
input_file_path = "Dataset\\Extracted Data Jawi\\dataset 1 jawi.txt"  # Replace with the path to your input file
output_file_path = "Dataset\\Formatted Dataset Rumi\\formatted_dataset_jawi 1.txt"  # Replace with the path for the output file

with open(input_file_path, 'r', encoding='utf-8') as f:
    dataset_sample = f.read()

# Remove non-ASCII characters
# cleaned_dataset = remove_non_ascii(dataset_sample)

# Format the dataset
formatted_dataset = format_dataset(dataset_sample)

# Removed empty lines
removed_empty_lines_dataset = remove_empty_line(formatted_dataset)

# Write formatted dataset to a new file
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(removed_empty_lines_dataset)

print("Formatted dataset has been written to", output_file_path)