import txtclean as tc
import clean_text_regex
import cosine
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import yake
import search
import numpy as np
import requests
from bs4 import BeautifulSoup
import PyPDF2
#load the model finalized_model.sav
import joblib
def calculator(paragraph):
    content = tc.clean_text(paragraph)
    word = tc.tokenize_text(content)
    word = tc.stopwordremove(word)
    lem_word=[]
    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()
    for i in word:
        if i.endswith('ed') or i.endswith('ing'):
            lem_word.append(ps.stem(i))
        else:
            lem_word.append(lemmatizer.lemmatize(i))
    word = ' '.join(lem_word)
    # import spacy 
    # nlpl = spacy.load('en_core_web_sm')
    # doc = nlpl(word)
    print("KEYWORD EXTRACTION")
    keyword1 = tc.keywordextract(word)
    keyword2 = tc.monkeyword(word)
    key_extractor = yake.KeywordExtractor()
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.5
    numOfKeywords = 14
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keyword3 = custom_kw_extractor.extract_keywords(word)
    keyword3 = sorted(keyword3, key = lambda x: x[1],reverse=True)
    links=np.array([])
    c = []
    for i in range(len(keyword1)):
        c.append(keyword1[i][0])
    c = ' '.join(c)
    k = search.search(c)
    for i in k:
        links = np.append(links,i['link'])
    c = keyword2
    c = ' '.join(c)
    k = search.search(c)

    for i in k:
        if i['link'] in links:
            continue
        else:
            links = np.append(links,i['link'])
    c = []
    for i in range(len(keyword1)):
        c.append(keyword1[i][0])
    #Join the Keywords
    c = ' '.join(c)
    k = search.search(c)
    for i in k:
        if i['link'] not in links:
            links = np.append(links,i['link'])
    print("IS THAT WEB PAGE IS SCRAPABLE OR NOT")
    scrapable_links = []
    if links is not None:
        for link in links:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type')
                    if content_type.startswith('text/html'):
                        soup = BeautifulSoup(response.content, 'html.parser')
                        if soup is not None:
                            scrapable_links.append(link)
                    elif content_type == 'application/pdf':
                        pdf_file = PyPDF2.PdfFileReader(response.content)
                        if pdf_file.getNumPages() > 0:
                            scrapable_links.append(link)
            except:
                pass
    # print(scrapable_links)
    suspicous_paragraphs = []
    links = scrapable_links
    print("EXTRACTING CONTENT FROM WEB PAGES")
    if links is not None:
        for link in links:
            try:
                response = requests.get(link)
                content_type = response.headers.get('content-type')
                if content_type.startswith('text/html'):
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract the page title from the HTML page
                    title = soup.title.string if soup.title else ''
                    # print(f"Scraping HTML content from {link} - Page title: {title}")
                    # Extract the text from the HTML page
                    text = soup.get_text()
                    suspicous_paragraphs.append(text)
                elif content_type == 'application/pdf':
                    pdf_file = PyPDF2.PdfFileReader(response.content)
                    if pdf_file.getNumPages() > 0:
                        # Extract the text from the PDF file
                        text = ''
                        for i in range(pdf_file.getNumPages()):
                            page = pdf_file.getPage(i)
                            text += page.extractText()
                        suspicous_paragraphs.append(text)
                        # print(f"Scraping PDF content from {link} - Text: {text}")
                else:
                    print(f"Content type not supported for {link}")
            except:
                print(f"Error fetching content from {link}")

    row = []
    temp = []
    preprocessed_suspicious_paragraph=[]
    temp1 = clean_text_regex.stopwordcount(paragraph)
    temp2 = clean_text_regex.punctuation_count(paragraph)
    print("TEXT PREPROCESSING FOR SUSPICIOUS PARAGRAPH")
    #Text Preprocessing
    for i in suspicous_paragraphs:
        #feauture extraction
        #stop word count of original paragraph
        if temp1==0:
            temp.append(0)
        else:
            kpt = clean_text_regex.stopwordcount(i)
            if(temp1<kpt):
                temp.append(temp1/kpt)
            else:
                temp.append(kpt/temp1)
    
        #punctuation count
        
        if temp2==0:
            temp.append(0)
        else:
            kt = clean_text_regex.punctuation_count(i)
            if(temp2<kt):
                temp.append(temp2/kt)
            else:
                temp.append(kt/temp2)
        
        #Step 1: text cleaning -> punctuation removal,special characters and numbers removal
        sus_para = tc.clean_text(i)

        #Step 2: tokenization -> split text to words or tokens
        sus_token = tc.tokenize_text(sus_para)
        # print("CONTENT AFTER STEP 2 TOKENIZE: ",sus_token)

        #Step 3: stop word removal 
        sus_token = tc.stopwordremove(sus_token)

        #Step 5: Stemming and Lemmatization (convert to base using dictionary) -> convert words to root words
        lem_word=[]
        lemmatizer = WordNetLemmatizer()
        ps = PorterStemmer()
        for i in sus_token:
            
            #if sus_token ends with past tense or ing or ed then perform stemming else lemmatization
            if i.endswith('ed') or i.endswith('ing'):
                lem_word.append(ps.stem(i))
            else:
                lem_word.append(lemmatizer.lemmatize(i))

        sus_token = ' '.join(lem_word)
        preprocessed_suspicious_paragraph.append(sus_token)
        # row[i].append(temp)
        row.append(temp)
        temp = []
    j=0
    print("FEATURE EXTRACTION FOR SUSPICIOUS PARAGRAPH")
    for i in preprocessed_suspicious_paragraph:
        #feauture extraction
        
        #text after punctuation removal, stop word removal, numbers removal and extra whitespace removal
        original = clean_text_regex.clean_text(i)

        #word overlap ratio
        # row[j].append(wordoverlapratio.word_overlap_ratio(original,word))

        #cosine similarity
        row[j].append(cosine.cosine_similarity(original,word))

        # #jaccard similarity
        # row[j].append(jaccard.jaccard_similarity(original,word))

        # #euclidean distance
        # row[j].append(euclidean_distance.euclidean(original,word))

        # #Leshtein Distance
        # row[j].append(levenshtein.levenshtein_distance(original,word))
        j+=1
    print("PREDICTING THE OUTPUT")
    # #joblib load model
    # loaded_model = joblib.load('finalized_model.sav')
    # result = []
    # #use the model to predict the output
    # for i in row:
    #     inp = [i]
    #     #convert predicted output from numpy array to int
    #     result.append(int(loaded_model.predict(inp)))
    result = []
    for i in range(len(row)):
        result.append(row[i][2]*100)

    dict = {}
    if result is not None:
        for i in range(len(links)):
            dict[links[i]] = result[i]
    else:
        return sorted_dict
    #sort the dictionary in descending order
    sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    #take only top 3
    if(len(sorted_dict)>3):
        sorted_dict = sorted_dict[:3]
    return sorted_dict