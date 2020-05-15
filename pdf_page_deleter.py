# -*- coding: utf-8 -*-
"""

author: john roark
purpose: automatically removes specified PDF pages from all PDF files in the parent directory.
dependencies: PyPDF2, all others are core
version: python 3.7

-----------

MIT License

Copyright (c) 2020 JOHN ROARK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

## Import

## Function setup

from PyPDF2 import PdfFileWriter, PdfFileReader
from distutils.dir_util import copy_tree
import os
import glob
import shutil
import time

## Place start, temp, and 'new' (location for finished files) below --

## -- What folder are the PDFs currently in:

startFolder = '/example/directory'

## -- What should the temporary folder of the program be:

tempFolder = '/example/directory'

## -- Where should the finished PDFs go:

newFolder = '/example/directory'

def copyDirectory():
    
    print("Program will not run correctly if any user has any of the PDFs currently open \n")
    copyDirectoryUserAsk = input("Is anyone currently using any of the PDfs in this directory? (Y/N): ")
    
    if copyDirectoryUserAsk.lower() in (['n', 'no']):
    
        print("Copying files to:", tempFolder, "...")
        copy_tree(startFolder, tempFolder)
        print("Done!")
    
    elif copyDirectoryUserAsk.lower() in (['y', 'yes']):
    
        print("Please run again when ready...")
        time.sleep(3)
        exit()
    
    else:
    
        print("Please enter a valid response...")
        copyDirectory()

def clearDirectory():

    ## Short waits are added as to not cause issues with the fileserver getting so many rapid move and delete requests
    time.sleep(1)
    shutil.rmtree(startFolder)
    time.sleep(1)
    os.mkdir(startFolder)
    print("Done!")
    
def pdfProgramStart():
    
    pagesToDelete = []
    nPagesToDelete = 1
    ## user input appended to list for comparison later
    
    for i in range(0, nPagesToDelete):
    
        askForPages = int(input("What page(s) should be deleted? (1, 2, 3, etc): ")) - 1        
        pagesToDelete.append(askForPages)
        
    print("Delete page ", askForPages + 1, " ... okay")

    for pdf in glob.glob(os.path.join(tempFolder, '*.pdf')):
        pdfFile = PdfFileReader(pdf, strict=False)
        print("File: ", pdf)
        
        for pdfFiles in os.walk(tempFolder, topdown=False):
        
            outputFile = PdfFileWriter()
            ## Clears out function "PdfFileWriter() before beginning loop again
            for x in range(0, pdfFile.getNumPages()):
            
                if x not in pagesToDelete:
                
                    y = pdfFile.getPage(x)
                    outputFile.addPage(y)
                    print('Page', x + 1, 'saved')
                    y = 0
                    
                elif x in pagesToDelete:
                
                    print('Page', x + 1,'deleted')

            ## ^^ This adds all pages of a document except for pages not in pagesToDelete to an object in memory            
            ## This new document without the 'deleted' pages gets written to a file and exited.
            
            ## Creates new file at earlier set folder path below
    
            os.chdir(newFolder)
            newPdfName = str(os.path.basename(pdf))
            print("Generating new PDF: ", newFolder, newPdfName)
            
            ## Writes file 
            
            with open(newPdfName, 'wb') as newPdf:
            
                outputFile.write(newPdf)
    
    print('Files generated successfully...')
    
def main():

    copyDirectory()
    clearDirectory()
    pdfProgramStart()

main()
