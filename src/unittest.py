CEDICT_PATH: str = "../data/cedict.json"

import json 

def segmentate(text: str, lookup_file_path: str, lookup_key: str) -> list[str]:
    
    # 不同意
    # 不同意思
    
    ''' This file contains a json list of dictionary entries. Each one has a key
    at ["lookup_key"]. We want to retrieve this one ket from all of them and store
    in a in a dict so that we can lookup up values faster than iterating through a
    119k obj list.'''
    with open(lookup_file_path, encoding="utf8") as file:
    
        lookup_json: str = file.read()
        # Parse into python onj (dict).
        lookup_table: dict = json.loads(lookup_json)
        
        # The dict that contains all of the keys extracted.
        lookup_map: dict[str] = {}
        
        # Extract the keys from all the entries in the lookup_table.
        for row in lookup_table:
            lookup_map[row[lookup_key]] = None
            
        # This is the text after it is segmented properly.
        segments: list[str] = []
        
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
    



msg = '''
很久很久以来我就梦想着有一只属于自己的狗可是我们住在租来的房子里
而房东又明令禁止我们养狗父亲曾经几次试着和房东商量但都无济于事唉
世上就是有那么一些不好商量的人房东声明其他的房客不希望看见房子里有狗
这简直是胡说八道我认识住在三楼和四楼的人家他们都很想养一只狗事实上
是房东自己不喜欢狗
我爸爸曾说他的问题其实跟狗无关他是因为不喜欢自己所以也不愿意
让别人过得快乐
于是有一天我仔仔细细地观察了一下房东他的长相看上去真的是很粗俗后
来我妈妈又向他提起养狗的事情他竟然给我们寄来了一封挂号信恐吓我们要
我们解除房约!
直到今天我仍然认为没有人有权禁止别人养狗但从能养小动物这一点来看
自己买房子真的是一件非常必要的事情
过了一段时间我爸妈真的买了一栋带花园的房子于是我有了自己的房间
我的感觉真是好极了像生活在天堂一般但我的爸爸妈妈却没有那么快乐了他
们总是愁云满面因为买房的实际费用比原先计划的要高我隐隐约约地听出家
里的钱现在变得报紧张了所以我决定在几周之内先把我的愿望藏在肚子里不对
爸爸妈妈说可是我是真的太渴望有一只属于自己的小狗了
'''
sentence: list[str] = segmentate(msg, CEDICT_PATH, "simplified")
print(sentence)