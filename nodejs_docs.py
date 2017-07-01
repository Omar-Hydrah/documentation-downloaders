# ---------------------
# This script downloads Nodejs Documentation from Nodejitsu 
# ---------------------

import pdfkit
import requests
import os
from bs4 import BeautifulSoup as Soup

# Links are stored in "div#column2 a" from anchor tag 3 to anchor tag 44
def grab_links(url):
	request  = requests.get(url)
	soup     = Soup(request.content, "html.parser")

	# Links are stored in this div.
	main_div    = soup.find("div", {"id" : "column2"})
	anchor_tags = main_div.find_all("a")

	links = anchor_tags[3:45]
	return links

# Creates file names for the pdfs to be saved.
def compose_file_name(page):
	# Example:
	# "assert.html" / "buffer.html"
	file_name = page.split(".")[0] + ".pdf"
	return file_name

# Takes links, and saves pdf files.
def download_page(page):
	url = "https://nodejs.org/api/" + page
	options = {"dpi": 380, "zoom": 0.5}
	pdfkit.from_url(url, compose_file_name(page), options = options)


def main():
	os.chdir("C:\\nodejs-docs")
	links = grab_links("https://nodejs.org/api/")
	for link in links:
		download_page(link["href"])


if __name__ == "__main__":
	main()