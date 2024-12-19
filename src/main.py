import genanki
import jieba
import json
import csv

# Path to the text that is going to be analyzed and have a deck made from it's unfamiliar vocab.
INPUT_FILE_PATH: str = "../input/file.txt"

# Path to full word lists of each HSK Level.
HSK_PATH: str = "../data/hsk.json"

# Path to the users known characters.
SAVED_PATH: str = "../data/saved.json"

# Path to punctionation.
PUNCTUATION_PATH: str = "../data/punctuation.txt"

CEDICT_PATH: str = "../data/cedict.json"

SENTENCES_PATH: str = "../data/sentences.tsv"




def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False




# Step 1: Read in the input text.
input_text: str = ""
with open(INPUT_FILE_PATH, encoding="utf8") as input_file:
    input_text = input_file.read()

# Step 2: Get the highest HSK 2.0 level that the user has completed.
waiting_for_level: bool = True
user_hsk_level: int = 0
while waiting_for_level:
    try:
        input_u: str = input("Enter your HSK 2.0 level (highest level which you have fully completed) e.g. '3': ")
        user_hsk_level = int(input_u) # TODO: This may not be the best method.
        if 0 <= user_hsk_level <= 6:
            waiting_for_level = False
    except:
        print("Some sort of invalid input received; just input a whole number.")


# Step 3: Load in a list of all the words that the user knows from both HSK and saved.
known_words: list[str] = []

# First, the HSK words.
with open(HSK_PATH, encoding="utf8") as hsk_file:
    hsk_json: str = hsk_file.read()
    hsk_data: list[dict] = json.loads(hsk_json)
    for word_data in hsk_data:
        if word_data["HSK"] <= user_hsk_level:
            known_words.append(word_data["hanzi"])
            
# Second, the saved known words.
with open(SAVED_PATH, encoding="utf8") as saved_file:
    saved_json: str = saved_file.read()
    saved_data: list[dict] = json.loads(saved_json)
    for word_data in saved_data:
        known_words.append(word_data["hanzi"])

# Step 4: Cut the read-in text into segments of language (almost words), and save a list of them that has no duplicates
segments: list[str] = []
raw_segments: list[str] = list(jieba.cut(input_text, cut_all=False))
for segment in raw_segments:
    if segment not in segments:
        segments.append(segment)

# Step 5: Now we need to clean up the segment list, by removing punctuation and numbers. (what's left is words only)
with open(PUNCTUATION_PATH, encoding="utf8") as punct_file:
    punctuation: str = punct_file.read()
    i = 0
    while i <= len(segments) -1:        
        if segments[i] in punctuation or is_float(segments[i]):
            segments.pop(i)
        else:
            i+=1
            
words: list[str] = segments

# Step 6: Subtract the known words from the words that we have been left with.
for known_word in known_words:
    if known_word in words:
        i = words.index(known_word)
        words.pop(i)

# Step 7: Let's initialize a data structure that will hold our
# words, pinyin, meaning, example sentence, example sentence pinyin, and example sentence meaning.

# This is the final step before moving on to exporting this data into an ANKI deck.

# Step 7a: instantiate.
deck_data: list[dict[str]] = []

# Step 7b: populate with words.
for word in words:
    deck_data.append(
        {
            "word" : word
        }
    )
    
# Step 7c: populate with pinyin and meaning.
with open(CEDICT_PATH, encoding="utf8") as cedict_file:
    cedict_json_str: str = cedict_file.read()
    cedict: list[dict] = json.loads(cedict_json_str)
    for deck_entry in deck_data:
        for cedict_entry in cedict:
            if deck_entry["word"] == cedict_entry["simplified"]:
                deck_entry["pinyin"] = cedict_entry["pinyin"]
                deck_entry["definition"] = cedict_entry["english"]
                
# Step 7d: populate with example sentence, its meaing, and pinyin.
with open(SENTENCES_PATH, encoding="utf8") as sentences_file:
    ex_sentences: list[str] = list(csv.reader(sentences_file, delimiter="\t"))
    for deck_entry in deck_data:
        for ex_sentence in ex_sentences:
            if deck_entry["word"] in ex_sentence[0]:
                deck_entry["ex_sentence"] = ex_sentence[0]
                deck_entry["ex_sentence_pinyin"] = ex_sentence[1]
                deck_entry["ex_sentence_transl"] = ex_sentence[2]
                break

# print(deck_data)
test=json.dumps(deck_data, ensure_ascii=False, indent=4)
print(test)