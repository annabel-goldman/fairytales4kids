import os
from datetime import datetime
import xml.etree.ElementTree as ET
from pathlib import Path

def generate_sitemap():
    # Base URL for your website
    base_url = "https://fairytales4kids.com"
    
    # Create the root element
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Add the main pages with appropriate priorities
    add_url(urlset, base_url + "/", datetime.now().strftime("%Y-%m-%d"), "1.0", "weekly")
    add_url(urlset, base_url + "/pages/stories.html", datetime.now().strftime("%Y-%m-%d"), "0.9", "weekly")
    
    # Add all story pages
    stories_dir = Path("../src/pages/stories")
    if not stories_dir.exists():
        print(f"Error: Stories directory not found at {stories_dir}")
        return
    
    for story_file in stories_dir.glob("*.html"):
        story_url = base_url + "/pages/stories/" + story_file.name
        # Get the last modification time of the file
        lastmod = datetime.fromtimestamp(story_file.stat().st_mtime).strftime("%Y-%m-%d")
        add_url(urlset, story_url, lastmod, "0.8", "monthly")
        print(f"Added to sitemap: {story_file.name}")
    
    # Create the XML tree
    tree = ET.ElementTree(urlset)
    
    # Write to sitemap.xml in the public directory
    sitemap_path = Path("../public/sitemap.xml")
    with open(sitemap_path, "wb") as f:
        # Add proper XML formatting
        tree.write(f, encoding="UTF-8", xml_declaration=True, method="xml")
    
    print(f"Sitemap generated at: {sitemap_path}")

def add_url(urlset, loc, lastmod, priority="0.5", changefreq="monthly"):
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = loc
    ET.SubElement(url, "lastmod").text = lastmod
    ET.SubElement(url, "changefreq").text = changefreq
    ET.SubElement(url, "priority").text = priority

if __name__ == "__main__":
    generate_sitemap() 