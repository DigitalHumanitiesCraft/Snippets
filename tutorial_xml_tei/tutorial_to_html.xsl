<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    Company: Digital Humanities Craft OG
    Author: Christopher Pollin
    Last update: 2022
 -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:lido="http://www.lido-schema.org"
    xmlns:bibtex="http://bibtexml.sf.net/" exclude-result-prefixes="#all">

    <xsl:template match="/">

        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport"
                    content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
                <meta name="description" content=""/>
                <meta name="author" content=""/>
                <title>Just a Tutorial</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"
                    rel="stylesheet"
                    integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU"
                    crossorigin="anonymous"/>
                <link rel="stylesheet" href="css/tutorial_highlighting.css"/>
            </head>
            <body>
                <header>
                    <nav class="navbar navbar-expand-lg navbar-light bg-light">
                        <div class="container-fluid">
                            <a class="navbar-brand" href="#">Navbar</a>
                            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                                data-bs-target="#navbarSupportedContent"
                                aria-controls="navbarSupportedContent" aria-expanded="false"
                                aria-label="Toggle navigation">
                                <span class="navbar-toggler-icon"/>
                            </button>
                            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                    <li class="nav-item">
                                        <a class="nav-link active" aria-current="page" href="#"
                                            >Home</a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </nav>
                </header>

                <div class="container-fluid">
                    <div class="row">
                        <div class="col-sm-auto bg-light sticky-top">
                            <div
                                class="d-flex flex-sm-column flex-row flex-nowrap bg-light align-items-center sticky-top">
                                <a href="/" class="d-block p-3 link-dark text-decoration-none"
                                    title="" data-bs-toggle="tooltip" data-bs-placement="right"
                                    data-bs-original-title="Icon-only">
                                    <i class="bi-bootstrap fs-1"><xsl:text> </xsl:text></i>
                                </a>
                                <ul
                                    class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mb-auto mx-auto text-center align-items-center">
                                    <xsl:for-each select="//t:div[@xml:id]">
                                        <li class="nav-item">
                                            <a href="{concat('#', @xml:id)}"
                                                class="nav-link py-3 px-2" title=""
                                                data-bs-toggle="tooltip" data-bs-placement="right"
                                                data-bs-original-title="Home">
                                                <span>
                                                  <xsl:value-of select="t:head"/>
                                                </span>
                                            </a>
                                        </li>
                                    </xsl:for-each>
                                </ul>
                            </div>
                        </div>
                        <div class="col-sm p-3 min-vh-100">
                            <h2>
                                <xsl:value-of select="//t:teiHeader//t:title[1]"/>
                            </h2>
                            <!-- ? -->
                            <div xml:id="abstract" class="lead">
                                <xsl:apply-templates select="//t:teiHeader/t:profileDesc/t:abstract/t:p"/>
                            </div>
                            <xsl:apply-templates select="//t:body"/>
                        </div>
                    </div>
                </div>
                <!-- Bootstrap core JS-->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"><xsl:text> </xsl:text></script>
                <!--  -->
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"><xsl:text> </xsl:text></script>
                <script>hljs.highlightAll();</script>
                <!-- copy code -->
                <script src="js/tutorial.js"><xsl:text> </xsl:text></script>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="t:head">
        <xsl:variable name="depth" select="count(ancestor::t:div) + 2"/>
        <xsl:element name="h{$depth}">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="t:div">
        <div id="{@xml:id}">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <!--  -->
    <xsl:template match="t:span[@type = 'tooltip']">
        <span class="text-decoration-underline">
            <xsl:if test="t:note">
                <xsl:attribute name="title" select="normalize-space(t:note)"/>
            </xsl:if>
            <xsl:apply-templates select="text()"/>
        </span>
    </xsl:template>
    
    <xsl:template match="t:ref[@target]">
        <xsl:choose>
            <xsl:when test="@type='video'">
                <video width="320" height="240">
                    <source src="{@target}" type="video/mp4"/>
                    Your browser does not support the video tag.
                </video> 
            </xsl:when>
            <xsl:otherwise>
                <a href="{@target}">
                    <xsl:apply-templates/>
                </a>
            </xsl:otherwise>
        </xsl:choose>
       
    </xsl:template>

    <xsl:template match="t:hi">
        <span>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    <xsl:template match="t:lb">
        <br/>
    </xsl:template>

    <xsl:template match="t:p | t:ab">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match="t:code">
        <code>
            <xsl:call-template name="rend"/>
            <xsl:apply-templates/>
        </code>
    </xsl:template>
    
    <xsl:template match="t:figure">
        <xsl:variable name="POSITION" select="count(preceding::t:code[@rend = 'block'])+1"/>
        <figure class="figure container m-3">
            <img src="{t:graphic/@url}" class="img-fluid d-block mx-auto" alt="{t:caption}" width="500" height="500"/>
            <xsl:if test="t:caption">
                <figcaption class="figure-caption text-center">
                    <figcaption class="figure-caption text-center">
                        <xsl:value-of select="concat('Figure ', $POSITION, ': ', t:caption)"/>
                    </figcaption>
                 </figcaption>
            </xsl:if>
        </figure>
    </xsl:template>
    
    
    <xsl:template match="t:ab[t:code[@rend = 'block']]">
        <xsl:variable name="POSITION" select="count(preceding::t:code[@rend = 'block']) + 1"/>
        <div class="border mb-3">
            <div class="nav p-2 justify-content-end">
                <a class="btn btn-outline-dark btn-sm" type="button"
                    onclick="copy(document.getElementById('{generate-id()}'))">Copy</a>
            </div>
            <div class="tab-content mb-4">
                <div class="tab-pane active" role="tabpanel">
                    <pre class="grey lighten-3 mb-0 line-numbers overflow-auto" style="max-height: 500px;">
                        <code id="{generate-id()}">
                            <xsl:value-of select="t:code[@rend = 'block']"/>
                        </code>
                        <xsl:if test="t:caption">
                            <figcaption class="figure-caption text-center">
                                <xsl:value-of select="concat('Code Snippet ', $POSITION, ': ', normalize-space(t:caption))"/>
                            </figcaption>
                        </xsl:if>
                    </pre>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="t:list">
        <xsl:choose>
            <xsl:when test="@rend = 'numbered'">
                <ol>
                    <xsl:apply-templates/>
                </ol>
            </xsl:when>
            <xsl:when test="@rend = 'simple'">
                <ul style="list-style-type: none;">
                    <xsl:apply-templates/>
                </ul>
            </xsl:when>
            <xsl:otherwise>
                <ul>
                    <xsl:apply-templates/>
                </ul>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="t:item">
        <li>
            <xsl:apply-templates/>
        </li>
    </xsl:template>

    <xsl:template match="t:table">
        <table class="table">
            <tbody>
                <xsl:apply-templates select="t:row"/>
            </tbody>
        </table>
    </xsl:template>

    <xsl:template match="t:row">
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>

    <xsl:template match="t:cell">
        <td>
            <xsl:apply-templates/>
        </td>
    </xsl:template>

    <xsl:template name="rend">
        <xsl:if test="@rend">
            <xsl:choose>
                <xsl:when test="@rend = 'bold'">
                    <xsl:attribute name="class">
                        <xsl:text>fw-bold</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="@rend = 'italic'">
                    <xsl:attribute name="class">
                        <xsl:text>fst-italic</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="@rend = 'underline'">
                    <xsl:attribute name="class">
                        <xsl:text>text-decoration-underline</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <!-- styling inline code with same color as code block via highlight.js -->
                <xsl:when test="@rend = 'attribute'">
                    <xsl:attribute name="class">
                        <xsl:text>hljs-attr</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="@rend = 'element'">
                    <xsl:attribute name="class">
                        <xsl:text>hljs-name</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
