#!/usr/bin/env python3
import print_with_chrome
from PdfGenerator import PdfGenerator
from pypdf import PdfMerger
import os
#TODO: Options to 1) set today's date; or 2) use last Saturday
crossword_date='2023-10-28'

pdf_file = PdfGenerator(['https://www.theage.com.au/puzzles/crosswords/cryptic/' + crossword_date,'https://www.theage.com.au/puzzles/crosswords/quick/' + crossword_date]).main()

with open('cryptic.pdf', "wb") as outfile:
    outfile.write(pdf_file[0].getbuffer())
with open('quick.pdf', "wb") as outfile:
    outfile.write(pdf_file[1].getbuffer())

pdfs = ['cryptic.pdf', 'quick.pdf']
merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()
#TODO: Load printer from config, or just use default
os.system('lp -d Brother_HL-2270DW_series -o sides=two-sided-short-edge result.pdf')

