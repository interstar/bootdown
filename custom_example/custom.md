menu=About #about, Tricks #tricks, Credits #credits
footer=Copyleft <a href="http://project.geekweaver.com/">Phil Jones</a>, 2014-2016
projectname=An Example Site
custom_template=cust_tpl

////index.html
<section id="top">

[.container 

[.row [.col-lg-12/text-center
## BootDown Custom Example
<hr class="star-primary">
.] .]


[.row
[.col-md-4 
### Dahlia
<img src="bs/assets/dahlia.jpg" width="90%"/>
.]

[.col-md-4
### Keystoke
<img src="bs/assets/keystoke.jpg" width="90%"/>
.]

[.col-md-4
### Lantana
<img src="bs/assets/lantana.jpg" width="90%"/>
.]

.].]

</section>



<section id="about">
[.container 

[.row [.col-lg-12/text-center
## About BootDown
<hr class="star-primary">
.] .]

[.row [.col-md-12

BootDown combines Markdown and Bootstrap to allow you to make quick and dirty static HTML sites as quickly and easily as possible.

Features 

  * Markdown - but extended with a short notation for divs with classes using [&nbsp;. See the source of this site for details.
  * Bootstrap and BootSwatch 
  
### Philosophy

Basically it's a Markdown to HTML processor with some extra tricks added to it

  * A header section that lets you define a menu, footer, projectname, bootswatch, head_extra (extra code to put in page headers)
  * A "page-break" option (lines beginning with ////) so that your single .md file becomes a number of HTML pages
  * A very light-weight markup for defining divs with classes and ids using &lbrack;.CLASSNAME#ID and .&rbrack;
  * A markup for including CSV files as tables.
  
Unlike most static site systems that are built around templating engines, with BootDown you write both your page content, and the structure in a single source file. Using &lbrack;. .&rbrack; for divs. This gives you all the flexibility you need to layout your pages any way you like, within the BootStrap grid.


### Aims and Features

  * To be the quickest, laziest way to make an "acceptable" flat site.
  * Emphasis on the "acceptable". Comes with several off-the-shelf Bootstrap / [Bootswatches](https://bootswatch.com/) to choose from.
  * But strongly discourages you trying to write your own CSS or other styling. No templates!
  * Single Python script
  * Write your entire site in a single .md file. No faffing with managing multiple source files.
  * Suitable for landing pages, documentation sites, guides, handbooks, portfolios etc.
  

.].].]
</section>

<section id="tricks">
[.container 

[.row [.col-lg-12/text-center
## Tricks
<hr class="star-primary">
.] .]



[.row [.col-md-12
### A CSV file
::CSV=example.csv

### Embedded YouTube
::YOUTUBE=https://www.youtube.com/watch?v=kszLwBaC4Sw
.] .]
</section>

<section id="credits">
[.container 

[.row [.col-lg-12/text-center
## Credits
<hr class="star-primary">
.] .]


[.row [.col-md-12

  * Thanks to [MarkDown](https://daringfireball.net/projects/markdown/)
  * Thanks to [BootStrap](http://getbootstrap.com/) 
  * Thanks to [Python Markdown Lib](https://pypi.python.org/pypi/Markdown)
  * Thanks to [Start Bootstrap](http://startbootstrap.com) for this custom template
  * Thanks to Susan Jones for the photographs.
  * Glue by [Phil Jones](http://sdi.thoughtstorms.info/) 2014-2016

.].].]
</section>

