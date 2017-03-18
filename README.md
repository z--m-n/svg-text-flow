# svg-text-flow
Conversion of rectangular text flow objects in SVG 

## Background

For the time being there are [transitional](http://wiki.inkscape.org/wiki/index.php/Frequently_asked_questions#What_about_flowed_text.3F) issues with text flow objects in SVG documents, where
 * the text may not show correctly in SVG viewers such as web browsers
 * the text may not show up in another SVG editor

The SVG editor Inkscape (version 0.9) uses its own implementation for text flow not found in the SVG specification, whereas foreignObject elements (non-SVG, XHTML) are not widely supported yet. 

## What can I find here?

A very basic code example for the translation between foreignObject (XHTML code) and flowRoot (Inkscape) text flow. 

Example 1 includes:
* Example1.svg: a simple SVG document with text in a Foreign Object.
* Example1_mod.svg: the Foreign Object text flow was translated to Rootflow objects Inkscape. 
  ```bash 
  svg_foreign2flow.py -i Example1.svg -o Example1_mod.svg -s 100 100
  ```
* Example1_mod+conv.svg: the text flow was converted to plain SVG text elements. This made the SVG safe for use on the web and for conversion to other formats.
  The conversion of text flow objects to plain SVG text objects is something Inkscape does very well, also from the command   line:
  ```bash
  inkscape --file='Example1_mod.svg' \
     --export-area-page \
     --export-text-to-path \
     --export-pdf='Example1_mod+conv.pdf' 
  ```



