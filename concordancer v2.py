import spacy
import pandas as pd
from string import punctuation

punc = set(punctuation)

def find_concordance(text, lemmas):
    nlp = spacy.load('ru_core_news_lg')
    doc = nlp(text)
    concordance = []

    for token in doc:
        if token.lemma_.lower() in lemmas:
            left_context = [t.text for t in token.sent if t.i < token.i]
            left_context2 = ''.join(w if set(w) <= punc else ' '+w for w in left_context).lstrip().replace('« ', '«').replace(' »', '»')
            right_context = [t.text for t in token.sent if t.i > token.i]
            right_context2 = ''.join(w if set(w) <= punc else ' '+w for w in right_context).lstrip().replace('« ', '«').replace(' »', '»')
            
            concordance.append([left_context2, token.text, right_context2])
    return concordance

# Example usage
text = "В лингвистике термин «текст» используется в широком значении, включая и образцы устной речи. Восприятие текста изучается в рамках лингвистики текста и психолингвистики. Так, например, И. Р. Гальперин определяет текст следующим образом: «Это письменное сообщение, объективированное в виде письменного документа, состоящее из ряда высказываний, объединённых разными типами лексической, грамматической и логической связи, имеющее определённый моральный характер, прагматическую установку и соответственно литературно обработанное»."
lemmas = ["лингвистика", "значение", 'определять']

concordance = find_concordance(text, lemmas)

# Convert concordance results to a DataFrame
df = pd.DataFrame(concordance, columns=["Left Context", "Instance", "Right Context"])

# Save DataFrame to Excel
output_file = "concordance_results.xlsx"
df.to_excel(output_file, index=False)
print("Concordance results saved to '{}'".format(output_file))
