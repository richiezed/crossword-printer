#!/usr/bin/env python3
import print_with_chrome
from PdfGenerator import PdfGenerator
from pypdf import PdfMerger
import os
from datetime import datetime
from datetime import timedelta
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="Prints a crossword from The Age. Default is to print one copy of previous Saturday"
)
#parser = argparse.ArgumentParser()
#parser.add_argument('weeksback', nargs='?', default=0)
parser.add_argument("--today", action="store_true", help="Use this flag to print today's crossword instead of the the one that would otherwise be printed")
parser.add_argument("-d", "--day", default=6, type=int, choices=range(1,8), metavar='[1-7]', help="The day of the week to be printed (Mon to Sun), if you want to override Saturday.")
parser.add_argument("-b", "--back", default=0, metavar='<n>', type=int, help="<n> is number of weeks back.")
parser.add_argument("-c", "--copies", default=1, type=int, choices=range(0,6), metavar='[0-5]', help="The number of copies to be printed.")

args = parser.parse_args()
#print(args.weeksback)

copies=args.copies

if(args.today):
    printDate = today = datetime.today()

else:
    today = datetime.today() - timedelta(weeks = int(args.back))
    cwday=args.day-1
    offset = (today.weekday() + 7- cwday ) % 7
    printDate = today - timedelta(days=offset)

crossword_date = printDate.strftime("%Y-%m-%d")


#crossword_date='2023-11-05'



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

#os.system('lp -d Brother_HL-2270DW_series -o sides=two-sided-short-edge result.pdf')
printrun = 0
while printrun < copies:
    os.system('lp -o sides=two-sided-short-edge result.pdf')
    printrun += 1