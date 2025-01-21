import requests
import xml.etree.ElementTree as ET


def fetch_rss_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
        return None

def parse_rss_feed(xml_content):
    root = ET.fromstring(xml_content)
    items = []
    
    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        items.append({
            'title': title,
            'description': description,
            'link': link
        })
    
    return items

def display_feed(items):
    for item in items:
        print(f"Title: {item['title']}")
        print(f"Description: {item['description']}")
        print(f"Link: {item['link']}")
        print("-" * 40)

def main():
    rss_url = input("Enter the RSS feed URL: ")
    xml_content = fetch_rss_feed(rss_url)
    
    if xml_content:
        items = parse_rss_feed(xml_content)
        display_feed(items)

if __name__ == "__main__":
    main()

def main():
    rss_urls = input("Enter the RSS feed URLs (comma-separated): ").split(',')
    all_items = []
    
    for url in rss_urls:
        url = url.strip()
        xml_content = fetch_rss_feed(url)
        
        if xml_content:
            items = parse_rss_feed(xml_content)
            all_items.extend(items)
    
    display_feed(all_items)

def parse_rss_feed(xml_content):
    root = ET.fromstring(xml_content)
    items = []
    
    # Handle RSS 2.0
    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        items.append({
            'title': title,
            'description': description,
            'link': link
        })
    
    # Handle Atom feeds
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        description = entry.find('{http://www.w3.org/2005/Atom}summary').text
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        items.append({
            'title': title,
            'description': description,
            'link': link
        })
    
    return items

