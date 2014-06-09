import re, markdown


def ms(s) : return markdown.markdown(s.strip())

def attRest(s) :
    [atts,rest] = re.split("[\s]",s,1)
    atts = atts.replace("."," ")
    if "#" in atts :
        [cls,id] = atts.split("#")
        atts = 'class="%s" id="%s"' % (cls,id)
    else :
        atts='class="%s"' % atts
    return (atts,rest)
    
def tryOrReport(f) :
    def g(s) :
        try :
            f(s)
        except Exception, e :
            print e
            print "Error in " + s
    return g            
            
#@tryOrReport
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
            

class BootDown :
    
    def pair_gen(self,s) :
        p = (y.split("=") for y in s.split("\n") if "=" in y)
        return p

    def make_menu(self) :
        if self.atts.has_key("menu") :
            def link(x) : 
                [name,url] = x.split(" ")
                return """\n<li><a href="%s">%s</a></li>""" % (url.strip(),name.strip()) 
            self.atts["menu"] = '<ul class="nav navbar-nav">' + "".join(link(x.strip()) for x in self.atts["menu"].split(",")) + '\n</ul>'
    
            
    def make_globals(self,s) :
        self.atts = dict([x[0],x[1].strip()] for x in self.pair_gen(s))
        self.make_menu()
        
    def __init__(self,page) :
        if not "\n////" in page :
            self.pages = []
            self.atts = {}
        else :
            xs = page.split("\n////")
            self.make_globals(xs[0])
            self.pages = [Page(x) for x in xs[1:]]
            
if __name__ == '__main__' :
    import sys,os,distutils,string
    
    tpl = string.Template((open("index.tpl")).read())
        
    fName = sys.argv[1]
    with open(fName) as f :
        bd = BootDown(f.read())
        
        # setting up target directories
        if bd.atts.has_key("dest") :
            dest = bd.atts["dest"]
        else :
            dest = fName.split(".")[0]
            
        if not os.path.exists(dest) :
            os.makedirs(dest)
        
        os.system("cp -rf bs %s/" % dest)
        os.system("cp -rf assets %s/" % dest)
        if bd.atts.has_key("bootswatch") :
            os.system("cp bs/bootswatches/%s/bootstrap.min.css %s/bs/css/" % (bd.atts["bootswatch"],dest))
                  
        for p in bd.pages :
            f2 = open(dest+"/"+p.name,"w")
            d = {"body":p.body}
            d.update(bd.atts)

            s = tpl.safe_substitute(d)
            f2.write(s)
            f2.close()
