# Import necessary libraries
import nltk
import os
import sys
from pathlib import Path
from nltk.collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


input_folder = sys.argv[1]  # an input_folder
output_folder = sys.argv[2]  # an output_folder
num_sents = sys.argv[3]  # the number of sentences of the summary


# This is how I ran the code in terminal (venv):
# python summarizer.py ./articles/ ./output/ ./6/


input_folder = "articles"

output_folder = "./output"
Path("./output").mkdir(exist_ok=True)  # Creates the directory and does not raise an exception, if the directory already exists
index = 0

summaries = output_folder + "/" + "texts_summaries" + ".txt"

with open(summaries,"w",encoding = "utf-8") as output:
        for file in os.listdir(input_folder):
            if file.endswith(".txt"):  # For every file that ends with .txt in the specific folder
                file_name = os.path.join(input_folder, file)  # Generates full path of each file in the folder
                # print(file_name)   # Prints the full path of every text in the folder
                file = open(file_name, "r", encoding="utf-8-sig")  # Opens the file for reading
                read_lines = file.read()  # Reads all the lines of the file

                def process_tokens(text):
                    # Tokenize in words
                    lower_case = text.lower() # Turns the letters into lower case
                    tokens = nltk.word_tokenize(lower_case) # Splits the text into tokens
                    #print(tokens)
                    
                    # Filters out punctuation from the tokens
                    no_punct = [word for word in tokens if word.isalpha()]  # the function isalpha() removes the non-alphabetic tokens
                    # print(f'Tokens without punctuation for every text in the folder:\n',words[:70])

                    # Filters out stopwords from the tokens
                    stop_words_set = set(stopwords.words("english"))
                    words = [w for w in no_punct if not w in stop_words_set]
                    #print(f'Tokens without stop_words for every text in the folder:\n', words[:70])                   
                    return words
                
                
                def process_sentences(text):
                    # Tokenize in sentences
                    split_newline = text.split('\n') # Replace the newline with space between sentences using split() and join()
                    split_newline = " ".join(split_newline)
                    sentences = nltk.sent_tokenize(split_newline) # Split the text in sentences
                    return sentences
                
                
                def count_occurences(words):
                    # Count the occurence of a word of each text
                    word_counts = {}
                    for w in words:
                        if w not in word_counts.keys():
                            word_counts[w] = 1
                        else:
                            word_counts[w] += 1
                    #print(word_counts)
                    return word_counts


                def word_frequency(word_counts):
                    # Count the frequency distribution of each word
                    freq_dist = {}
                    max_freq = max(word_counts.values()) # Gets the maximum frequency value of each text
                    for word in word_counts.keys():
                        freq_dist[word] = (word_counts[word]/max_freq)
                        # Divides the occurrence of each word by the frequency of the most occurring word
                    return freq_dist
                

                def sentence_scores(sentences,words,freq_dist):
                    # Calculate the sum of frequencies for the words of each sentence
                    sentence_scores = {}
                    for sent in sentences:
                        for word in words:
                            if word.lower() in freq_dist.keys():
                                if sent not in sentence_scores.keys():
                                    sentence_scores[sent] = freq_dist[word.lower()]
                                else:
                                    sentence_scores[sent] += freq_dist[word.lower()]
                    #print(sentence_scores)
                    return sentence_scores


                # Summarize text according to the scored(important) sentences and the selected number of sentences for a summary
                def summarize(sentence_scores,n_sents):

                    top_sents = Counter(sentence_scores)
                    summary = ""
                    scores = []

                    top = top_sents.most_common(n_sents)
                    for i in top:
                        summary += i[0].rstrip() + " "
                        scores.append((i[1], i[0]))
                    return summary[:-1], scores


                #------------------ Run all the functions, create and write the summaries -------------- 
                tokens = process_tokens(read_lines)
                
                sents = process_sentences(read_lines)
                num_sents = len(sents)
               
                word_counts = count_occurences(tokens)
                
                frequency_distribution = word_frequency(word_counts)
                
                sents_scores = sentence_scores(sents,tokens,frequency_distribution)
                
                summary,sents_scores = summarize(sents_scores,num_sents)
                summ = str(summary)
                print(summ)

                index += 1

                output.write(f"TEXT {index}:\n{file_name}\n\n{read_lines}\nSUMMARY {index}:\n{summ}\n\n")
                print(f"\nThe file is ready!")

                file.close()


if __name__ == '__main__':
    print (f"\nNo. of arguments passed is: {len(sys.argv)}")
    print (f"Argument List: {str(sys.argv)}")
    for indx, arg in enumerate(sys.argv):
        print(f"Argument #{indx} is: {arg}")
