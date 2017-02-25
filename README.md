# svg-text-flow
Conversion of text objects in SVG 

## Background

You may have stumbled upon issues with text flow objects in SVG documents, where
 * the text would not show correctly in SVG viewers such as web browser;
 * the text could not be shown or editted in documents saved by different editors

This apparently depends on how much of the SVG specification is implemented. For example, SVG editor Inkscape (version 0.9) ignores text flow within Foreign Object code blocks and instead uses methods that are not supported by the SVG specification. 

## What can I find here?

The translation between foreign object (XHTML code) and flowroot (Inkscape) text flow objects can be straighforward. An example of such a translation has been included for a simple case, using Python.

Conversion of text flow objects to native SVG text objects is something Inkscape does very well, even from a command line.


