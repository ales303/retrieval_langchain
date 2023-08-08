import os
import glob
import numpy as np

def count_words_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        words = text.split()
        num_words = len(words)
    return num_words

def main():
    directory_path = './destwin_text_files'  # Replace with your directory path
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))

    word_counts = []
    for file_path in txt_files:
        num_words = count_words_in_file(file_path)
        word_counts.append((os.path.basename(file_path), num_words))
        print(f'Filename: {os.path.basename(file_path)}, Number of Words: {num_words}')
        print(f'Filename: {os.path.basename(file_path)}, Number of Words / 750: {round(num_words/750, 1)}')

    if word_counts:
        word_counts.sort(key=lambda x: x[1])  # Sort by word count

        print(f'Mean Number of Words per Document: {np.mean([wc[1] for wc in word_counts])}')
        print(f'Median Number of Words per Document: {np.median([wc[1] for wc in word_counts])}')
        print(f'Max Number of Words per Document: {np.max([wc[1] for wc in word_counts])}')
        print(f'Min Number of Words per Document: {np.min([wc[1] for wc in word_counts])}')

        # Print the top 10 largest files
        print("\nTop 10 largest files by word count:")
        for file, count in word_counts[-10:]:
            print(f'Filename: {file}, Word count: {count}')

        # Print the top 10 smallest files
        print("\nTop 10 smallest files by word count:")
        for file, count in word_counts[:10]:
            print(f'Filename: {file}, Word count: {count}')

    else:
        print('No text files found.')

if __name__ == '__main__':
    main()
