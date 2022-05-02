#!/usr/bin/python3

import argparse
import json
import os
from sys import prefix
from tokenize import String

# https://stackoverflow.com/questions/761824/python-how-to-convert-markdown-formatted-text-to-text
from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)

parser = argparse.ArgumentParser()
parser.add_argument("json_filename", help="display a square of a given number")
parser.add_argument("--usename", help="write deck's name on cards instead of 'Cards Against Humanity'")
args = parser.parse_args()
print(args.json_filename)

data = None

cards_path = "cards/"

with open(args.json_filename, 'r') as json_file:
    data = json.load(json_file)
    #print(data)

if not os.path.exists(cards_path):
    os.mkdir(cards_path)

count = 0

for deck in data:
    #print(deck)
    deckname = deck["name"]
    # make deck name legal
    clean_deckname = "".join( x for x in deckname if (x.isalnum() or x in "._- "))
    count+=1
    deckpath = cards_path+"deck_"+str(count)
    #deckpath = cards_path+clean_deckname
    if not os.path.exists(deckpath):
        os.mkdir(deckpath)
    with open(deckpath+"/white.txt", 'w') as file:
        for card in deck["white"]:
            text = card["text"]
            #text = unmark(text)
            text = text.replace("\"","\\\"")
            text = text.replace("\n","\\n")
            text = text.replace("$","\\$")
            file.write(text+"\n")
    with open(deckpath+"/black.txt", 'w') as file:
        for card in deck["black"]:
            text = card["text"]
            #text = unmark(text)
            text = text.replace("\"","\\\"")
            text = text.replace("\n","\\n")
            text = text.replace("$","\\$")
            text = text.replace("_","________")
            prefix = ""
            if card["pick"] == 2:
                prefix = "[[2]]"
            elif card["pick"] == 3:
                prefix = "[[3]]"
            file.write(prefix+text+"\n")
            #print(card)
    with open(deckpath+"/info.txt", 'w') as file:
        name = "Cards Against Humanity"
        if args.usename:
            name = deck["name"]
        file.write("name = "+name+"\n")
        file.write("short_name = CAH\n")
        file.write("real_name = "+deck["name"]+"\n")
        file.write("version = 1\n")
        file.write("custom_img_1 = bean.png\n")
        file.write("custom_img_2 = bean.png\n")
        file.write("custom_img_3 = bean.png\n")
        file.write("custom_img_4 = bean.png\n")
        file.write("custom_img_5 = bean.png\n")
    print(clean_deckname)