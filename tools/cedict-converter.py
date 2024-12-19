import decode_pinyin as dc
import json

def parse_line(line: str) -> dict:
    
    word_definition_data = {}
    
    if line == '' or len(line) <= 1 or line[0] == "#":
        return None
    
    line = line.rstrip('/').split('/')
    
    english: list[str] = line[1:]
    char_and_pinyin = line[0].split('[')
    
    characters: list[str] = char_and_pinyin[0].split()
    
    traditional = characters[0]
    simplified = characters[1]
    
    raw_pinyin: list[str] = char_and_pinyin[1].rstrip().rstrip("]").split()
    proper_pinyin: list[str] = []
    for unit in raw_pinyin:
        proper_pinyin.append(dc.decode_pinyin(unit))
    pinyin = " ".join(proper_pinyin)
    
    word_definition_data['traditional'] = traditional
    word_definition_data['simplified'] = simplified
    word_definition_data['pinyin'] = pinyin
    word_definition_data['english'] = english
    
    return word_definition_data

lines: list[str] = []
with open('./cedict_ts.u8', encoding="utf8") as file:
    text: str = file.read()
    lines = text.split('\n')

all_data: list[dict[str]] = []

print("Parsing dictionary . . .")
for line in lines:
    word_definiation_data: dict[str] = parse_line(line)
    if word_definiation_data:
        all_data.append(word_definiation_data)
        

#remove entries for surnames from the data:
print("Removing Surnames . . .")
for i in range(len(all_data)-1, -1, -1):
    if "surname " in all_data[i]['english']:
        if all_data[i]['traditional'] == all_data[i+1]['traditional']:
            all_data.pop(i)
            
print('Done!')

json_data: str = json.dumps(all_data, ensure_ascii=False, indent=4)

with open("./cedict.json", "w", encoding="utf8") as f:
    f.write(json_data)