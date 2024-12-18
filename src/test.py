from bs4 import BeautifulSoup
import requests
import time

def get_example_sentence(word_block: str) -> dict:
    """Use web scraping to retrieve a mandarin definition, pinyin, and example sentence
        with meainging from a mandarin word.

    Args:
        word (str): Mandarin word.

    Returns:
        dict: Mandarin example sentence that uses the word.
    """
    
    url: str = f"https://www.purpleculture.net/dictionary-details/?word={word_block}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
    }   
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        
        html_content = response.text

        # Full parsed HTML ready to by used
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Here's a laundry list of what we want from the page:
        #   - the word
        #   - the word's pinyin pronounciation
        #   - the word's english meaning
        #   - an example sentence
        #   - the example sentence's meaning in english
        
        word:    str = ""
        pinyin:  str = ""
        meaning: str = ""
        
        example_sentence:         str = ""
        example_sentence_meaning: str = ""
        
        # This element contains the word and it's pinyin.
        word_block = soup.find("ruby", class_="mainsc")
        
        # Step 1: Extract the word.
        word_block_hanzi_elements = word_block.find_all("a", recursive=False)
        for element in word_block_hanzi_elements:
            word += element.text.strip()
        
        # Step 2: Extract the pinyin.
        word_block_pinyin_elements = word_block.find_all("rt")
        for element in word_block_pinyin_elements:
            pinyin += element.text.strip()

        # Step 3: Extract the meaning.
        meaning = soup.find("div", class_="en py-2").text.strip()
        
        # Step 4. Extract the Example sentence
        example_sentence_hanzi_elements = soup.find(id="sen1").find_all("span", class_="cnchar")
        example_sentence_hanzi: str = ""
        for element in example_sentence_hanzi_elements:
            example_sentence += element.text.strip()
        
        
        print(word)
        print(pinyin)
        print(meaning)
        print(example_sentence)
        
        
        # Print Pinyin
        
        # Print Sentence English Meaning
    else:
        print("Failed to retrieve the webpage:", response.status_code)
    
    

get_example_sentence("流行")
