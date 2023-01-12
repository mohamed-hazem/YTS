# --- Modules --- #
import requests
from selectolax.parser import HTMLParser
import urllib.request

from zipfile import ZipFile
import os
from pyperclip import copy

import concurrent.futures
# ========================================== #
MOVIES_DIR = r"E:\Movies"
# ========================================== #

# ------------ Download API ------------ #
def search(movie_name):
    url = f"https://yts.mx/browse-movies/{movie_name}/all/all/0/latest/0/all"

    page = HTMLParser(requests.get(url).content)

    reults = page.css(".browse-movie-wrap")

    urls = [a.css_first(".browse-movie-link").attributes['href'] for a in reults]

    return urls

def get_movie_data(url):
    data = dict()
    try:
        page = HTMLParser(requests.get(url).content)

        data['img'] = page.css_first("#movie-poster").css_first("img").attributes['src']
        data['title'] = page.css_first("#movie-info").css_first("h1").text()
        data['year'] = page.css_first("#movie-info").css_first("h2").text(deep=False)
        data['rating'] = page.css_first(".bottom-info").css(".rating-row")[-1].css_first("span").text()
        data['imdb_id'] = page.css_first(".bottom-info").css(".rating-row")[-1].css_first("a").attributes['href'].split('/')[-2][2:]
        data['movie_page'] = f"{url}#screenshots"

        q = 1 if (len(page.css(".tech-spec-info")) > 1) else 0

        data['size'] = page.css(".tech-spec-info")[q].css(".row")[0].css(".tech-spec-element")[0].text(strip=True)
        data['duration'] = page.css(".tech-spec-info")[q].css(".row")[1].css(".tech-spec-element")[2].text(strip=True).replace(" ", "").replace("r", "r ")

        data['dl'] = page.css(".modal-torrent")[q].css_first(".magnet-download").attributes['href']
        data['quality'] = page.css_first(".bottom-info").css_first("p").css("a")[q].text().replace(".", " ")
        
        return data
    except:
        return None

# - Main Function - #
def main(movie_name):
    urls = search(movie_name)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_movie_data, urls)

    results = list(filter(lambda x: x is not None, results))

    return results
# ------------------------------------------------------------------------- #



# ------------ Subtitle API ------------ #
def make_movie_dir(name, year):
    invalid_chars = {':', '*', '<', '>', '?', '"', '|'}
    for char in invalid_chars:
        name = name.replace(char, "")
    
    title = f"{name} ({year})"
    dir = os.path.join(MOVIES_DIR, title)
    copy(dir)

    if not (os.path.isdir(dir)):
        os.mkdir(dir)

    return (dir, os.path.join(dir, f"{title}.zip"))

def download_file(dl, zipfile_dir, zipfile_path):
    # download Zip file
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'MyApp/1.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(dl, f"{zipfile_path}")

    # unzip file
    with ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(zipfile_dir)
    os.remove(zipfile_path)

# - Main Function - #
def download_subtitle(imdb_id, name, year):
    url = f"https://yifysubtitles.org//movie-imdb/tt{imdb_id}"
    page = HTMLParser(requests.get(url).content)

    subs = page.css_first("tbody").css('tr')
    arabic_subs = list(filter(lambda x: x.css_first('.sub-lang').text() == "Arabic", subs))

    # choose high rating subtitle
    arabic_sub = arabic_subs[0]
    max_rating = 0
    for sub in arabic_subs:
        sub_rate = int(sub.css_first('.rating-cell').text())
        if (sub_rate >= max_rating):
            arabic_sub = sub
            max_rating = sub_rate

    sub_title_name = arabic_sub.css_first('a').text(strip=True)[8:]

    sub_dl = arabic_sub.css_first('a').attributes['href']
    domain = sub_dl.split("/subtitles")[0]
    dl_page =  HTMLParser(requests.get(sub_dl).content)
    dl = f"{domain}/{dl_page.css_first('a.download-subtitle').attributes['href']}"     

    zipfile_dir, zipfile_path = make_movie_dir(name, year)
    download_file(dl, zipfile_dir, zipfile_path)

    return (True, sub_title_name)
# ------------------------------------------------------------------------- #

# print(download_subtitle("0443453", "Borat", "2006"))