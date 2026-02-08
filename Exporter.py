import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

def fetch_download_links(base_url, output_file='links.txt'):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {base_url}:\n{e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a_tag in soup.select('a[href]'):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        links.append(full_url)

    with open(output_file, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')

    print(f"✔ Saved {len(links)} links to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fetch_links.py <URL> [output_file]")
        sys.exit(1)

    url = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else 'links.txt'

    fetch_download_links(url, out_file)
