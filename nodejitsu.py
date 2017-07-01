# ---------------------
# This script downloads Nodejs Documentation from Nodejitsu 
# ---------------------

import pdfkit
import requests
import os
import threading
from bs4 import BeautifulSoup as Soup

# url = "https://docs.nodejitsu.com/articles/file-system/how-to-read-files-in-nodejs/"

# If the last slash exists, this function removes it.
# Slashes are used in naming files. No need for extra slashes.
def remove_last_slash(link):
	# if link[len(link)-1:len(link)] == "/":
	if link.endswith("/"):
		link = link[:len(link)-1]
	return link


# Extracts the pdf name from the url.
def extract_name(url):
	# Sample :
	# https://docs.nodejitsu.com/articles/file-system/how-to-read-files-in-nodejs
	link = remove_last_slash(url)
	
	partials = url.split("/")
	# partials list format:
	# [0] = "https" / [1] = "" / [2] = "docs.nodejitsu.com" / [3] = "articles"
	# [4] = "file-system" / [5] = "how-to-read-files-in-nodejs"

	# The name can compose of 2 parts at max
	# articles/file-system/how-to-read-files-in-nodejs
	# "file-system" would be the first part.
	# "how-to-read-files-in-nodejs" would be the second part
	first_part  = ""
	second_part = ""
	if partials[len(partials) -2] != "articles":
		first_part = partials[len(partials) -2]
	second_part = partials[len(partials) -1]
	# Concatenating full file name.
	file_name = ""
	if len(first_part) > 1:
		file_name = first_part + "-" + second_part + ".pdf"
	else:
		file_name = second_part + ".pdf"
	return file_name
		

def download_page(url):
	# example:
	# "/articles/file-system/how-to-read-files-in-nodejs/"

	# Making sure to trim any extra characters before "articles/"
	site = "https://docs.nodejitsu.com/" + url[url.find("articles"):]
	print("Downloading from: " + url)
	pdfkit.from_url(site, extract_name(url))

def get_articles_links(url):
	request = requests.get(url)
	soup    = Soup(request.content, "html.parser")
	anchor_tags = soup.find_all("a")

	links = []

	for tag in anchor_tags:
		# print(tag)
		if tag["href"].find("articles") != -1:
			links.append(tag["href"])
			# print(extract_name(tag["href"]))
			# print(tag["href"])
	return links


def main():
	os.chdir("C:\\nodejitsu")

	links = get_articles_links("https://docs.nodejitsu.com/articles/file-system/how-to-read-files-in-nodejs/")
	for link in links:
		download_page(link)


if __name__ == "__main__":
	main()