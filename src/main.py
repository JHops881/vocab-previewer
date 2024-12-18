# use this library to make anki decks
import genanki

# use this library to parse chinese text and get the words from it.
import jieba

import requests
from bs4 import BeautifulSoup

# Path to the text that is going to be analyzed and have a deck made from it's unfamiliar vocab.
INPUT_FILE_PATH: str = "../input/file.txt"

# Path to full word lists of each HSK Level.
LEVEL_1_PATH: str = "./dictionary/hsk20-1.txt"
LEVEL_2_PATH: str = "./dictionary/hsk20-2.txt"
LEVEL_3_PATH: str = "./dictionary/hsk20-3.txt"
LEVEL_4_PATH: str = "./dictionary/hsk20-4.txt"
LEVEL_5_PATH: str = "./dictionary/hsk20-5.txt"
LEVEL_6_PATH: str = "./dictionary/hsk20-6.txt"

# Now we can assign the levels to their corresponding vocab
vocab_levels: dict = {
    1 : LEVEL_1_PATH,
    2 : LEVEL_2_PATH,
    3 : LEVEL_3_PATH,
    4 : LEVEL_4_PATH,
    5 : LEVEL_5_PATH,
    6 : LEVEL_6_PATH,
}

# Grab the text in the input file for extraction.
input_file = open(INPUT_FILE_PATH, encoding="utf8")
text = input_file.read()
input_file.close()

punctuation: list[str] = [
    "'", '"', "[", "]", "{", "}", "!",
    ".", ">", "<", "=", "-", "+", "_",
    "*", "&", "^", "%", "$", "#", "@",
    "(", ")", ";", ":", ",", "/", "?",
    "\\", "|", "【", "】", "。", "「",
    "」", "﹁", "﹂", "“", "”", "『", "』",
    "‘", "’", "、", "·", " ", "《", "》",
    "〈", "〉", "﹏", "…", "⸺", "–",
    "～", "_", "，", "\n", "（", "）"
]

# Unique, unknown, Mandarin words found in the text
unique_words: dict = {}



# Get the highest HSK 2.0 level that the user has completed. Use this to erase words found in the text that the
# user already knows.
waiting_for_level: bool = True
user_level: int = 0
while waiting_for_level:
    try:
        input_u: str = input("Enter your HSK 2.0 level (highest level which you have fully completed) e.g. '3': ")
        user_level = int(input_u)
        if 0 <= user_level <= 6:
            waiting_for_level = False
    except:
        print("Some sort of invalid input received; just input a whole number.")



# First, we cut the text into Mandarin words
seg_list = jieba.cut(text, cut_all=False)

# Then we have to go through a and assure the quality of each word
for word in seg_list:
    
    # Make sure, first, that we havent already added it to the unique words dictionary
    if word not in unique_words:
        
        # TODO: THIS IS INCREDIBLY UGLY AND NOT ELEGANT
        # Flag it if is a number
        is_number: bool = False
        try:
            float(word)
            is_number = True
        except:
            pass
        
        # If it's not flagged as a number, and not a punctuation mark, then we can add it.
        if word not in punctuation and not is_number:
            
            unique_words[word] = "None"
            
# Go through according to the selected level, and delete all known words.
#TODO: COMMENT
def eliminate_know_words(vocab_level_dict: dict, level: int, words: dict):
    print(list(range(level+1))[1:])
    for n in list(range(level+1))[1:]:
        with open(vocab_level_dict[n], encoding="utf8") as file:
            lines = [line.rstrip() for line in file]
            for ci in lines:
                if ci in words:
                    words.pop(ci)
    return words
                    
unique_words = eliminate_know_words(vocab_levels, user_level, unique_words)

def get_example_sentence(word: str) -> str:
    """Use web scraping to retrieve a mandarin example sentence from a mandarin word.

    Args:
        word (str): Mandarin word.

    Returns:
        str: Mandarin example sentence that uses the word.
    """
    
    url: str = f"https://www.iciba.com/word?w={word}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        html_content = response.text  # Get the HTML content of the page

        # Step 3: Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Step 4: Extract specific data (example: all paragraph texts)
        paragraphs = soup.find_all("p")  # Find all <p> tags
        for p in paragraphs:
            print(p.text)  # Print the text inside each <p> tag
    else:
        print("Failed to retrieve the webpage:", response.status_code)
    
    
    

# Display all the unique, unknown, words that the text contained.
counter: int = 1
for k, v in unique_words.items():
    print(f"{counter} {k} : {v}")
    counter+=1