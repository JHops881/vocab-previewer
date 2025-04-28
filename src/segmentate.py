import json

def segmentate(text: str, lookup_file_path: str, lookup_key: str) -> list[str]:
    """
    Uses a custom algorithm to break text into dictionary words verified by a 
    local dictionary. Words are returned on a best-guess basis -meaning some 
    three character strings (e.g. 不同意) will/may return two words (同意, 不同)
    because the algorithm is unable to derive contextual meaning.

    Args:
        text (str): The text to segmentate into dictionary words.
        lookup_file_path (str): path to a (table-like) json file that contains
            the dictionary entries to check against.
        lookup_key: (str): The json key under which the word is stored in each 
            dictionary entry. 

    Returns:
        list: A list of all dictionary words identified from the text, mostly in
            order, and also containing repeats.     
    """
    
    # 不同意
    # 不同意思
    # TODO: fix these situations
    
    ''' This file contains a json list of dictionary entries. Each one has a key
    value pair with the key "lookup_key". We want to retrieve the value from all
    of them and store in a in a dict so that we can lookup up values faster than
    iterating through a potentially 119k obj list.'''
    with open(lookup_file_path, encoding="utf8") as file:
    
        lookup_json_dumped: str = file.read()

        # Parse into python obj (dict).
        lookup_json_loaded: dict = json.loads(lookup_json_dumped)
        
        # Let's create our map that is going to store all of the lookup_key values
        lookup_map: dict[str] = {}
        
        # Extract the values from all the entries in the lookup_json_loaded.
        for row in lookup_json_loaded:
            lookup_map[row[lookup_key]] = None
            
        # This will contain the words after it is segmented properly.
        segments: list[str] = []
        
        # Custom algo.. how do I begin to explain. TODO: document.
        def worder(index: int, text: str, seg: str, map: dict, depth: int) -> any:
            if seg + text[index+1] in map:
                return worder(index+1, text, seg+text[index+1], map, depth+1)
            else:
                return seg, depth
        
        # algo v1.0
        is_child: bool = False
        for i, char in enumerate(text):
            
            # is it real?
            if char in lookup_map:
                
                (segment, depth) = worder(i, text, char, lookup_map, 0)
                
                if not is_child or (is_child and depth > 0):
                    segments.append(segment)

                    
                is_child = depth
                    
            # No, Okay we'll deal with this later.
            else:
                pass
        
        return segments