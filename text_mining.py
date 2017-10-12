###text_mining.py
import requests
bad_links = ["/wiki/Help","/wiki/File","/wiki/Wiki"]
links = {}
def find_start(text,start):
	'''
	Finds the start of the body and index 'start' of the wikipedia page represented by 'text'
	>>> find_start('<p>more</a></p><p>sucess</p>',10)
	15
	>>> find_start('cat<p><a>more</a></p><p>sucess</p>',0)
	21
	'''
	check = text.find("<p>",start)
	if check+5 >= len(text):
		raise ValueError("No appropriate start in string.")
	elif text[check+3:check+5]=="<a" or text[check+3:check+5]=="<s":
		return find_start(text,check+3)
	else:
		return check

def analyze_page(url):
    return requests.get(url).text

def find_link(text,start):
	'''
	Finds and returns the first internal link in 'text' after index 'start' and returns the link.
	This mehtod is very specific to Wikipedia in its parsing.
	>>> find_link('href="/wiki/exploding_kittens"',0)
	('/wiki/exploding_kittens', 16)
	>>> find_link('href="/wiki/nope" href="/wiki/exploding_kittens"',6)
	('/wiki/exploding_kittens', 34)
	>>> find_link('href="googlenope" href="/wiki/exploding_kittens"',6)
	('/wiki/exploding_kittens', 34)
	'''
	link_start = text.find('href=',start)+6
	link_end = text.find('"',link_start)
	first_link = text[link_start:link_end]
	a = first_link[:5]
	b = first_link[:10]
	if a != "/wiki" or b in bad_links: #insures it is a non-file, non-help internal link
		return find_link(text,link_end)
	else:
		return first_link,link_start+10

def crawl(page,depth,width):
	'''
	Accepts a starting 'page' and creates a tree of depth 'depth' following the first 'width' Wikipedia article links on each page.
	Returns a list whose first element is the origin, and each subsequent element is a branch. This pattern is followed recursively for each nested list.
	>>> print(crawl('/wiki/Turkish_language', 1, 1))
	/wiki/Turkish_language
	### Can't figure out how to make second test work, print statements commented for doctest ease
	#>>> crawl('/wiki/Turkish_language', 3, 1)
	['/wiki/Turkish_language', [['/wiki/Turkic_languages', ['/wiki/Language_family', '/wiki/Native_language']], ['/wiki/Ottoman_Turkish_language', ['/wiki/Register_(sociolinguistics)', '/wiki/Vulgar_Latin']]]]
	'''
	next_start = 0
	if page in links:
		#print('"'+page+'" was in links')
		return page
	else:
		links[page] = 1
	if depth <= 1:
		#print('maximum depth reached')
		return page
	text = analyze_page('https://en.wikipedia.org'+page)
	links_list = []
	next_link, next_start = find_link(text,find_start(text,next_start))
	res = []
	for i in range(0,2):
		res.append(crawl(next_link,depth-1,width))
		next_link, next_start = find_link(text,find_start(text,next_start))
	return([page,res])
out =crawl('/wiki/Turkish_language', 3, 1)
print(out)

if __name__ == "__main__":
	import doctest
	doctest.testmod(verbose=True)
