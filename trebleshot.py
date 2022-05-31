"""
This program just takes a HTML file, extracts all links of a certain kind from
it, downloads each of those images.

It's faster than using the UI provided by TrebleShot.  The problem is, data
needed to be offloaded from a phone, and a limitation of TrebleShot is that it
makes you both select and download each file manually; imagine doing that 135
times.  It was faster to write this Python program to download the web page
that has the links, and then grab and download each image link.

Both the phone and the computer this script is running on should be on the same
network.
"""


import requests
import os

from bs4 import BeautifulSoup


HOST_AND_PORT = 'http://192.168.1.125:58732'


def get_the_content(filename=None):
    """Somehow obtains the content of the HTML page, either via filename or a
    HTTP request."""
    if filename:
        filename = "Web Share - TrebleShot.html"
        with open(filename, 'r') as fh:
            contents = fh.read()
            soup = BeautifulSoup(contents, 'html5lib')
    else:
        response = requests.get(HOST_AND_PORT)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, 'html5lib')
    return soup


def _process_item(image):
    """Download the item and save it locally."""
    image_url = HOST_AND_PORT + image.attrs['href']
    print("Downloading %s.." % image_url)
    response = requests.get(image_url)
    assert response.status_code == 200
    print("Done.")

    filename = os.path.basename(image.attrs['href'])
    with open(filename, 'wb') as fh:
        fh.write(response.content)
    print("Saved to %s." % filename)


def _select_the_images(soup):
    """This is specific to the output that TrebleShot HTTP server uses."""
    images = soup.find_all('a', {'class': 'btn btn-primary'})
    return images


def main():
    """
    Driver function.

    By the time this function is called, the TrebleShot program on your phone
    should be currently open, and you should have the files selected for
    sharing, and the Web Share functionality operating."""
    soup = get_the_content()

    images = _select_the_images(soup)
    print(len(images))

    for image in images:
        _process_item(image)


if __name__ == '__main__':
    main()
