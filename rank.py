#!/usr/bin/python
#matt garrett
#cse 417

import sys
from sys import stdout
from math import sqrt
from math import pow

class Document:
    """Represents an HTML document"""
    def __init__(self, url):
        self.url = url
        self.outbound = []
        self.inbound = []
        self.hub = 1
        self.auth = 1

def dumpDocuments(documents):
    for doc in documents:
        print documents[doc].url
        print "OUTBOUND:"
        for link in documents[doc].outbound:
            print "   " + documents[link.url].url
        print "INBOUND:"
        for link in documents[doc].inbound:
            print "   " + documents[link.url].url
        print
    print "number of documents = " + str(len(documents))

def processDocuments(documents, inputFileName):
    print("reading from input file...")
    inputFile = open(inputFileName, "r")
    for line in inputFile:
        if line.find("   ") != 0:
            documents[line[:-2]] = (Document(line[:-2]))

    inputFile = open(inputFileName, "r")
    for line in inputFile:
        if line.find("   ") != 0:
            current = documents[line[:-2]]
        elif line[3:-1] in documents:
            current.outbound.append(documents[line[3:-1]])
            documents[line[3:-1]].inbound.append(documents[current.url])

def rankByHITS(documents, iterations):
    for i in range(0, iterations):
        stdout.write(str(i + 1) + " out of " + str(iterations) + " iterations complete!\r")
        stdout.flush()
        norm = 0
        for doc in documents:
            documents[doc].auth = 0
            for incomming in documents[doc].inbound:
                documents[doc].auth += incomming.hub
            norm += pow(documents[doc].auth, 2)
        norm = sqrt(norm)
        for doc in documents:
            documents[doc].auth = documents[doc].auth / norm
        norm = 0
        for doc in documents:
            documents[doc].hub = 0
            for outbound in documents[doc].outbound:
                documents[doc].hub += outbound.auth
            norm += pow(documents[doc].hub, 2)
        norm = sqrt(norm)
        for doc in documents:
            documents[doc].hub = documents[doc].hub / norm
    stdout.write("\n")

def printRanks(documents, outputFileName):
    print("writing to output file...")
    newList = sorted(documents, key=lambda doc: documents[doc].auth + documents[doc].hub, reverse=True)
    rank = 1
    outputFile = open(outputFileName, "w")
    for url in newList:
        outputFile.write(str(rank) + "\t" + str(documents[url].auth + documents[url].hub) + " " + url + "\n")
        rank = rank + 1
    outputFile.close()

#yeah I'm used to java, learning python is hard
def main():
    if (len(sys.argv) < 4):
        showUsage()
    else:
        inputFileName  = sys.argv[1]
        outputFileName = sys.argv[2]
        iterations     = int(sys.argv[3])
        documents = {}
        processDocuments(documents, inputFileName)
        rankByHITS(documents, iterations)
        printRanks(documents, outputFileName)
        print("done!")

main()
