<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:param name="splitat" select="20000"/>
    <xsl:template match="dataroot" >
        <xsl:for-each-group select="./*" group-adjacent="(position()-1) idiv $splitat" >
            <xsl:result-document href="parts/{substring-after(substring-before(base-uri(),'.xml'),'XML/')}-part-{current-grouping-key()}.xml">
                <dataroot>
                    <xsl:copy-of select="current-group()" />
                </dataroot>
              
            </xsl:result-document>
        </xsl:for-each-group>
    </xsl:template>
    
</xsl:stylesheet>