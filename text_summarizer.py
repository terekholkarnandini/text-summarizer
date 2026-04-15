import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# =========================
# Run these ONCE, then you can comment them out
# =========================
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# =========================
# INPUT TEXT
# =========================
text = """
Artificial Intelligence is the simulation of human intelligence by machines.
It enables computers to learn from experience.
AI is used in healthcare, education, and transportation.
It helps automate tasks and improve efficiency.
Artificial Intelligence improves decision making.
"""

# =========================
# STEP 1: Sentence Tokenization
# =========================
sentences = sent_tokenize(text)

# =========================
# STEP 2: Word Tokenization
# =========================
words = word_tokenize(text.lower())

# =========================
# STEP 3: Stopword Removal
# =========================
stop_words = set(stopwords.words("english"))

filtered_words = []
for word in words:
    if word.isalnum() and word not in stop_words:
        filtered_words.append(word)

# =========================
# STEP 4: Word Frequency
# =========================
word_frequency = {}
for word in filtered_words:
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

# =========================
# STEP 5: Sentence Scoring
# =========================
sentence_scores = {}
for sentence in sentences:
    for word in word_tokenize(sentence.lower()):
        if word in word_frequency:
            if sentence in sentence_scores:
                sentence_scores[sentence] += word_frequency[word]
            else:
                sentence_scores[sentence] = word_frequency[word]

# =========================
# STEP 6: Generate Summary
# =========================
summary_sentences = sorted(
    sentence_scores,
    key=sentence_scores.get,
    reverse=True
)[:2]   # top 2 sentences

summary = " ".join(summary_sentences)

# =========================
# OUTPUT
# =========================
print("ORIGINAL TEXT:\n")
print(text)

print("\nSUMMARY:\n")
print(summary)
