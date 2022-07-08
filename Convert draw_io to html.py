from unittest import result
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

xslt_doc = etree.XML(XSLT_CONTENT)

input_doc = etree.parse('test.xml')
print ("document parsed")

transformer = etree.XSLT(xslt_doc)
result_xslt = input_doc.xslt(xslt_doc)
print ("document transformed")

result_doc = etree.ElementTree(result_xslt.getroot())
result_doc.write('test_result.xml', encoding='utf-8', compression = 0)

print ("document written")