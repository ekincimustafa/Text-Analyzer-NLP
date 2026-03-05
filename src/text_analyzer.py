import locale
from sys import argv

locale.setlocale(locale.LC_ALL, "en_US")


def f0_start(file_out):
    name_of_file = argv[1]              # writing input file name
    file_out.write(f"Statistics about {name_of_file:7}:\n")


def f_no_punctuations_text(file_in):            # for convenience
    text = file_in.read()
    my_punct = ".,!?()'[]{}:;\""
    clear_text = ""
    for element in text:
        if element not in my_punct:             # separating the text from punctuation
            clear_text += element.lower()       # minimising letters
    return clear_text           # returning because I will use this in other function


def f_strip_(file_in):                  # for convenience
    file_in.seek(0)                     # starting from beginning
    text = file_in.read()
    my_punct = ".,!?()'[]{}:;\""
    cleaned_text = ""

    for element in text.split():        # separating words because I will need them later
        cleaned_element = element.strip(my_punct)  # I need to remove unwanted things
        cleaned_text += cleaned_element.lower() + " "   # I add " " (space) because I want to get the words again

    return cleaned_text         # returning because I will use later


def f_word_count(clear_text, file_out):
    word_count = len(clear_text.split())       # finding number
    word_count = str(word_count)       # have to convert for writing
    file_out.write(f"{'#Words':24}: {word_count:}\n")
    return word_count               # returning because I will use later


def f_sentence_count(file_in, file_out):
    file_in.seek(0)             # I need to start beginning
    text = str(file_in.read())
    text = "".join(text)    # I need string , for this combining elements
    text = text.replace("...", ".")     # I convert because does not recognise three dots
    sentence_counter = [".", "!", "?"]
    sentence_count = sum(text.count(element) for element in sentence_counter)
    # I try every punctuation ,and finally I add all numbers with 'sum' method
    file_out.write(f"{'#Sentences':24}: {sentence_count:}\n")
    return sentence_count       # returning because I will use later


def f_words_div_sentence(word_count, sentence_count, file_out):
    word_div_sentence_count = int(word_count) / int(sentence_count)
    file_out.write(f"{'#Words/#Sentences':24}: {word_div_sentence_count:.2f}\n")


def f_character_counter(file_in, file_out):
    file_in.seek(0)
    text = file_in.read().rstrip()  # I remove last character \n if I dont use this ,count 1 will appear more
    character_count = len(text)
    file_out.write(f"{'#Characters':24}: {character_count:}\n")


def f_character_just_words(file_in, file_out):
    file_in.seek(0)
    text = file_in.read()
    text = text.split()
    my_punct = ".,!?()'-[]{}:;\"" + "\n"
    character_just_words = 0
    # I need just word and I remove everything else
    for element in text:
        new_text = element.strip(my_punct)
        character_just_words += len(new_text)

    file_out.write(f"{'#Characters (Just Words)':24}: {character_just_words:}\n")


def f_words_and_freq(cleaned_text, file_out):
    word_list = cleaned_text.split()        # I used the function I defined before
    word_count = len(word_list)
    word_freq = {}          # I need dict for word and freq

    for element in word_list:
        if element in word_freq:
            word_freq[element] += 1 / int(word_count)  # updating if element already exist
        else:                   # I div by word count because I need freq
            word_freq[element] = 1 / int(word_count)

    word_and_freq_list = word_freq.items()    # I can get both keys and values at the same time --> list
    sorted_words_and_freq = sorted(word_and_freq_list, key=lambda a: (-a[1], a[0]))
    # A[1] means freq and a[0] means word then I can sort it according to this
    # - means from big to small

    min_length = min(len(element) for element in word_list)   # I need to know min length
    shortest_words = [element1 for element1 in word_list if len(element1) == min_length]
    shortest_words = list(dict.fromkeys(shortest_words))  # eliminating repetitive elements
    shortest_words.sort()
    # I need to check if there is more than one short word

    if len(shortest_words) == 1:
        shortest_word = shortest_words[0]       # getting first element
        shortest_word_freq = word_freq.get(shortest_word, 0)  # I get the word freq from the dict, if there is no return 0
        file_out.write(f"{'The Shortest Word':24}: {shortest_word:24} ({shortest_word_freq:.4f})\n")
    else:
        file_out.write(f"{'The Shortest Words':24}:\n")
        for element in shortest_words:      # If there is more than one I need loop
            shortest_word_freq = word_freq.get(element, 0)
            file_out.write(f"{element:24} ({shortest_word_freq:.4f})\n")
    # Same with short word

    max_length = max(len(element) for element in word_list)
    longest_words = [element for element in word_list if len(element) == max_length]
    longest_words = list(dict.fromkeys(longest_words))
    longest_words.sort()

    if len(longest_words) == 1:
        longest_word = longest_words[0]
        longest_word_freq = word_freq.get(longest_word, 0)
        file_out.write(f"{'The Longest Word':24}: {longest_word:24} ({longest_word_freq:.4f})\n")
    else:
        file_out.write(f"{'The Longest Words':24}:\n")
        for element in longest_words:
            longest_word_freq = word_freq.get(element, 0)
            file_out.write(f"{element:24} ({longest_word_freq:.4f})\n")

    file_out.write(f"{'Words and Frequencies':24}:\n")

    for_new_garb_line = ""   # At the end is \n and this creates new line, I don't want this
    for element, frequencies in sorted_words_and_freq:
        for_new_garb_line += f"{element:24}: {frequencies:.4f}\n"
    file_out.write(for_new_garb_line.rstrip("\n"))      # I can remove new line


def main():
    with open(argv[1], "r") as file_in, open(argv[2], "w") as file_out:
        f0_start(file_out)
        clear_text = f_no_punctuations_text(file_in)  # I am using another function
        cleaned_text = f_strip_(file_in)
        word_count = f_word_count(clear_text, file_out)
        sentence_count = f_sentence_count(file_in, file_out)
        f_words_div_sentence(word_count, sentence_count, file_out)
        f_character_counter(file_in, file_out)
        f_character_just_words(file_in, file_out)
        f_words_and_freq(cleaned_text, file_out)


if __name__ == "__main__":
    main()
