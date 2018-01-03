
import re, os

from txlib import MarkdownThoughtStorms, Environment
chef = MarkdownThoughtStorms()


def attRest(s) :
    [atts,rest] = re.split("[\s]",s,1)
    atts = atts.replace("."," ")
    if "#" in atts :
        [cls,id] = atts.split("#")
        cls = cls.replace("/"," ")
        atts = 'class="%s" id="%s"' % (cls,id)    
    elif "/" in atts :
        classes = atts.split("/")
        atts = 'class="' + " ".join(classes) + '"'     
    else :
        atts='class="%s"' % atts
    return (atts,rest)
            
def handleDivs(s,count,pageName,site_root,sister_sites) :
    if (not "[." in s) and (not ".]" in s) : return chef.cook(s,Environment(site_root,sister_sites))
    
    if (".]" in s) and (not "[." in s) :
        if (count < 1) : raise Exception("Mismatched divs, close without opening :: " + pageName + " :: " + s)        
        [rest,after] = s.rsplit(".]",1)
        return handleDivs(rest,count-1,pageName,site_root,sister_sites) + "\n</div>\n"+chef.cook(after,Environment(site_root,sister_sites))
    
    if ("[." in s) and (not ".]" in s) : 
        raise Exception("Mismatched divs, open without closing :: " + pageName + " :: " + s)
                
    if s.find("[.") < s.find(".]") :
        #open before close
        [before,rest] = s.split("[.",1)
        [atts,rest] = attRest(rest)
        return chef.cook(before,Environment(site_root,sister_sites)) + ("\n<div %s>\n" % atts) + handleDivs(rest,count+1,pageName,site_root,sister_sites)
        
    #close before the next open
    [before,after] = s.split(".]",1)
    return handleDivs(before,count,pageName,site_root,sister_sites) + "\n</div>\n" + handleDivs(after,count-1,pageName,site_root,sister_sites)
    
class Page :

    def __init__(self,page,site_root,sister_sites={}) :
        [name,body] = (page.split("\n",1))
        self.name = name.strip()
        self.body = handleDivs(body.strip(),0,self.name,site_root,sister_sites)
        self.raw = body.strip()
            

class BootDown :

    def __init__(self,cwd,src,site_root="",sister_sites={}) :
        src = src.decode("utf-8")
        if not "\n////" in src :
            self.pages = []
            self.atts = {}
        else :
            xs = src.split("\n////")
            self.make_globals(xs[0])
            if self.atts.has_key("site_root") :
            	site_root=self.atts["site_root"]
            else :
            	site_root=""
            self.pages = [Page(x,site_root,sister_sites) for x in xs[1:]]
            
            # extra pages            
            if self.atts.has_key("extra_pages") : 
                pages_path = cwd + "/" + self.atts["extra_pages"]
                page_names = [x for x in os.listdir(pages_path) if x[-3:]=='.md']
                for p in page_names :  
                    with open(pages_path+"/"+p) as f:
                        self.pages.append(Page(p.replace(".md",".html")+"\n"+f.read(),site_root,sister_sites)) 
                        
    
    def pair_gen(self,s) :
        p = (y.split("=",1) for y in s.split("\n") if "=" in y)
        return p

    def make_menu(self) :
        if self.atts.has_key("menu") :
            def link(x) :
                xs = x.split(" ")
                url = xs[-1]
                name = " ".join(xs[:-1])
                #[name,url] = x.split(" ")
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
        bd = BootDown(cwd,f.read())
        
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
                print "Currently copying ", name
                srcname = os.path.join(customDir, name)
                dstname = os.path.join(destPath, "bs", name)
                if os.path.isdir(srcname):
                    try :
                        shutil.copytree(srcname, dstname)
                    except OSError, oe :         
                        if oe.errno == 17 :
                            try :
                                shutil.rmtree(dstname)
                                shutil.copytree(srcname,dstname)           
                            except Exception, e :
                                print "Problem delete and copy %s to %s" % (srcname,dstname)
                                raise e
                        else :
                            raise e                                
                    except Exception, e :
                        print "Failed to copy %s to %s" % (srcname,dstname)
                        raise e
                else:
                    shutil.copy2(srcname, dstname)
                    
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
