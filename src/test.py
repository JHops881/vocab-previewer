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
  ])

my_note = genanki.Note(
  model=my_model,
  fields=["星云", "xīng yún", "nebula", "一些天文学家认为星云是银河系的一部分。", "yìxiē tiānwénxuéjiā rènwéi xīngyún shì yínhéxì de yíbùfèn", "Some astronomers thought nebulae were part of our Milky Way Galaxy."])


my_deck = genanki.Deck(
  1907462364,
  'Country Capitals')

my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file('../output/output.apkg')