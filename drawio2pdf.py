#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import subprocess
import pymupdf
import argparse
import os

parser = argparse.ArgumentParser(description="Convert drawio files to pdf with layers")
parser.add_argument("-o", "--output", help="pdf output file name", default="ouput.pdf")
parser.add_argument("input", help="drawio input file name")
args = parser.parse_args()

#Path to the Drawio, this is for windows
drawio_path = "C:\Program Files\draw.io\draw.io.exe"

tree = ET.parse(args.input)
root = tree.getroot()
total_pages = int(root.get("pages"))
print("Total drawio pages: " +  str(total_pages))
pages = []
for page in range(total_pages):
    print("Processing page: " + str(page))
    layers = []
    if page == 0:
        for x in root[page][0][0]:
            if x.tag == "mxCell" and x.attrib.get("parent") == "0":
                if "value" not in x.attrib:
                    x.attrib["value"] = "Background"
                layers.append({"name": x.attrib["value"], "visible": x.attrib.get("visible") != "0"})
                
            if x.tag == "object" and x[0].attrib.get("parent") == "0":
                layers.append({"name": x.attrib["label"], "visible": x[0].attrib.get("visible") != "0"})
        pages.append(layers)
    else:
        parent_id = ""
        for x in root[page][0][0]:
            if x.tag == "mxCell" and "parent" not in x.keys():
                print("Parent: " +x.get("id") )
                parent_id=x.get("id")
            if x.tag == "mxCell" and x.attrib.get("parent") == parent_id:
                if "value" not in x.attrib:
                    x.attrib["value"] = "Background"
                layers.append({"name": x.attrib["value"], "visible": x.attrib.get("visible") != "0"})
                
            if x.tag == "object" and x[0].attrib.get("parent") == parent_id:
                layers.append({"name": x.attrib["label"], "visible": x[0].attrib.get("visible") != "0"})
        pages.append(layers)

    
for drawio_page in range(len(pages)):
    subprocess.run([drawio_path, "-l", "-1", "-t", "-o", ".base.pdf", "-x", args.input])
    doc = pymupdf.open(".base.pdf")
    doc_page = doc.load_page(0)
    layer = pages[drawio_page]
    for i, layer in enumerate(layers):
        subprocess.run([drawio_path, "-p", str(drawio_page + 1), "-l", str(i), "-t", "-o", ".layer.pdf", "-x", args.input])
        doc_layer = pymupdf.open(".layer.pdf")
        xref = doc.add_ocg(layer["name"], on=layer["visible"])
        doc_page.show_pdf_page(doc_page.rect, doc_layer, 0, oc=xref)
        doc_layer.close()
    doc.save(str(drawio_page) + "_" + args.output)
    doc.close()
    os.remove(".layer.pdf")
    os.remove(".base.pdf")