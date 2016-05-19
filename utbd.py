
import unittest
from bootdown import *

class TestPage(unittest.TestCase) :
    def test1(self) :       
        p = Page("page1.html\nhello world")
        self.assertEquals(p.name,"page1.html")
        self.assertEquals(p.body,"<p>hello world</p>")
        
class TestPageBreak(unittest.TestCase) :
 
    def test1(self) :
        s = "hello world"
        bd = BootDown(s)
        self.assertEquals(bd.pages,[])
        
    def test2(self) :
        s = """title=Hello World    
//// page1.html
page 1"""        
        bd = BootDown(s)
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
        bd = BootDown(s)
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
        s = "sfds [.boo fsfsdf [.hoo sdfsdfs[.shuff#ling sdfds .] dsfsd.]sdfs.]"
        des = """<p>sfds</p><div class="boo">
<p>fsfsdf</p><div class="hoo">
<p>sdfsdfs</p><div class="shuff" id="ling">
<p>sdfds</p>
</div><p>dsfsd</p>
</div><p>sdfs</p>
</div>"""
        self.assertEquals(handleDivs(s,0).replace("\n",""),des.replace("\n",""))

    def test2(self) :       
        s = "asdas [.she jljlkj .] [.ra fafa.] jkl"
        des = '<p>asdas</p>\n<div class="she">\n<p>jljlkj</p>\n</div>\n\n<div class="ra">\n<p>fafa</p>\n</div><p>jkl</p>'
        self.assertEquals(handleDivs(s,0).replace("\n",""),des.replace("\n",""))

        
class TestRows(unittest.TestCase) :
    def test1(self) :
        s = """dummy=blah
////page1.html
[.row#r1

[.span3

# Page 1

[.hoo#boo hello inside .]
.]

.]"""
        bd = BootDown(s)
        p = bd.pages[0]
        self.assertEquals(p.body.replace("\n",""),"""<div class="row" id="r1">

<div class="span3">
<h1>Page 1</h1>
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
        bd = BootDown(s)        
        self.assertEquals(bd.atts["menu"],"""<ul class="nav navbar-nav">
<li><a href="about.html">About</a></li>
<li><a href="http://synaesmedia.net">Synaesmedia</a></li>
</ul>""")
    def test2(self) :
        s = """menu=OneItem oneitem.html
////oneitem.html
blah"""
        bd = BootDown(s)
        self.assertEquals(bd.atts["menu"],"""<ul class="nav navbar-nav">
<li><a href="oneitem.html">OneItem</a></li>
</ul>""")               

class TestMultiClass(unittest.TestCase) :
    def testMulti(self) :
        s = """blah=Blah
////index.html
[.another.green#world xyz .]"""
        bd = BootDown(s)
        p = bd.pages[0]
        self.assertEquals(p.body,"""
<div class="another green" id="world">
<p>xyz</p>
</div>
""")

class TestCustomizer(unittest.TestCase) :
    def test1(self) :
        c = Customizer()
         
        s1 = "hello world"
        self.assertEquals(c.postProcess(s1),s1)
         
    def test2(self) :
        c = Customizer()
        
        s2 = "::YOUTUBE=https://www.youtube.com/watch?v=MO2mb5HY3Yg"
        self.assertEquals(c.postProcess(s2),"""<iframe width="640" height="360" src="https://www.youtube.com/watch?v=MO2mb5HY3Yg" frameborder="0" allowfullscreen></iframe>""")

        s3 = "::YOUTUBE=http://www.youtube.com/watch?v=MO2mb5HY3Yg"
        self.assertEquals(c.postProcess(s3),"""<iframe width="640" height="360" src="http://www.youtube.com/watch?v=MO2mb5HY3Yg" frameborder="0" allowfullscreen></iframe>""")

    def test3(self) : 
        c = Customizer() 
        s = "::CELL= About,, aboutimg.png,, About me,, about.html"
        self.assertEquals(c.postProcess(s),"""<div class="col-md-4">

<h3>About</h3>

<a href='about.html'><img src='aboutimg.png' width='100px' /></a>
<div>
About me
</div>
</div>""")
        s = "::CELL= Elsewhere,, elsewhere.png,, Elsewhere,, elsewhere.html"
        self.assertEquals(c.postProcess(s),"""<div class="col-md-4">

<h3>Elsewhere</h3>

<a href='elsewhere.html'><img src='elsewhere.png' width='100px' /></a>
<div>
Elsewhere
</div>
</div>""")

if __name__ == '__main__' :
    unittest.main()
