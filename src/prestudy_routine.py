import genanki
import json
import csv
import os 
import sys

from deck import Deck
from segmentate import segmentate


def prestudy_routine(input_text: str, user_hsk_level: int):

    # Path to a (table-like) json file containing the entries of all HSK 2.0 words 1-6 tagged by level.
    HSK_PATH: str = "../data/hsk.json"

    # Path to the users known words.
    SAVED_PATH: str = "../data/saved.json"

    # Path to the json-fied CE-DECT dictionary -locally containing a best-effort database of all known chinese words
    CEDICT_PATH: str = "../data/cedict.json"

    # Path to file containing all our local example sentences
    SENTENCES_PATH: str = "../data/sentences.tsv"

    # Fix for some computers not executing in the proper dir.
    os.chdir( os.path.dirname( sys.argv[0] ) )

    # Load in a list of all the words that the user knows from both HSK and saved.
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

    # Cut the read-in text into words, and save a list of them without duplicates
    words: list[str] = []

    # segments has duplicates in it.
    segments: list[str] = segmentate(input_text, CEDICT_PATH, "simplified")

    for segment in segments:
        if segment not in words:
            words.append(segment)

    # Subtract the known words from the words that we have been left with.
    for known_word in known_words:

        if known_word in words:
            i = words.index(known_word)
            words.pop(i)

    # Let's initialize a data structure that will hold our
    # words, pinyin, meaning, example sentence, example sentence pinyin, and example sentence meaning.
    # This is the final step before moving on to exporting this data into an ANKI deck.
    deck: Deck = Deck()

    # populate with words.
    for word in words:
        deck.add_new_card(word)

    # TODO: solve the 只 issue. it has multiple entries. all 多音字 do.
    # populate with pinyin and meaning.
    with open(CEDICT_PATH, encoding="utf8") as cedict_file:
        cedict_json_str: str = cedict_file.read()
        cedict: list[dict] = json.loads(cedict_json_str)
        
        for card in deck.cards:
            for cedict_entry in cedict:
                if card.word == cedict_entry["simplified"]:
                    card.word_pinyin = cedict_entry["pinyin"]
                    card.word_translation = cedict_entry["english"]
                    
            # Catch erroneous words that don't exist according to cedict. Delete them.
            if card.word_translation == "":
                print(f"DEFINITION FOR {card.word} DOES NOT EXIST")
                deck.cards.remove(card)
                    
    # populate with example sentence, its meaning, and pinyin.
    with open(SENTENCES_PATH, encoding="utf8") as sentences_file:
        tatoeba_sentence_entries: list[str] = list(csv.reader(sentences_file, delimiter="\t"))
        for card in deck.cards:
            for entry in tatoeba_sentence_entries:
                if card.word in entry[0]:
                    
                    #TODO: SMART LEVELING
                    #TODO: 不同 is in 不同意! Fix this!
                    
                    card.sentence             = entry[0]
                    card.sentence_pinyin      = entry[1]
                    card.sentence_translation = entry[2]
                    break
                
    # Some of the words don't have example sentences. We need to scrape the web to retrieve them.
    for card in deck.cards:
        if card.sentence == "":
            
            print(f"No local example found for: {card.word}")
            print("Retrieving one from online.")

            # TODO: Need to find another way to get missing examples
                
    deck.print()

    # Covert to an anki deck
    qfmt: str = ""
    with open("./front.html") as front:
        qfmt = front.read()

    afmt: str = ""
    with open("./back.html") as back:
        afmt = back.read()
    
    css: str = ""
    with open("./style.css") as f:
        css = f.read()
    
    my_model = genanki.Model(
        1907462364,
        'Simple Model',
        fields=[
            {'name': 'Word'},
            {'name': 'Pinyin'},
            {'name': 'Definition'},
            {'name': 'ExampleSentence'},
            {'name': 'ExamplePinyin'},
            {'name': 'ExampleTranslation'},
        ],
        css=css,
        templates=[
            {
                'name': 'Card 1',
                'qfmt': qfmt,
                'afmt': afmt
            },
        ]
    )

    notes: list[genanki.Note] = []
    for card in deck.cards:
        notes.append(
            genanki.Note(
                model=my_model,
                fields=[
                    card.word,
                    card.word_pinyin,
                    " ".join(card.word_translation),
                    card.sentence,
                    card.sentence_pinyin,
                    card.sentence_translation
                ]
            )
        )

    my_deck = genanki.Deck(
        1907462364,
        'TestDeck')

    for note in notes:  
        my_deck.add_note(note)

    genanki.Package(my_deck).write_to_file('../output/output.apkg')