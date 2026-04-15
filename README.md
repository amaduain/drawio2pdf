# drawio2pdf
convert drawio files to pdf using the drawio CLI.
Layers in drawio will be converted to OCGs (optional content groups) with the correct name and visibility as in the drawing.
Those Layers/OCGs can be enabled/disabled in most modern PDF viewers.

usage: drawio2pdf.py input.drawio -o output.pdf

## Requirements
python module: pymupdf

Edit the file to change the path to your draw.io executable

## Limitations
This version allows to convert multiple pages, it creates one pdf per page in draw.io, because of PDF limitations and to avoid to create a mess of layers, it is easier to generate one pdf per page.
In any case you can merge the documents into one later using adobe pdf editor or other options.

