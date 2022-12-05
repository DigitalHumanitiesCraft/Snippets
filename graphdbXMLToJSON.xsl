<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:s="http://www.w3.org/2005/sparql-results#"
    exclude-result-prefixes="#all" version="2.0">

    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="text" media-type="application/json"/>

    <!--    [s:binding[@name='datensatzkennung']/s:literal[text()='NA 3660']]
-->    
    <xsl:template match="/">
        <xsl:text>[</xsl:text>
        <xsl:for-each select="//s:result">
            <xsl:text>{</xsl:text>
            <xsl:for-each select="s:binding">
                <xsl:text>"</xsl:text>
                <xsl:value-of select="@name"/>
                <xsl:text>": </xsl:text>
                <xsl:text>"</xsl:text>
                <xsl:choose>
                    <xsl:when test="s:literal != ''">
                        <xsl:value-of select="translate(normalize-space(s:literal),'\','/')"/>
                    </xsl:when>
                    <xsl:when test="s:uri != ''">
                        <xsl:value-of select="normalize-space(s:uris)"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>-</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text>"</xsl:text>
                <xsl:if test="position() != last()">
                    <xsl:text>,</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>}</xsl:text>
            <xsl:if test="position() != last()">
                <xsl:text>,</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]</xsl:text>
    </xsl:template>
</xsl:stylesheet>
