menu=About about.html, Credits credits.html
footer=Copyleft Phil Jones, 2015
projectname=EXAMPLE
bootswatch=slate
head_extra=
////index.html

[.jumbotron [.container
# MAIN JUMBO
More stuff
.] .]

[.container [.row
[.col-md-4 
## One
.]

[.col-md-4
## Two
.]

[.col-md-4
## Three
.]

.].]
////about.html
[.container [.row [.col-md-12

## About BootDown

BootDown combines Markdown and Bootstrap to allow you to make quick and dirty static HTML sites as quickly and easily as possible.

Features 

  * Markdown - but extended with a short notation for divs with classes using [&nbsp;. See the source of this site for details.
  * Bootstrap and BootSwatch 
  
### Philosophy

Basically it's a Markdown to HTML processor with some extra tricks added to it
  * A header section that lets you define a menu, footer, projectname, bootswatch, head_extra (extra code to put in page headers)
  * A "page-break" option (lines beginning with ////) so that your single .md file becomes a number of HTML pages
  * A very light-weight markup for defining divs with classes and ids using [.CLASSNAME#ID and .]
  * A markup for including CSV files as tables.
  * A markup for embedding YouTube videos.
  
Unlike most static site systems that are built around templating engines, with BootDown you write both your page content, and the structure in a single source file. Using the [. and .] shorthand for divs. This gives you all the flexibility you need to layout your pages any way you like, within the BootStrap grid.

## Aims and Features

  * To be the quickest, laziest way to make an "acceptable" flat site.
  * Emphasis on the "acceptable". Comes with several off-the-shelf Bootstrap / [Bootswatches](https://bootswatch.com/) to choose from.
  * But strongly discourages you trying to write your own CSS or other styling. No templates!
  * Single Python script
  * Write your entire site in a single .md file. No faffing with managing multiple source files.
  * Suitable for landing pages, documentation sites, guides, handbooks, portfolios etc.
  

.].].]
////credits.html
[.container [.row [.col-md-12
## Credits 

  * Thanks to [MarkDown](https://daringfireball.net/projects/markdown/)
  * Thanks to [BootStrap](http://getbootstrap.com/) 
  * Thanks to [Python Markdown Lib](https://pypi.python.org/pypi/Markdown)
  * Thanks to [Bootswatch](https://bootswatch.com/)
  * Glue by Phil Jones 2014-2016

.].].]



