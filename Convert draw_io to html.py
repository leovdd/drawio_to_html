import argparse
import sys
import os
from lxml import etree
from tkinter import messagebox

XSLT_CONTENT = '''<?xml version='1.0'?>
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="@*|node()">
        <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="//diagram[contains(@name,'_')]">

    </xsl:template>
    </xsl:stylesheet>
'''

parser = argparse.ArgumentParser(description="Removes sheets starting with underscore from draw.io files. Works on both compressed as well as non-compressed files.")
parser.add_argument ("input", default = 'input.xml', help = "The original file. Defaults to 'input.xml'.")
parser.add_argument ("-o",help = "The cleaned file. By default it's [input filename]_cleaned.xml")
parser.add_argument ("--verbose", action=argparse.BooleanOptionalAction, help="Shows progress of script via informational messages. Used for trouble shooting mostly.")
parser.add_argument ("--xslt", action=argparse.BooleanOptionalAction, help="Saves the xslt used as 'Remove_underscore_sheets_from_draw.io_file.xslt'. Input filename is mandatory when used !")


input = ""
output = ""

args = parser.parse_args()

input = args.input   

input_filename, input_extention = os.path.splitext(args.input)
if args.o:
    output_filename, output_extention = os.path.splitext(args.o)
    if output_extention:
        output = args.o
    else:
        output = output_filename + '.xml'
else:
    output = input_filename + "_cleaned"
    if input_extention:
        output = output + input_extention
    else:
        output = output + ".xml"

if args.verbose:
    messagebox.showinfo(title="Program", message = "Ready to transform: \r\n\r\nInput file:\t"+ input + "\r\nOutput file:\t"+ output)

if args.xslt:
    try:
        with open ('Remove_underscore_sheets_from_draw.io_file.xslt', 'w') as x:
            x.write(XSLT_CONTENT)
            if args.verbose:
                messagebox.showinfo(title="XSLT", message="XSLT written to file Remove_underscore_sheets_from_draw.io_file.xslt.")
    except IOError:
        messagebox.showwarning (title= "XSLT", message="XSLT information could not be written to file: Remove_underscore_sheets_from_draw.io_file.xslt ." )

xslt_doc = etree.XML(XSLT_CONTENT)

try:
    input_doc = etree.parse(input)
    if args.verbose:
        messagebox.showinfo(title='Input', message= 'Input file ' + input +  ' succesfully parsed.')
except IOError:
    messagebox.showerror(title = 'Input', message = 'Input file '+input+ " not found or couldn't read.")
    exit(1)
except etree.XMLSyntaxError:
    messagebox.showerror(title = "Input", message = 'Input file '+input+ ' contains invalid xml.')
    exit(1)

try:
    result_xslt = input_doc.xslt(xslt_doc)
    if args.verbose:
        messagebox.showinfo(title="Parsing", message = "Transformation succeeded.")
except any:
    messagebox.showerror(title="Transformation", message= "XSLT transformation did not succeed.")
    exit(1)

result_doc = etree.ElementTree(result_xslt.getroot())

try:
    result_doc.write(output, method='xml', encoding='utf8')
    if args.verbose:
        messagebox.showinfo(title="Output", message = "Result of transformation written into file "+ output)
except IOError as e:
    messagebox.showerror(title="Output", message="File " +output+" could not be written")
    exit (1)

if args.verbose:
    messagebox.showinfo (title = "Process", message="Operation succesful.")