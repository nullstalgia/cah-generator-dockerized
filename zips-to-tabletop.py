#!/usr/bin/python3

import argparse
import json
import os
import zipfile
import shutil
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("decks_path", help="path of deck zips")
args = parser.parse_args()
print(args.decks_path)

onlyfiles = sorted([f for f in os.listdir(args.decks_path) if os.path.isfile(os.path.join(args.decks_path, f))])

#new_per_card_size = "406x560"
pre_sheet_size_w = 32880
pre_sheet_size_h = 31416
new_sheet_size_w = 4096
new_sheet_size_h = 3914
new_card_size_w = 3001
new_card_size_h = 4096

def make_whites(pngs, iteration=0):
    whites = args.decks_path+"white/"
    #command = "montage -depth 2 -limit area 8192 -limit memory 8192 -quality 100 -mode concatenate -tile 10x7 -fill white "
    png_load = pngs
    if len(png_load) == 1:
        with Image.open(whites+png_load[0]) as card:
            card = card.resize((new_card_size_w, new_card_size_h))
            card.save(args.decks_path+"white-"+str(iteration)+"-1.png")
        return
    if len(pngs) > 69:
        #for i in range(69):
        png_load = pngs[0:69]
        png_offload = pngs[69:]
        make_whites(png_offload,iteration+1)
    im = Image.new("RGB", size=(pre_sheet_size_w,pre_sheet_size_h))
    
    # fill white
    im.paste( (255,255,255), [0,0,im.size[0],im.size[1]])

    column = 0
    row = 0
    for png in png_load:
        with Image.open(whites+png) as card:
            im.paste(card, (card.size[0]*column,card.size[1]*row))
            column+=1
            if column == 10:
                column = 0
                row+=1
    column = 9
    row = 6  
    with Image.open("tts/back-white.png") as card:
            im.paste(card, (card.size[0]*column,card.size[1]*row))

    im = im.resize((new_sheet_size_w,new_sheet_size_h))
    im.save(args.decks_path+"white-"+str(iteration)+"-"+str(len(png_load))+".png")

def make_blacks(pngs, iteration=0):
    blacks = args.decks_path+"black/"
    #command = "montage -depth 2 -limit area 8192 -limit memory 8192 -quality 100 -mode concatenate -tile 10x7 -fill white "
    png_load = pngs
    if len(png_load) == 1:
        with Image.open(blacks+png_load[0]) as card:
            card = card.resize((new_card_size_w, new_card_size_h))
            card.save(args.decks_path+"black-"+str(iteration)+"-1.png")
        return
    if len(pngs) > 69:
        #for i in range(69):
        png_load = pngs[0:69]
        png_offload = pngs[69:]
        make_blacks(png_offload,iteration+1)
    im = Image.new("RGB", size=(pre_sheet_size_w,pre_sheet_size_h))
    
    # fill black, just in case
    im.paste( (0,0,0), [0,0,im.size[0],im.size[1]])

    column = 0
    row = 0
    for png in png_load:
        with Image.open(blacks+png) as card:
            im.paste(card, (card.size[0]*column,card.size[1]*row))
            column+=1
            if column == 10:
                column = 0
                row+=1
    column = 9
    row = 6  
    with Image.open("tts/back-black.png") as card:
            im.paste(card, (card.size[0]*column,card.size[1]*row))

    im = im.resize((new_sheet_size_w,new_sheet_size_h))
    im.save(args.decks_path+"black-"+str(iteration)+"-"+str(len(png_load))+".png")
args.decks_path+="/"
for zip in onlyfiles:
    whites = args.decks_path+"white/"
    blacks = args.decks_path+"black/"
    srcs = args.decks_path+"src/"
    zippath = args.decks_path+"/"+zip
    
    if zip[-3:] == "zip" and zip[:5] == "deck_":
        print(zip)
        os.system("rm "+args.decks_path+"/white-*")
        os.system("rm "+args.decks_path+"/black-*")
        if os.path.exists(whites):
            shutil.rmtree(whites)
        if os.path.exists(blacks):
            shutil.rmtree(blacks)
        if os.path.exists(srcs):
            shutil.rmtree(srcs)
        with zipfile.ZipFile(zippath, 'r') as zip_ref:
            zip_ref.extractall(args.decks_path)
        pngs = sorted([f for f in os.listdir(whites) if os.path.isfile(os.path.join(whites, f))])
        print("Generating Whites")
        make_whites(pngs)
        pngs = sorted([f for f in os.listdir(blacks) if os.path.isfile(os.path.join(blacks, f))])
        print("Generating Blacks")
        make_blacks(pngs)
        deckname = ""
        with open(srcs+'info.txt') as info_file:
            info = info_file.readlines()
            data = []
            for line in info:
                data.append(line.strip())
            deckname = data[8].split('=')[1].strip()
        deckname = "".join( x for x in deckname if (x.isalnum() or x in "._- "))
        if os.path.exists(args.decks_path+"/"+deckname):
            shutil.rmtree(args.decks_path+"/"+deckname)
        os.mkdir(args.decks_path+"/"+deckname)
        for deck in sorted([f for f in os.listdir(args.decks_path) if os.path.isfile(os.path.join(args.decks_path, f))]):
            if deck[-4:] == ".png" and (deck[:5] == "white" or deck[:5] == "black"):
                shutil.move(args.decks_path+deck, args.decks_path+"/"+deckname)
        #os.remove(zippath)
        shutil.move(zippath, args.decks_path+"/"+deckname+".zip")
if os.path.exists(whites):
    shutil.rmtree(whites)
if os.path.exists(blacks):
    shutil.rmtree(blacks)
if os.path.exists(srcs):
    shutil.rmtree(srcs)