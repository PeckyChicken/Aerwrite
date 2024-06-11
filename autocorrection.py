import Wordy
import autocorrect

CorrectWord = autocorrect.Speller()

def correct(word):
    return CorrectWord(word)

def complete(word):
    return sorted(Wordy.find_words(start=word),key=len)