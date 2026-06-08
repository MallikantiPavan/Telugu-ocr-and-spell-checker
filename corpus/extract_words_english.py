import re
input_file=r"E:\Nlp_projects\nlp_project_ocr\corpus\english_corpus.txt"
output_file=r"E:\Nlp_projects\nlp_project_ocr\corpus\english_words.txt"
with open(input_file,"r",encoding="utf-8") as f:
    text=f.read()

words=re.findall(r"\b[a-zA-Z]+\b",text)
with open(output_file,"w",encoding="utf-8") as f:
    for word in words:
        f.write(word+"\n")

print(f"Done. {len(words)} words extracted → {output_file}")