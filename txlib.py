import re, markdown, yaml, urllib2, csv


## Links

class LinkFixer :
	def __init__(self,site_root,sister_sites) :
		self.r_sister = re.compile("(\[\[((\S+?):(\S+?))\]\])")
		self.r_sqrwiki = re.compile("(\[\[(\S+?)\]\])")
		self.r_sqr_alt = re.compile("(\[\[((\S+?)(\s+)(.+))\]\])")
		self.site_root = site_root
		self.sister_sites = sister_sites

	def sub_sister(self) :
		def ss(mo) :
			mog = mo.groups()
			site_id,page_name = mog[2],mog[3]
			try :
				url = self.sister_sites[site_id].strip("/")
				return """<a href="%s/%s">%s:%s</a>""" % (url,page_name,site_id,page_name)
			except Exception, e :
				return "** | Error in SisterSite link ... seems like %s is not recognised. %s %s"  % (site_id,e,sister_sites)
		return ss

	def sister_line(self,s) :
		if self.r_sister.search(s) :
			s = self.r_sister.sub(self.sub_sister(),s)
		return s
	
	def sqrwiki_line(self,s) :
		if self.r_sqrwiki.search(s) :
			s = self.r_sqrwiki.sub(r"""<a href="%s\2">\2</a>"""%self.site_root,s)
		return s
		
	def sqr_alt_line(self,s) :
		if self.r_sqr_alt.search(s) :
			s = self.r_sqr_alt.sub(r"""<a href="%s\3">\5</a>"""%self.site_root,s)
		return s

	def link_filters(self,line) :
		return self.sqr_alt_line(self.sqrwiki_line(self.sister_line(line)))

class DoubleCommaTabler :

	def __init__(self) :
		self.tableMode = False
		self.newTable = False
		self.doubleComma = re.compile("(,,)")
		
	def __call__(self,l) :
		if not self.tableMode :
			if self.doubleComma.findall(l) :
				self.tableMode = True
				self.newTable = True
        
		if self.tableMode :
			if not self.doubleComma.findall(l) :
				l = l + "\n</table>"
				self.tableMode = False
			else :
				l = self.doubleComma.sub("</td><td>",l)
				l = "<tr><td>"+l+"</td></tr>"

		if self.newTable :
			l = "<table border=1px;>\n" + l
			self.newTable = False
			
		return l
		
table_line = DoubleCommaTabler()


def wiki_filters(s,site_root,sister_sites) : 
	return LinkFixer(site_root,sister_sites).link_filters(table_line(s))

		
## Standard Wikish (the markup of UseMod)
	
class WikishProcessor :
	
    def __init__(self,site_root,sister_sites) :
        self.blm = re.compile("^$")
        self.hr = re.compile("----")
        self.h6 = re.compile("^======(.+)======")
        self.h5 = re.compile("^=====(.+)=====")
        self.h4 = re.compile("^====(.+)====")
        self.h3 = re.compile("^===(.+)===")
        self.h2 = re.compile("^==(.+)==")
        self.h1 = re.compile("^=(.+)=")
        self.bold = re.compile("'''(.*?)'''")
        self.italic = re.compile("''(.*?)''")
        
        self.sqrbrkt = re.compile("(\[\[(\S+?)\]\])")
        self.extlink = re.compile("(\[(http\S+)\s+(.+?)\])")

		#self.wikiword = re.compile("([A-Z][a-z]+([A-Z][a-z]+)+)")
        
        
        self.indent = 0        
                 
    def line(self,l) :	
        nl = l.strip()
	   
        nl = self.blm.sub("<br/><br/>",nl)
        nl = self.hr.sub("<hr>",nl)
        nl = self.bold.sub(r"<b>\1</b>",nl)
        nl = self.italic.sub(r"<i>\1</i>",nl)

        nl = self.h6.sub(r"<h6>\1</h6>",nl)
        nl = self.h5.sub(r"<h5>\1</h5>",nl)
        nl = self.h4.sub(r"<h4>\1</h4>",nl)
        nl = self.h3.sub(r"<h3>\1</h3>",nl)
        nl = self.h2.sub(r"<h2>\1</h2>",nl)
        nl = self.h1.sub(r"<h1>\1</h1>",nl)
        nl = self.sqrbrkt.sub(r"""<a href="/view/\2">\2</a>""",nl)
        nl = self.extlink.sub(r"""<a href="\2">\3</a>""",nl)

        #nl = self.wikiword.sub(r"<a href='/view/\1' title='origin'>\1</a>",nl)        
	
            
        return nl


    def outlineFilter(self,l) :
        if l[0] != "*" :
            if self.indent > 0 :
                s = "</ul>"*(self.indent)
                self.indent = 0
                l = s + "\n" + l
            return l
        
        count = 0
        while l[count] == "*" :
            count=count+1
        meat = l[count:]

        if count == self.indent :
            return " " * (self.indent+1) + "<li>" + meat + "</li>"
        if count > self.indent :
            self.indent = self.indent + 1
            return "<ul>\n" + " " * (self.indent+1) + "<li>" + meat + "</li>"
        s = "</ul>" * (self.indent + 1 - count) + "<li>" + meat + "</li>" 
        self.indent = count
        return s

    def cook(self,p) :
        lines = (self.line(wiki_filters(l)) for l in p.split("\n"))
        lines = (self.outlineFilter(l) for l in lines)
        lines = (social_filters() for l in lines)        
        return "\n".join(lines)


chef = WikishProcessor("",{})

class Wikish2Markdown(WikishProcessor) :

	def __init__(self,convert_tables=False) :
		WikishProcessor.__init__(self)
		self.convert_tables = convert_tables
                 
	def line(self,l) :	
		nl = l.strip()
		nl = self.blm.sub("\n",nl)
        
		nl = self.bold.sub(r"**\1**",nl)
		nl = self.italic.sub(r"*\1*",nl)

		nl = self.h6.sub(r"###### \1",nl)
		nl = self.h5.sub(r"##### \1",nl)
		nl = self.h4.sub(r"#### \1",nl)
		nl = self.h3.sub(r"### \1",nl)
		nl = self.h2.sub(r"## \1",nl)
 		nl = self.h1.sub(r"# \1",nl)
        
 		nl = self.extlink.sub(r"""[\3](\2)""",nl)
              

		if self.convert_tables :
			if not self.tableMode :
			    if self.doubleComma.findall(nl) :
			        self.tableMode = True
			        self.newTable = True
			
			if self.tableMode :
			    if not self.doubleComma.findall(nl) :
			        nl = nl + "\n\n"
			        self.tableMode = False
			    else :
			        nl = self.doubleComma.sub(" | ",nl)
			        nl = "| "+nl+" |\n"

			if self.newTable :
			    nl = "| " + nl
			    self.newTable = False

		return nl


#### Current

from functools import reduce

OPEN = "[<"
CLOSE = ">]"
class BlockParseException(Exception) :
	pass

class UnknownBlock() : 
	def evaluate(self,lines) :
		return ["Block of type Unknown evaluated\n"] + lines + ["\nBLOCK ENDS"]
		
class YouTubeBlock() :
	def evaluate(self,lines) :
		data = yaml.load("\n".join(lines))
		return ["""<div class="youtube-embedded"><iframe width="400" height="271" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe></div>""" % data["id"]]

class SoundCloudBlock() :
	def evaluate(self,lines) :
		data = yaml.load("\n".join(lines))
		return [r"""<div class="soundcloud-embedded"><iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player?url=https://api.soundcloud.com/playlists/""" + "%s"%data["id"] + """&amp;visual=true"></iframe></div>"""]

class BandCampBlock() :
	def evaluate(self,lines) :
		data = yaml.load("\n".join(lines))
		return ["""<div class="bandcamp-embedded"><iframe style="border: 0; width: 350px; height: 555px;" src="https://bandcamp.com/EmbeddedPlayer/album=%s/size=large/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="%s">%s</a></iframe></div>""" % (data["id"],data["url"],data["description"])]
		
class AudioBlock() :
	def evaluate(self,lines) :
		data = yaml.load("\n".join(lines))
		if "mp3" in data :
			return ["""#### %s

<audio controls>
  <source src="%s" type="audio/mpeg">
Your browser does not support the audio element.
</audio>""" % (data["title"],data["mp3"])]


class LocalFileBlock() :
	def evaluate(self,lines) :
		data = yaml.load("\n".join(lines))
		try :
			f = open(data["path"])
			ext_lines = f.readlines()
		except Exception, e :
			ext_lines = ["Error, can't read %s" % data["path"]]
		return ["<pre>"] + ext_lines + ["</pre>"]

class SimpleRawTranscludeBlock() :
	def __init__(self,site_root,sister_sites) :
		self.site_root = site_root
		self.sister_sites = sister_sites

	def evaluate(self,lines,md_eval=True) :
		data = yaml.load("\n".join(lines))
		try :
			url = data["url"]
			response = urllib2.urlopen(url)
			s = response.read()
			#return s.split("\n")
			if md_eval :
				s = MarkdownThoughtStorms().cook(s,site_root,sister_sites)
			s = """
<div class="transcluded">

<strong>Transcluded from <a href="%s">%s</a> </strong>

%s

</div>	
""" % (url,url,s)
			return s.split("\n")
			
			
		except Exception, e :
			return ["Error, can't get data from %s" % url]


class CSVBlock() :
	def evaluate(self,lines,md_eval=True) :
		data = yaml.load("\n".join(lines))
		try :
			build = ""
			with open(data["path"]) as csvfile :
				reader = csv.reader(csvfile, delimiter=',', quotechar='"')
				for row in reader:
					build = build + "<tr><td>" + u'</td><td>'.join((i.decode("utf-8") for i in row)) + "</td></tr>\n"
				return ["""\n<table class="table table-striped table-bordered table-condensed">
    %s    
    </table>""" % build]
		except Exception, e :
			return ["Error in CSV Include %s " % e]
	
	
class Block :
	def __init__(self,typ) :
		self.type = typ
		self.lines = []
		if self.type == "YOUTUBE" :
			self.evaluator = YouTubeBlock()
		elif self.type == "SOUNDCLOUD" :
			self.evaluator = SoundCloudBlock()
		elif self.type == "BANDCAMP" :
			self.evaluator = BandCampBlock()
		elif self.type == "AUDIO" :
			self.evaluator = AudioBlock()
		elif self.type == "LOCALFILE" :
			self.evaluator = LocalFileBlock()
		elif self.type == "SIMPLERAWTRANSCLUDE" :
			self.evaluator = SimpleRawTranscludeBlock()
		elif self.type == "CSV" :
			self.evaluator = CSVBlock()
			
		else :
			self.evaluator = UnknownBlock()
		
	def add_line(self,l) :
		self.lines.append(l)
		
	def evaluate(self) : return self.evaluator.evaluate(self.lines)
		
class BlockServices : 
	"""
	Provides embeddable blocks within pages. This should become the generic mechanism for all inclusions / transclusions 
	"""
	def handle_lines(self,lines) :
		if not reduce(lambda a, b : a or b, [OPEN in l for l in lines],False) : return lines
		current_block = None
		in_block = False
		count = 0
		new_lines = []
		for l in lines :
			if in_block :
				# In Block
				if CLOSE in l :
					in_block = False
					count = count + 1
					new_lines = new_lines + current_block.evaluate()
					current_block=None
					continue
				elif OPEN in l :
					raise BlockParseException("Opening block inside another block at line %s" % count)
				else :
					# Do stuff inside block
					current_block.add_line(l)
					count = count + 1
			else :
				# Not in Block
				if CLOSE in l : 
					raise BlockParseException("Trying to close a block when we aren't in one at line %s" % count)	
				if OPEN in l :
					in_block = True
					block_type = l.split(OPEN)[1].strip()
					current_block = Block(block_type)
					count = count + 1
					continue
				# here we are not in a block and not starting one
				new_lines.append(l)
				count = count + 1		
		return new_lines

class MarkdownThoughtStorms :
	"""ThoughtStorms Wiki has been converted to Markdown for basic formatting.
	We keep some extra formatting. 
	Double Square brackets for internal links and Double commas as a quick table format, (handled within "wiki_filters")
	social_filters handles the social media embedding we use.
	Finally we do markdown.
	"""
	def cook(self,p,site_root,sister_sites) :
		lines = p.split("\n")
		lines = BlockServices().handle_lines(lines)
		lines = (wiki_filters(l,site_root,sister_sites) for l in lines)
		page = markdown.markdown("\n".join((l.strip() for l in lines)))                
		return page

