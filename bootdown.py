import re, markdown
import csv

def custom(s) :
    r = re.compile("::CSV=(\S+)",re.MULTILINE)    
    if r.search(s) :
        before,after = re.split("::CSV",s,1)
        m = r.search("::CSV"+after)
        build = ""
        with open(m.groups()[0], 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                build = build + "<tr><td>" + u'</td><td>'.join((ms(i.decode("utf-8")) for i in row)) + "</td></tr>\n"
        return before + """\n<table class="table table-striped table-bordered table-condensed">
%s
</table>""" % build

    return s                
                
                
def ms(s) : return markdown.markdown(custom(s.strip()))

def attRest(s) :
    [atts,rest] = re.split("[\s]",s,1)
    atts = atts.replace("."," ")
    if "#" in atts :
        [cls,id] = atts.split("#")
        atts = 'class="%s" id="%s"' % (cls,id)
    else :
        atts='class="%s"' % atts
    return (atts,rest)
            
def handleDivs(s,count) :
    if (not "[." in s) and (not ".]" in s) : return ms(s)
    
    if (".]" in s) and (not "[." in s) :
        if (count < 1) : raise Exception("Mismatched divs, close without opening :: " + s)        
        [rest,after] = s.rsplit(".]",1)
        return handleDivs(rest,count-1) + "\n</div>\n"+ms(after)
    
    if ("[." in s) and (not ".]" in s) : 
        raise Exception("Mismatched divs, open without closing :: " + s)
                
    if s.find("[.") < s.find(".]") :
        #open before close
        [before,rest] = s.split("[.",1)
        [atts,rest] = attRest(rest)
        return ms(before) + ("\n<div %s>\n" % atts) + handleDivs(rest,count+1)
        
    #close before the next open
    [before,after] = s.split(".]",1)
    return handleDivs(before,count) + "\n</div>\n" + handleDivs(after,count-1)
    
class Page :

    def __init__(self,page) :
        [name,body] = (page.split("\n",1))
        self.name = name.strip()
        self.body = handleDivs(body.strip(),0)
        self.raw = body.strip()
            

class BootDown :

    def __init__(self,page) :
        page = page.decode("utf-8")
        if not "\n////" in page :
            self.pages = []
            self.atts = {}
        else :
            xs = page.split("\n////")
            self.make_globals(xs[0])
            self.pages = [Page(x) for x in xs[1:]]
    
    def pair_gen(self,s) :
        p = (y.split("=",1) for y in s.split("\n") if "=" in y)
        return p

    def make_menu(self) :
        if self.atts.has_key("menu") :
            def link(x) : 
                [name,url] = x.split(" ")
                return """\n<li><a href="%s">%s</a></li>""" % (url.strip(),name.strip()) 
            self.atts["menu"] = '<ul class="nav navbar-nav">' + "".join(link(x.strip()) for x in self.atts["menu"].split(",")) + '\n</ul>'
        else :
            self.atts["menu"] = ""
    
            
    def make_globals(self,s) :
        self.atts = dict([x[0],x[1].strip()] for x in self.pair_gen(s))
        self.make_menu()
        
            
if __name__ == '__main__' :
    import sys,os,distutils,string
    
    codeHome = "/".join((os.path.abspath(__file__).split("/"))[:-1])+"/"
    cwd = os.getcwd()+"/"
    
    print "Code Home : %s " % codeHome
    print "CWD : %s " % cwd
    
    tpl = string.Template((open(codeHome+"index.tpl")).read())
        
    fName = sys.argv[1]
    with open(cwd + "/" + fName) as f :
        bd = BootDown(f.read())
        
        # setting up target directories
        if bd.atts.has_key("dest") :
            destPath = bd.atts["dest"]
        else :
            destPath = fName.split(".")[0]
        
        destPath = cwd + destPath
        
        if not os.path.exists(destPath) :
            os.makedirs(destPath)
        
        os.system("cp -rf %s/bs %s" % (codeHome,destPath))
        os.system("cp -rf assets %s/bs" % destPath)
        if bd.atts.has_key("bootswatch") :
            os.system("cp %sbs/bootswatches/%s/bootstrap.min.css %s/bs/css/" % (codeHome,bd.atts["bootswatch"],destPath))
                  
        for p in bd.pages :
            if p.name == "main.css" :
                f2 = open(destPath+"/bs/css/main.css","w")
                s = p.raw 
            else :
                f2 = open(destPath+"/"+p.name,"w")
                d = {"body":p.body}
                d.update(bd.atts)
                s = tpl.safe_substitute(d)
                
            f2.write(s.encode("utf-8"))
            f2.close()
