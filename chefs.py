
# All chefs have a 

# preProcess(self,s)
# postProcess(self,s)

import re, csv, markdown



class NullChef :
    def preProcess(self,s) :  return s
    def postProcess(self,s) : return s


def _C(*argv) :
    def inner(x) :
        for f in argv :
            x = f(x)
        return x
    return inner

def _D(x, *argv) : 
    return _C(*argv)(x)

                
def ms(s) : return markdown.markdown(mainChef.postProcess(s.strip()))


class DefaultChef :

    def preProcess(self,s) :
        return s
        
    def postProcess(self,s) :
        return _D(s,  lambda x : self.links(x),
                      lambda x : self.csv(x), 
                      lambda x : self.youtube(x), 
                      lambda x : self.soundcloud(x),
                      lambda x : self.bandcamp(x),
                      lambda x : self.bigcell(x))
    
    def links(self,s) :
        r = re.compile("\[\[(\S+)\]\]",re.MULTILINE)
        return r.sub(r"""<a href="\1.html">\1</a>""",s)
            

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
            s = r.sub(r"""<iframe width="98%"  src="\1" frameborder="0" allowfullscreen></iframe>""",s)
        return s
            
    def soundcloud(self,s) :
        r = re.compile("::SOUNDCLOUD=(\S+)",re.MULTILINE)
        if r.search(s) :
            s = r.sub(r"""<iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player?url=\1&amp;visual=true"></iframe>""",s)            
        return s

    def bandcamp(self,s) :
        r = re.compile("::BANDCAMP=(\S+)\s+(\S+)\s+(.+)",re.MULTILINE)
        if r.search(s) :
            s = r.sub(r"""<iframe style="border: 0; width: 350px; height: 555px;" src="https://bandcamp.com/EmbeddedPlayer/album=\1/size=large/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="\2">\3</a></iframe>""",s)
        return s



    def bigcell(self,s) :
        """ s is formated like this :
        ::CELL= title,, img,, desc,, link
        """
        r = re.compile("::CELL=(.+)$",re.MULTILINE)
        if r.search(s) :        
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

mainChef = DefaultChef()
