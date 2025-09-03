import os
import sys
import re
from collections import defaultdict

BUFFER_SIZE = 4096

def read_file(fd):
    content = b""
    while True:
        chunk = os.read(fd,BUFFER_SIZE)
        if not chunk:
            break
        content += chunk
    return content.decode ('utf-8', errors='ignore')

def write_file(fd, data):
    os.write(fd, data.encode('utf-8'))

def process_text(text):
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text) #only letters
    return words

def main():
    if len(sys.argv) != 3:
        print("wrong command entered")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
#open file
    try:
        input_fd = os.open(input_path, os.O_RDONLY)
    except FileNotFoundError:
        print("file not found")
        sys.exit(1)

    #read file
    text= read_file(input_fd)
    os.close(input_fd)

    #count words
    words= process_text(text)
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1

    #sort by frequency, then alphabetically
    sorted_words = sorted(word_count.items(), key=lambda x:(x[0]))

    #open output file (write, create if doesnt exist, truncate if exists)
    output_fd = os.open(output_path, os.O_WRONLY| os.O_CREAT| os.O_TRUNC, 0o6444)

    #write output file
    for word, count in sorted_words:
        line = f"{word} {count}\n"
        write_file(output_fd,line)

    os.close(output_fd)


main()
