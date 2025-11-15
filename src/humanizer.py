"""
Text humanization module.
Transforms AI-generated text to appear more human-like using NLP techniques.
"""
import nltk
import re
import random
import spacy
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

# Download NLTK resources (only once)
try:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)  # Newer NLTK versions require this
    nltk.download("wordnet", quiet=True)
except:
    pass  # Already downloaded

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download if not available
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Contraction expansion map
CONTRACTION_MAP = {
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'ll": " will",
    "'ve": " have",
    "'d": " would",
    "'m": " am"
}

# Academic transition phrases
ACADEMIC_TRANSITIONS = [
    "Moreover,",
    "Additionally,",
    "Furthermore,",
    "Hence,",
    "Therefore,",
    "Consequently,",
    "Nonetheless,",
    "Nevertheless,",
    "In contrast,",
    "On the other hand,",
    "In addition,",
    "As a result,",
]


def expand_contractions(sentence: str) -> str:
    """Turn contractions into full forms: can't -> can not, I'm -> I am, etc."""
    tokens = word_tokenize(sentence)
    expanded = []
    for t in tokens:
        replaced = False
        lower_t = t.lower()
        for contr, expansion in CONTRACTION_MAP.items():
            if contr in lower_t and lower_t.endswith(contr):
                new_t = lower_t.replace(contr, expansion)
                # Preserve capitalization of first letter
                if t[0].isupper():
                    new_t = new_t.capitalize()
                expanded.append(new_t)
                replaced = True
                break
        if not replaced:
            expanded.append(t)
    return " ".join(expanded)


def get_synonyms(word: str, pos: str):
    """Get WordNet synonyms for a word with a given POS (spaCy tag)."""
    wn_pos = None
    if pos.startswith("ADJ"):
        wn_pos = wordnet.ADJ
    elif pos.startswith("NOUN"):
        wn_pos = wordnet.NOUN
    elif pos.startswith("ADV"):
        wn_pos = wordnet.ADV
    elif pos.startswith("VERB"):
        wn_pos = wordnet.VERB
    
    synonyms = set()
    if wn_pos:
        for syn in wordnet.synsets(word, pos=wn_pos):
            for lemma in syn.lemmas():
                lemma_name = lemma.name().replace("_", " ")
                if lemma_name.lower() != word.lower():
                    synonyms.add(lemma_name)
    return list(synonyms)


def replace_synonyms(sentence: str, p_syn: float = 0.2) -> str:
    """
    Replace some content words (adj, noun, verb, adv) with WordNet synonyms
    with probability p_syn per token.
    """
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    for token in doc:
        if token.pos_ in ["ADJ", "NOUN", "VERB", "ADV"] and wordnet.synsets(token.text):
            if random.random() < p_syn:
                synonyms = get_synonyms(token.text, token.pos_)
                if synonyms:
                    new_tokens.append(random.choice(synonyms))
                else:
                    new_tokens.append(token.text)
            else:
                new_tokens.append(token.text)
        else:
            new_tokens.append(token.text)
    return " ".join(new_tokens)


def add_academic_transition(sentence: str, p_transition: float = 0.2) -> str:
    """
    Prepend an academic transition phrase with probability p_transition.
    """
    sentence = sentence.strip()
    if not sentence:
        return sentence
    
    if random.random() < p_transition:
        transition = random.choice(ACADEMIC_TRANSITIONS)
        return f"{transition} {sentence}"
    return sentence


def minimal_humanize_line(line: str, p_syn: float = 0.2, p_trans: float = 0.2) -> str:
    """Apply humanization transformations to a single line."""
    line = expand_contractions(line)
    line = replace_synonyms(line, p_syn=p_syn)
    line = add_academic_transition(line, p_transition=p_trans)
    return line


def minimal_rewriting(text: str, p_syn: float = 0.2, p_trans: float = 0.2) -> str:
    """Apply humanization to all sentences in the text."""
    sentences = sent_tokenize(text)
    out_sentences = [
        minimal_humanize_line(s, p_syn=p_syn, p_trans=p_trans) for s in sentences
    ]
    return " ".join(out_sentences)


def humanize_text(text: str, p_syn: float = 1.0, p_trans: float = 1.0) -> str:
    """
    Humanize an AI-generated passage.
    
    Args:
        text (str): The text to humanize
        p_syn (float): Synonym replacement probability (0.0-1.0)
        p_trans (float): Academic transition frequency (0.0-1.0)
    
    Returns:
        str: Humanized text
    """
    # Clamp values to [0,1]
    p_syn = max(0.0, min(1.0, p_syn))
    p_trans = max(0.0, min(1.0, p_trans))
    
    rewritten = minimal_rewriting(text, p_syn=p_syn, p_trans=p_trans)
    
    # Normalize spaces around punctuation
    rewritten = re.sub(r"\s+([.,;:!?])", r"\1", rewritten)
    rewritten = re.sub(r"(\()\s+", r"\1", rewritten)
    rewritten = re.sub(r"\s+(\))", r")", rewritten)
    
    return rewritten

