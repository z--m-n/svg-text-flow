# svg-text-flow
Conversion of text objects in SVG 

## Background

You may have stumbled upon issues with text flow objects in SVG documents, where
 * the text would not show correctly in SVG viewers such as web browsers
 * the text did not show up a different SVG editor

It apparently depends on how much of the SVG specification is implemented. For example, SVG editor Inkscape (version 0.9) ignores text flow within foreignObject code blocks and instead uses methods that are not supported by the SVG specification. 

## What can I find here?

The translation between foreignObject (XHTML code) and flowRoot (Inkscape) text flow elements can be straighforward. An example of such a translation has been included with an example, using Python.

Example 1 includes:
* Example1.svg: a simple SVG document with text in a Foreign Object.
* Example1_mod.svg: the Foreign Object text flow was translated to Rootflow objects Inkscape. 
* Example1_mod+conv.svg: the text flow was converted to native SVG text objects. This made the SVG safe for use on the web.

Conversion of text flow objects to native SVG text objects is something Inkscape does very well, even from a command line.




