import re
# import stopword
# Define a function to clean text using regex for list of list
def clean_text(text_list):
    # convert to lower case
    text_list = text_list.lower()
    # Remove punctuation
    pattern = r'[^\w]+'
    length = len(text_list)
    words = text_list.split()
    for k in range(len(words)):
        words[k] = re.sub(pattern, ' ', words[k])

    # Rejoin words with spaces
    text_list = ' '.join(words)
    # Remove extra whitespace
    text_list = re.sub(r'\s+', ' ', text_list)
    # # Remove numbers
    # text_list = re.sub(r'\d+', '', text_list)

    # print(text_list,"\n")
    import nltk
    from nltk.corpus import stopwords
    # nltk.download('stopwords')  # download the stop words corpus
    stop_words = set(stopwords.words('english'))
    filtered_text = ""
    words = text_list.split()
    for word in words:
        if word.lower() not in stop_words:
            filtered_text += word + ' '   
    return filtered_text

def stopwordremove(text):
    # text1 = text.lower()
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in text if not w in stop_words]
    return filtered_sentence

def stopwordcount(text):
    # import nltk
    # nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    stop_words_count = 0
    words = text.split()
    for word in words:
        if word.lower() in stop_words:
            stop_words_count += 1
    return stop_words_count

def punctuation_count(text_list):
    #regex punctuation count
    import re
    punctuation_count = 0
    words = text_list.split()
    for word in words:
        punctuation_count += len(re.findall(r'[^\w\s]', word))
    return punctuation_count

def word_count(text):
    newl = 0
    newl = len(text.split())
    return newl