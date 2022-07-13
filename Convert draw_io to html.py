import argparse
import sys
import os
from lxml import etree

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

if args.xslt:
    with open ('Remove_underscore_sheets_from_draw.io_file.xslt', 'w') as x:
        x.write(XSLT_CONTENT)

print ("input:" , args.input)
print ("output:", output)
        

xslt_doc = etree.XML(XSLT_CONTENT)

input_doc = etree.parse('test.xml')
print ("document parsed")

transformer = etree.XSLT(xslt_doc)
result_xslt = input_doc.xslt(xslt_doc)
print ("document transformed")

result_doc = etree.ElementTree(result_xslt.getroot())
result_doc.write('test_result.xml', encoding='utf-8', compression = 0)

print ("document written")