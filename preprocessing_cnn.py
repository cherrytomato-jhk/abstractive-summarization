"""
아래 튜토리얼을 모델에 맞게 수정한 코드입니다.
https://machinelearningmastery.com/prepare-news-articles-text-summarization/

데이터는 https://cs.nyu.edu/~kcho/DMQA/ 에서 다운받을 수 있습니다.
"""

from os import listdir
import string
import pandas as pd
import re

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, encoding='utf-8')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# split a document into news story and highlights
def split_story(doc):
    # find first highlight
    index = doc.find('@highlight')
    # split into story and highlights
    story, highlights = doc[:index], doc[index:].split('@highlight')
    # strip extra white space around each highlight
    highlights = [h.strip() for h in highlights if len(h) > 0]
    return story, highlights

# load all stories in a directory
def load_stories(directory):
    stories = list()
    for name in listdir(directory):
        filename = directory + '/' + name
        # load document
        doc = load_doc(filename)
        # split into story and highlights
        story, highlights = split_story(doc)
        # store
        stories.append({'story':story, 'highlights':highlights})
    return stories

# clean a list of lines
def clean_lines(lines, is_highlight):
    cleaned = list()
    for line in lines:
        # strip source cnn office if it exists
        index = line.find('(CNN) -- ')
        if index > -1:
            line = line[index+len('(CNN) -- '):]
        line = re.sub('^\(CNN\)', '', line)
        # tokenize on white space
        line = line.split()
        # store as string
        cleaned.append(' '.join(line))

    # remove empty strings
    cleaned = [c for c in cleaned if len(c) > 0]
    
    # change to string
    if is_highlight = 0:
        cleaned = ''.join(cleaned)
    else:
        cleaned = '.'.join(cleaned) 
    return cleaned

# CNN - load stories
directory = 'cnn_dm_dataset/cnn/stories/'
cnn_stories = load_stories(directory)
print('Loaded Stories %d' % len(cnn_stories))

for story in cnn_stories:
    story['story'] = clean_lines(story['story'].split('\n'), 0)
    story['highlights'] = clean_lines(story['highlights'], 1)

df = pd.DataFrame(data = cnn_stories)
print(df.describe())
df.to_csv('cnn_stories.csv', index=False)
