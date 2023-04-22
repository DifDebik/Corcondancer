import spacy
from tabulate import tabulate

def find_concordance(text, lemma):
    nlp = spacy.load('ru_core_news_lg')
    doc = nlp(text)
    concordance = []

    for token in doc:
        if token.lemma_.lower() == lemma.lower():
            left_context = ' '.join([t.text for t in token.sent if t.i < token.i])
            right_context = ' '.join([t.text for t in token.sent if t.i > token.i])
            concordance.append([left_context, token.text, right_context])
    return concordance

# Example usage
text = "В лингвистике термин «текст» используется в широком значении, включая и образцы устной речи. Восприятие текста изучается в рамках лингвистики текста и психолингвистики. Так, например, И. Р. Гальперин определяет текст следующим образом: «Это письменное сообщение, объективированное в виде письменного документа, состоящее из ряда высказываний, объединённых разными типами лексической, грамматической и логической связи, имеющее определённый моральный характер, прагматическую установку и соответственно литературно обработанное»."
lemma = "образец"

concordance = find_concordance(text, lemma)
print("Concordance for lemma '{}':".format(lemma))
print(tabulate(concordance, headers=["Left Context", "Instance", "Right Context"]))
