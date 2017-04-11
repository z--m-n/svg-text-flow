# svg-text-flow
Conversion of rectangular text flow objects in SVG 

## Background

For the time being there are [transitional](http://wiki.inkscape.org/wiki/index.php/Frequently_asked_questions#What_about_flowed_text.3F) issues with text flow objects in SVG documents, where
 * the text may not show correctly in SVG viewers such as web browsers
 * the text may not show up in another SVG editor

The SVG editor Inkscape (version 0.9) uses its own implementation for text flow not found in the SVG specification, whereas foreignObject elements (non-SVG, XHTML) are not widely supported yet. 

## What can I find here?

A very basic code example for the translation between foreignObject (XHTML code) and flowRoot (Inkscape) text flow. 

Usage:
```
svg-text-flow.py [-h] [-i input] [-o output] [-s scale scale] [-f font] [-v]

Translate text flow in SVG from foreignObject to flowRoot.

optional arguments:
  -h, --help      show this help message and exit
  -i input        path to input SVG
  -o output       path to output SVG
  -s scale scale  scale font size and line height (%)
  -f font         default font
  -v, --verbose   increase output verbosity
```

## Other conversions

The conversion of flowed text to plain SVG text elements is something Inkscape does very well, also from the command line.

Step 1:
```bash
inkscape \ # convert to plain
--export-plain-svg /path-to-file/Example1_plain.svg \
--file /path-to-file/Example1_inkscape.svg
```
Step 2:
```bash
inkscape \ # convert flowed text to text
--verb EditSelectAll \
--verb SelectionUnGroup \
--verb SelectionUnGroup \
--verb ObjectFlowtextToText \ # most relevant part
--verb FileSave \
--verb FileQuit \
--file /path-to-file/Example1_plain.svg
```

Or convert text to paths to remove any dependency on fonts (safe for use on the web):
```bash
inkscape \ # convert text to paths
--export-text-to-path \
--export-plain-svg /path-to-file/Example1_plain.svg \
--file /path-to-file/Example1_inkscape.svg
```

## Examples

Example 1 includes:
* Example1.svg: a simple SVG document with rectengular text flow in Foreign Object elements.
* Example1_inkscape.svg: the Foreign Object text flow was translated to Rootflow objects for use in Inkscape. 
* Example1_plain.svg: the text flow was converted to plain SVG text elements. This should look very close to Example1.png.
