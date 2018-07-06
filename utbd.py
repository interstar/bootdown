
import unittest
from bootdown import Page, BootDown, handleDivs

from thoughtstorms.txlib import MarkdownThoughtStorms, LinkFixer, Environment

class TestPage(unittest.TestCase) :
    def test1(self) :       
        p = Page("page1.html\nhello world","",{})
        self.assertEquals(p.name,"page1.html")
        self.assertEquals(p.body,"<p>hello world</p>")
        
class TestPageBreak(unittest.TestCase) :
 
    def test1(self) :
        s = "hello world"
        bd = BootDown("",s)
        self.assertEquals(bd.pages,[])
        
    def test2(self) :
        s = """title=Hello World    
//// page1.html
page 1"""        
        bd = BootDown("",s)
        self.assertEquals(len(bd.pages),1)
        self.assertEquals(bd.atts["title"],"Hello World")
        self.assertEquals(bd.pages[0].name,"page1.html")
        self.assertEquals(bd.pages[0].body,"<p>page 1</p>")
        


    def test3(self) :
        s = """title=Hello World
menu=a a.com, b b.com        
//// page1.html
page 1
//// page2.html
Page 2

*  list"""
        bd = BootDown("",s)
        self.assertEquals(len(bd.pages),2)
        self.assertEquals(bd.atts["title"],"Hello World")
        p2= bd.pages[1]
        self.assertEquals(p2.name,"page2.html")
        self.assertEquals(p2.body,"""<p>Page 2</p>
<ul>
<li>list</li>
</ul>""")

class TestDivs(unittest.TestCase) :
    def test1(self) :
        s = "abc [.boo def [.hoo ghi[.shuff#ling jkl .] mno.]pqrs.]"
        des = """<p>abc</p>
<div class="boo">
<p>def</p>
<div class="hoo">
<p>ghi</p>
<div class="shuff" id="ling">
<p>jkl</p>
</div>
<p>mno</p>
</div>
<p>pqrs</p>
</div>"""
        self.assertEquals(handleDivs(s,0,"","",{}).replace("\n",""),des.replace("\n",""))

    def test2(self) :       
        s = "qwerty [.she uiop .] [.ra fafa.] jkl"
        des = '<p>qwerty</p>\n<div class="she">\n<p>uiop</p>\n</div>\n\n<div class="ra">\n<p>fafa</p>\n</div>\n<p>jkl</p>\n'
        self.assertEquals(handleDivs(s,0,"","",{}).replace("\n",""),des.replace("\n",""))

        
class TestRows(unittest.TestCase) :
    def test1(self) :
        s = """dummy=blah
////page1.html
[.row#r1

[.span3

# Page 5

[.hoo#boo hello inside .]
.]

.]"""
        bd = BootDown("",s)
        p = bd.pages[0]
        self.assertEquals(p.body.replace("\n",""),"""<div class="row" id="r1">
<div class="span3">
<h1>Page 5</h1>
<div class="hoo" id="boo">
<p>hello inside</p>
</div>
</div>
</div>""".replace("\n",""))

class TestMenu(unittest.TestCase) :
    def test1(self) :
        s = """menu=About about.html, Synaesmedia http://synaesmedia.net
////page1.html
blah blah"""
        bd = BootDown("",s)        
        self.assertEquals(bd.atts["menu"],"""<ul class="nav navbar-nav">
<li><a href="about.html">About</a></li>
<li><a href="http://synaesmedia.net">Synaesmedia</a></li>
</ul>""")
    def test2(self) :
        s = """menu=OneItem oneitem.html
////oneitem.html
blah"""
        bd = BootDown("",s)
        self.assertEquals(bd.atts["menu"],"""<ul class="nav navbar-nav">
<li><a href="oneitem.html">OneItem</a></li>
</ul>""")               

class TestMultiClass(unittest.TestCase) :
    def testMulti(self) :
        s = """blah=Blah
////index.html
[.another/green#world xyz .]"""
        bd = BootDown("",s)
        p = bd.pages[0]
        self.assertEquals(p.body,"""
<div class="another green" id="world">
<p>xyz</p>
</div>
""")


mkdn = MarkdownThoughtStorms()

env = Environment("/",{})

class TestBlocks(unittest.TestCase) :
    def test1(self) :
        s1 = "<p>hello world</p>"
        self.assertEquals(mkdn.cook(s1,env),"<p>"+s1+"</p>")
         
    def test2(self) :
        s2 = """[<YOUTUBE
id : MO2mb5HY3Yg
>]"""
        self.assertEquals(mkdn.cook(s2,env),"""<p><div class="youtube-embedded"><iframe width="400" height="271" src="http://www.youtube.com/embed/MO2mb5HY3Yg" frameborder="0" allowfullscreen></iframe></div></p>""")

class TestLinkFixing(unittest.TestCase) :
	def test1(self) :
		s = "Hello [[TeenageAmerica]]"
		self.assertEquals(LinkFixer(Environment("",{})).link_filters(s),"""Hello <a href="TeenageAmerica">TeenageAmerica</a>""")
	
	def test2(self) :
		s = "Hello [[TeenageAmerica]]"
		self.assertEquals(LinkFixer(Environment("http://mysite.site/path/",{})).link_filters(s),"""Hello <a href="http://mysite.site/path/TeenageAmerica">TeenageAmerica</a>""")

	def test3(self) :
		s = "Hello [[Elsewhere:TeenageAmerica]]"
		self.assertEquals(LinkFixer(Environment("",{"Elsewhere" : "http://remote.site/path/"})).link_filters(s),"""Hello <a href="http://remote.site/path/TeenageAmerica">Elsewhere:TeenageAmerica</a>""")
		
	def test4(self) :
		s = "Another [[test.html]]"
		self.assertEquals(LinkFixer(Environment("",{})).link_filters(s),"""Another <a href="test.html">test.html</a>""")
		
	def test5(self) :
		s = "Now with [[text.html a text link]]"
		self.assertEquals(LinkFixer(Environment("",{})).link_filters(s),"""Now with <a href="text.html">a text link</a>""")		
		

if __name__ == '__main__' :
    unittest.main()

