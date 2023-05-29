import collections
import config
import re

tabWidth = config.tabWidth
lineHeight = config.lineHeight

weirdChar = { # weird characters generated by Symbol Scraper that need to be replaced
    "\u2212": "-",  # long dash
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "fraction(-)": "",  # weird output of SymbolScraper
    "\u25a0": "",
}

# given a string or an array of strings, add the word to the end of the string
def updateText(inputObject, word):
    if not inputObject:
        return word
    elif isinstance(inputObject, str):
        # don't join with space if inputObject ends with a hyphen
        if inputObject and inputObject[-1] == "-":
            inputObject += word
        else:
            inputObject += " " + word
    else:
        # don't join with space if the last inputObject ends with a hyphen
        if inputObject and inputObject[-1] and inputObject[-1][-1] == "-":
            inputObject[-1] += word
        else:
            inputObject[-1] += " " + word
    return inputObject

# given an word xml element, return the word as a string
def buildWord(wordXml):
    wordBuf = ""
    for char in wordXml.iter("Char"):
        wordBuf += (
            weirdChar[str(char.text)] if char.text in weirdChar else str(char.text)
        )
    return wordBuf

# def checkSideLine(lineXml):
#     location = lineXml.attrib["BBOX"].split(" ")[0]
#     return location in ["9.0", "18.0"]


# def checkIgnoredPrefix(line):
#     for prefix in ignoredSuffix:
#         if line.startswith(prefix):
#             return True
#     return False

# find the two most common line start positions
def findOffset(root):
    lineStartPos = collections.defaultdict(int)
    for lineXml in root.iter("Line"):
        location = round(float(lineXml.attrib["BBOX"].split(" ")[0]))
        lineStartPos[location] += 1
    twoMean = sorted(lineStartPos.items(), key=lambda x: x[1], reverse=True)[:2]
    res = [twoMean[0][0], twoMean[1][0]]
    return res

# given a line xml element, check if it is the start of a paragraph
def checkStartParagrph(lineXmlBBOX, paragraphStart):
    startX = float(lineXmlBBOX.split(" ")[0])
    return roughEqual(startX-tabWidth, paragraphStart[0], 5) or roughEqual(startX-tabWidth, paragraphStart[1], 5)

# given a line of text, check if it is the end of a paragraph
# logic is done by checking if the page starts rendering graphs
def checkEndOfPage(text):
    text = text.lower()
    if re.match("^(scheme|table|figure) [1-9]. ", text):
        return True
    else:
        return False

# check if the start of two lines are very far from each other
def checkLinesFar(line1BBOX, line2BBOX):
    threshold = 20
    xMin1, yMin1 = line1BBOX.split(" ")[0], line1BBOX.split(" ")[1]
    xMin2, yMin2 = line2BBOX.split(" ")[0], line2BBOX.split(" ")[1]
    return abs(float(xMin1) - float(xMin2)) > threshold or abs(float(yMin1) - float(yMin2)) > threshold

# check if two lines start at the same x position
def checkSameStartX(line1BBOX, line2BBOX):
    xMin1, yMin1 = line1BBOX.split(" ")[0], line1BBOX.split(" ")[1]
    xMin2, yMin2 = line2BBOX.split(" ")[0], line2BBOX.split(" ")[1]
    return roughEqual(float(xMin1), float(xMin2), 5)

# check if new paragraph based on current line and previous line
def checkNewParagraph(currLineBBOX, prevLineBBOX, offsets):
    if not prevLineBBOX:
        return True
    xMinCurr, yMinCurr, xMaxCurr, yMaxCurr = currLineBBOX.split(" ")
    xMinPrev, yMinPrev, xMaxPrev, yMaxPrev = prevLineBBOX.split(" ")
    # convert to float
    xMinCurr, yMinCurr, xMaxCurr, yMaxCurr = float(xMinCurr), float(yMinCurr), float(xMaxCurr), float(yMaxCurr)
    xMinPrev, yMinPrev, xMaxPrev, yMaxPrev = float(xMinPrev), float(yMinPrev), float(xMaxPrev), float(yMaxPrev)
    # not a new paragraph if the current line is the same as the previous line
    if checkSameLine(currLineBBOX, prevLineBBOX):
        return False
    elif checkSameStartX(currLineBBOX, prevLineBBOX) and not checkLinesFar(currLineBBOX, prevLineBBOX):
        return False
    # if the current line is indented and the previous line is not
    if xMinCurr > xMinPrev and roughEqual(xMinCurr-xMinPrev, tabWidth, 5) and roughEqual(yMinCurr - yMinPrev, lineHeight, 5):
        return True
    # if the current line far from the previous line, and the two lines are not in two columns
    elif checkLinesFar(currLineBBOX, prevLineBBOX) and not (roughEqual(xMinCurr, max(offsets), 10) and roughEqual(xMinPrev, min(offsets), 10)):
        return True
    elif checkStartParagrph(currLineBBOX, offsets):
        return True
    else:
        return False

# check if two line xml elements are on the same line
def checkSameLine(line1BBOX, line2BBOX):
    if not line1BBOX or not line2BBOX:
        return False
    y1 = float(line1BBOX.split(" ")[1])
    y2 = float(line2BBOX.split(" ")[1])
    return roughEqual(y1, y2, 5) # line spacing is around 10, so using a threshold of something less than 10

# combine two lines of text with the same y coordinate
def combineLines(line1BBOX, line2BBOX):
    xMin1, yMin1, xMax1, yMax1 = line1BBOX.split(" ")
    xMin2, yMin2, xMax2, yMax2 = line2BBOX.split(" ")
    xMin = min(float(xMin1), float(xMin2))
    xMax = max(float(xMax1), float(xMax2))
    # recreate the bbox string
    bbox = str(xMin) + " " + str(yMin1) + " " + str(xMax) + " " + str(yMax1)
    return bbox

# check if two numbers are roughly equal
def roughEqual(a, b, threshold):
    return abs(a - b) < threshold