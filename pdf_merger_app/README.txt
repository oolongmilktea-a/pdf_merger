PDF Merger App
==============

This is a simple Python program with a small graphical interface that lets you merge two PDF files into one.

Requirements
------------
- Python 3.10+
- pypdf

Install dependency
------------------
pip install pypdf

Run the app
-----------
python pdf_merger.py

How to use
----------
1. Click Browse beside PDF 1 and choose the first PDF.
2. Click Browse beside PDF 2 and choose the second PDF.
3. Enter the output file name.
4. Click Merge PDFs.
5. Choose where to save the merged file.

Notes
-----
- The pages from PDF 1 will come first, followed by the pages from PDF 2.
- If a PDF is encrypted or damaged, the program may fail to open it.
