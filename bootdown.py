import re, markdown
import csv


class Customizer :

    def preProcess(self,s) :
        return s
        
    def postProcess(self,s) :
        s = self.csv(s)
        s = self.youtube(s)
        s = self.soundcloud(s)
        s = self.bandcamp(s)
        s = self.bigcell(s)
        
        return s                                
    
    def csv(self,s) :        
        r = re.compile("::CSV=(\S+)",re.MULTILINE)    
        if r.search(s) :
            before,after = re.split("::CSV=",s,1)
            m = r.search("::CSV="+after)
            build = ""
            with open(m.groups()[0], 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in reader:
                    build = build + "<tr><td>" + u'</td><td>'.join((ms(i.decode("utf-8")) for i in row)) + "</td></tr>\n"
            return before + ("""\n<table class="table table-striped table-bordered table-condensed">
    %s
    </table>""" % build) + after    
        return s
    
    def youtube(self,s) :
        r = re.compile("::YOUTUBE=(\S+)",re.MULTILINE)
        if r.search(s) :            
            s = r.sub(r"""<iframe width="640" height="360" src="\1" frameborder="0" allowfullscreen></iframe>""",s)
            print s
        return s
            
    def soundcloud(self,s) :
        r = re.compile("::SOUNDCLOUD=(\S+)",re.MULTILINE)
        if r.search(s) :
            s = r.sub(r"""<iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/\1&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe>""",s)
            print s
        return s

    def bandcamp(self,s) :
        r = re.compile("::BANDCAMP=(\S+)\s+(\S+)\s+(.+)",re.MULTILINE)
        if r.search(s) :
            s = r.sub(r"""<iframe style="border: 0; width: 350px; height: 555px;" src="https://bandcamp.com/EmbeddedPlayer/album=\1/size=large/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="\2">\3</a></iframe>""",s)
            print s
        return s



    def bigcell(self,s) :
        """ s is formated like this :
        ::CELL= title,, img,, desc,, link
        """
        r = re.compile("::CELL=(.+)$",re.MULTILINE)
        if r.search(s) :        
            print s
            print r.match(s)  
            print r.match(s).groups()
            title,img,desc,link = (x.strip() for x in (r.match(s).groups()[0]).split(",,"))  
            
            cell = """<div class="col-md-4">

<h3>%s</h3>

<a href='%s'><img src='%s' width='100px' /></a>
<div>
%s
</div>
</div>"""
            return cell % (title,link,img,desc)
        return s
                    
customizer = Customizer()
                
def ms(s) : return markdown.markdown(customizer.postProcess(s.strip()))

def attRest(s) :
    [atts,rest] = re.split("[\s]",s,1)
    atts = atts.replace("."," ")
    if "#" in atts :
        [cls,id] = atts.split("#")
        atts = 'class="%s" id="%s"' % (cls,id)
    elif "/" in atts :
        classes = atts.split("/")
        atts = 'class="' + " ".join(classes) + '"'     
    else :
        atts='class="%s"' % atts
    return (atts,rest)
            
def handleDivs(s,count,pageName) :
    if (not "[." in s) and (not ".]" in s) : return ms(s)
    
    if (".]" in s) and (not "[." in s) :
        if (count < 1) : raise Exception("Mismatched divs, close without opening :: " + pageName + " :: " + s)        
        [rest,after] = s.rsplit(".]",1)
        return handleDivs(rest,count-1,pageName) + "\n</div>\n"+ms(after)
    
    if ("[." in s) and (not ".]" in s) : 
        raise Exception("Mismatched divs, open without closing :: " + pageName + " :: " + s)
                
    if s.find("[.") < s.find(".]") :
        #open before close
        [before,rest] = s.split("[.",1)
        [atts,rest] = attRest(rest)
        return ms(before) + ("\n<div %s>\n" % atts) + handleDivs(rest,count+1,pageName)
        
    #close before the next open
    [before,after] = s.split(".]",1)
    return handleDivs(before,count,pageName) + "\n</div>\n" + handleDivs(after,count-1,pageName)
    
class Page :

    def __init__(self,page) :
        [name,body] = (page.split("\n",1))
        self.name = name.strip()
        self.body = handleDivs(body.strip(),0,self.name)
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
        if not self.atts.has_key("head_extra") : self.atts["head_extra"] = ""
        
        
            
if __name__ == '__main__' :
    import sys,os,distutils,string
	
    import shutil
    
    #codeHome = "/".join((os.path.abspath(__file__).split("/"))[:-1])+"/"
    #if codeHome == "" :
    codeHome = os.path.dirname(os.path.realpath(__file__))
		
    cwd = os.getcwd()
    
    print "Code Home : %s " % codeHome
    print "CWD : %s " % cwd
    
         
    fName = sys.argv[1]
    if fName[0:2] == ".\\" : 
        fName = fName[2:]
		
    print "fName : %s" % fName

    with open(os.path.join(cwd, fName)) as f :
        bd = BootDown(f.read())
        
        # setting up target directories
        if bd.atts.has_key("dest") :
            destPath = bd.atts["dest"]
        else :
            destPath = fName.split(".")[0]
        
        destPath = os.path.join(cwd, destPath)
        
        print "destPath : %s" % destPath
		
        if not os.path.exists(destPath) :
            os.makedirs(destPath)
        
        #os.system("cp -rf %s/bs %s" % (codeHome,destPath))
        print codeHome, destPath
        shutil.copytree(os.path.join(codeHome, "bs"),os.path.join(destPath,"bs"))
        #os.system("cp -rf assets %s/bs" % destPath)
        shutil.copytree("assets",os.path.join(destPath, "bs", "assets"))

        if bd.atts.has_key("custom_template") :
            customDir = bd.atts["custom_template"]
            print "customDir : %s" % customDir
            #os.system("cp -rf %s/* %s/bs/" % (customDir,destPath))
            names = os.listdir(customDir)
            print names
            for name in names : 
                srcname = os.path.join(customDir, name)
                dstname = os.path.join(destPath, "bs", name)
                try :
                    if os.path.isdir(srcname):
                        shutil.copytree(srcname, dstname)
                    else:
                        shutil.copy2(srcname, dstname)
                except Exception, e :
                    print "Failed to copy %s to %s" % (srcname,dstname)
                    raise e
			
            tpl = string.Template((open(os.path.join(customDir,"index.tpl"))).read())
        else :
            tpl = string.Template((open(os.path.join(codeHome,"index.tpl"))).read())
            if bd.atts.has_key("bootswatch") :
                #os.system("cp %sbs/bootswatches/%s/bootstrap.min.css %s/bs/css/" % (codeHome,bd.atts["bootswatch"],destPath))
				shutil.copy2(os.path.join(codeHome,"bs","bootswatches",bd.atts["bootswatch"],"bootstrap.min.css"),os.path.join(destPath,"bs","css"))
                              
        for p in bd.pages :
            if p.name == "main.css" :
                f2 = open(os.path.join(destPath,"bs","css","main.css"),"w")
                s = p.raw 
            else :
                f2 = open(os.path.join(destPath,p.name),"w")
                d = {"body":p.body}
                d.update(bd.atts)
                s = tpl.safe_substitute(d)
                
            f2.write(s.encode("utf-8"))
            f2.close()
