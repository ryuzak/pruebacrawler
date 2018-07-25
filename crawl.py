from urllib.request import Request, urlopen, urljoin, URLError
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup

class Crawler(object):
	"""docstring for Crawler"""

	base_url = ''
	myssl = ssl.create_default_context()
	myssl.check_hostname=False
	myssl.verify_mode=ssl.CERT_NONE
	errorLinks = set()
	crawledLinks = set()

	def __init__(self, base_url):
		Crawler.base_url = base_url

	@staticmethod
	def crawl(thread_name, url, linksToCrawl):
		try:
			link = urljoin(Crawler.base_url, url)
			if (urlparse(link).netloc == 'tutorialedge.net') and (link not in Crawler.crawledLinks):
				request = Request(link, headers={'User-Agent':'Mozilla/5.0'})
				response = urlopen(request, context=Crawler.myssl)
				Crawler.crawledLinks.add(link)
				print('url {} crawled with status {} : {} crawled in total'.format(response.geturl(), response.getcode(), len(Crawler.crawledLinks)))
				soup = BeautifulSoup(response.read(), 'html.parser')
				Crawler.enqueueLinks(soup.find_all('a'), linksToCrawl)
		except URLError as e:
			print('URL {} threw this error when trying to parse: {}'.format(link, e.reason))
			Crawler.errorLinks.add(link)

	@staticmethod
	def enqueueLinks(links, linksToCrawl):
		for link in links:
			if(urljoin(Crawler.base_url, link.get('href')) not in Crawler.crawledLinks):
				if(urljoin(Crawler.base_url, link.get('href')) not in linksToCrawl):
					linksToCrawl.put(link.get('href'))