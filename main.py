import PySimpleGUI as sg
import os
from PIL import Image
import sys
import pyocr
import pyocr.builders
import re


def processImage(i):
    img = Image.open(i)
    new_size = tuple(6*x for x in img.size)
    img = img.resize(new_size, Image.ANTIALIAS).convert('L')
    txt = tool.image_to_string(
        img, lang=lang, builder=pyocr.builders.TextBuilder())
    lines = txt.split("\n")
    counter = 0
    results = []
    for line in lines:
        match = re.findall(r"\d+", line)
        if len(match) == 1:
            results.append([int(match[0]), 0])
        elif len(match) == 2:
            results.append([int(match[0]), int(match[1])])
    return results


def processAll(files):
    result = []
    for i in files:
        result = result + processImage(i)
    return result


def printResults(result, avgElement, activate):
    print("Average elemental damage is +",
          (sum(avgElement)/len(avgElement))-1, "%")
    print("Average activation rate is", (activate/len(result))*100, "%")


def filterElement(result):
    avgElement = []
    activate = 0
    for num in result:
        if num[1] != 0:
            damage = num[0]/(num[0] - num[1])
            avgElement.append(damage)
            activate = activate + 1
    return avgElement, activate


def writeToFile(result):
    with open('output.txt', 'w') as f:
        for i in result:
            f.write(str(i[0])+" "+str(i[1])+"\n")


sg.theme("DarkAmber")
tools = pyocr.get_available_tools()
tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]
layout = [
    [sg.Text('Enter Files')],
    [sg.Input(key='_FILES_'), sg.FilesBrowse(
        file_types=(("jpeg", "*.jpg"), ("All Files", "*"),))],
    [sg.Output(size=(80, 5))],
    [sg.Button('ok'), sg.Button('cancel')]
]
window = sg.Window('Window Title', layout)
while True:
    event, values = window.read()
    if event in (None, 'cancel'):
        break
    elif event in ("ok"):
        files = values['_FILES_'].split(";")
        result = processAll(files)
        avgElement, activate = filterElement(result)
        writeToFile(result)
        printResults(result, avgElement, activate)
        window.Refresh()
window.close()
