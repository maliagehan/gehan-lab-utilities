#!/usr/bin/env python

## This was written by Malia Gehan, Donald Danforth Plant Science Center, creation date: 08-09-2016 ##

import argparse
import sys, os
import time
import csv
import pyqrcode as qr
import cv2
import numpy as np
import shutil
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Get file names to run cuffdiff over")
  parser.add_argument("-f", "--file", help="path to file", required=True)
  parser.add_argument("-d", "--delim", help="delimiter of file either tab or comma", required=False)
  parser.add_argument("-o", "--outname", help="name for resulting file of barcodes to print", required=False)
  args = parser.parse_args()
  return args

  """Create qr codes from a file of data.

  Inputs:
  file = text file of information for barcodes for now first column should be barcode info second column + should be a
         human readable label for underneath the QR code. One barcode per line.
  delim = the delimiter either 'comma' or 'tab' for more than one column
  outname = the filename for the resulting file of barcodes that you want to print

  Returns:
  Ultimately returns a concatenated file with barcodes to print

  :param filename: str
  :return img: numpy array
  :return path: str
  :return img_name: str
  """

def create_barcodes(file,delim):

    currenttime=time.time()
    tempfilename='temp_'+str(currenttime)
    cwd = os.getcwd()
    directory = str(cwd)+"/"+str(tempfilename)
    path = str(directory)+"/"
    barcodefile = str(file)

    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        raise RuntimeError("A temp directory of this name exists, fatal error.")

    if delim=='tab':
        delimvalue='\t'
    elif delim=='comma':
        delimvalue=','
    else:
        delimvalue=None

    with open(barcodefile) as fileinput:
        reader = csv.reader(fileinput, delimiter=delimvalue)
        for row in reader:
            barcodeqr=qr.create(str(row[0]))
            currenttime1 = time.time()
            barname=str(path)+str(currenttime1)+".png"
            barcodeqr.png(barname , scale=2)
            barcodepic=cv2.imread(barname)
            barcodepic1=cv2.copyMakeBorder(barcodepic,10,20, 25, 25,cv2.BORDER_CONSTANT,value=(255,255,255))

            ix,iy,iz=np.shape(barcodepic1)
            cv2.putText(barcodepic1,str(row[1]),(25,ix-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,0))
            cv2.imwrite(barname,barcodepic1)

    return path

def cat_barcodes(path,outname):
    path1=str(path)
    file1= os.listdir(path1)

    with PdfPages(str(outname)) as pdf:
        for x in file1:
            imgpath = str(path) + str(x)
            newpage = plt.imread(str(imgpath))
            plt.plot()
            plt.imshow(newpage)
            plt.axis('off')
            pdf.savefig(bbox_inches='tight')  # saves the current figure into a pdf page
            plt.close()

    shutil.rmtree(path1)

### Main pipeline
def main():
    # Get options
    args = options()

    path1=create_barcodes(args.file, args.delim)
    cat_barcodes(path1, args.outname)

if __name__ == '__main__':
    main()