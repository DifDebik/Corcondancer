import spacy
import pandas as pd
import re
from spacy.matcher import PhraseMatcher
from termcolor import colored




def highlight_word(sentence, word):
    return sentence.replace(word, colored(word,'grey','on_red'))
def remove_words_right(sen, wr):
    return sen[:sen.find(wr)]
def remove_words_left(sent, wrd):
    a = sent[sent.find(wrd):]
    return a.replace(wrd,'',1)


nlp = spacy.load('ru_core_news_lg', exclude=["parser"])
config = {"punct_chars": ['!', '.', '?','\n']}
nlp.add_pipe("sentencizer", config=config)

matcher = PhraseMatcher(nlp.vocab, attr = 'LEMMA')
terms = open('C:/Users/user/Desktop/2 класс/математика_готово/mathdict11737.txt', encoding='utf-8').read().splitlines()
patterns = [nlp(text) for text in terms]
matcher.add("TerminologyList", patterns)

doc = nlp(open('C:/Users/user/Desktop/2 класс/математика_готово/Tbook(P)_R_Mt_02_02_Pe_0_A_0_2019_11737.txt', 'r', encoding='utf-8').read())
matches = matcher(doc)
concdict = {}

for match_id, start, end in matches:
    span = doc[start:end]
    a = {span.text: span.sent.text}
    for k, v in a.items():                 
        concdict.setdefault(k, []).append(v)

concdict = {key: list(set(value)) for key, value in concdict.items()}

for key, value in sorted(concdict.items(), key=lambda i: i[0].lower()):
    print(key + ': ')
    for i in value:
        print(re.sub(r'(\n\s*)+\n', '\n', highlight_word(i, key)+'\n'))


l = []
k = []
r = []

for key, value in sorted(concdict.items(), key=lambda i: i[0].lower()):
    for i in value:
        l.append(re.sub(r"\s+", " ", remove_words_right(i, key).strip('\n')))
        r.append(re.sub(r"\s+", " ", remove_words_left(i, key).strip('\n')))
        k.append(key)

data = {'left context': l, 'key word': k, 'right context': r}
df = pd.DataFrame(data)
df.to_excel(r'C:\Users\user\Desktop\Конк_Мат_11737.xlsx', index = False)
