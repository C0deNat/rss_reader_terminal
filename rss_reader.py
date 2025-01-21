import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from io import BytesIO

# Function to fetch the RSS feed content
def fetch_rss_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
        return None

# Function to parse the RSS feed
def parse_rss_feed(xml_content):
    root = ET.fromstring(xml_content)
    items = []
    
    # Handle RSS 2.0
    for item in root.findall('.//item'):
        title = item.find('title').text
        description = item.find('description').text
        link = item.find('link').text
        
        # Extract image URL (if available)
        image_url = None
        media_content = item.find('.//media:content', namespaces={'media': 'http://search.yahoo.com/mrss/'})
        if media_content is not None:
            image_url = media_content.attrib.get('url')
        else:
            enclosure = item.find('enclosure')
            if enclosure is not None and enclosure.attrib.get('type', '').startswith('image'):
                image_url = enclosure.attrib.get('url')
        
        items.append({
            'title': title,
            'description': description,
            'link': link,
            'image_url': image_url
        })
    
    # Handle Atom feeds
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        description = entry.find('{http://www.w3.org/2005/Atom}summary').text
        link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        
        # Extract image URL (if available)
        image_url = None
        media_content = entry.find('.//media:content', namespaces={'media': 'http://search.yahoo.com/mrss/'})
        if media_content is not None:
            image_url = media_content.attrib.get('url')
        
        items.append({
            'title': title,
            'description': description,
            'link': link,
            'image_url': image_url
        })
    
    return items

# Function to fetch and display an image from a URL
def fetch_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            image.thumbnail((100, 100))  # Resize image to fit in the GUI
            return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Failed to fetch image: {e}")
    return None

# Function to display the feed items in the GUI
def display_feed(items, output_frame):
    # Clear previous content
    for widget in output_frame.winfo_children():
        widget.destroy()
    
    # Display each feed item
    for item in items:
        item_frame = tk.Frame(output_frame, bd=2, relief=tk.GROOVE)
        item_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Display image (if available)
        if item['image_url']:
            image = fetch_image(item['image_url'])
            if image:
                image_label = tk.Label(item_frame, image=image)
                image_label.image = image  # Keep a reference to avoid garbage collection
                image_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Display text (title, description, link)
        text_frame = tk.Frame(item_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(text_frame, text=item['title'], font=('Arial', 12, 'bold'), anchor='w')
        title_label.pack(fill=tk.X)
        
        description_label = tk.Label(text_frame, text=item['description'], wraplength=600, anchor='w')
        description_label.pack(fill=tk.X)
        
        link_label = tk.Label(text_frame, text=item['link'], fg='blue', cursor='hand2', anchor='w')
        link_label.pack(fill=tk.X)
        link_label.bind('<Button-1>', lambda e, url=item['link']: open_link(url))

# Function to open a link in the default web browser
def open_link(url):
    import webbrowser
    webbrowser.open(url)

# Function to handle the "Fetch Feed" button click
def fetch_and_display_feed():
    rss_urls = url_entry.get().strip()
    if not rss_urls:
        output_text.insert(tk.END, "Please enter at least one RSS feed URL.\n")
        return
    
    all_items = []
    for url in rss_urls.split(','):
        url = url.strip()
        xml_content = fetch_rss_feed(url)
        
        if xml_content:
            items = parse_rss_feed(xml_content)
            all_items.extend(items)
    
    display_feed(all_items, output_frame)

# Create the main GUI window
root = tk.Tk()
root.title("RSS Feed Reader")

# Create and place the URL input field
url_label = tk.Label(root, text="Enter RSS Feed URLs (comma-separated):")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the "Fetch Feed" button
fetch_button = tk.Button(root, text="Fetch Feed", command=fetch_and_display_feed)
fetch_button.pack(pady=10)

# Create and place the output frame (for feed items)
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True)

# Run the GUI event loop
root.mainloop()