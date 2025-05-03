import os
import re
from bs4 import BeautifulSoup

def add_seo_elements(file_path, story_title):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Create meta tags
    meta_description = f"Read the classic fairytale of {story_title}, a timeless children's story perfect for bedtime reading. A beloved tale that teaches important life lessons to young readers."
    meta_keywords = f"{story_title}, fairytale, children's story, bedtime story, classic fairytale, moral story for kids"
    
    # Add meta tags
    head = soup.head
    if not head.find('meta', {'name': 'description'}):
        meta_desc = soup.new_tag('meta', attrs={'name': 'description', 'content': meta_description})
        head.insert(2, meta_desc)
    
    if not head.find('meta', {'name': 'keywords'}):
        meta_key = soup.new_tag('meta', attrs={'name': 'keywords', 'content': meta_keywords})
        head.insert(3, meta_key)
    
    if not head.find('meta', {'name': 'author'}):
        meta_author = soup.new_tag('meta', attrs={'name': 'author', 'content': 'Fairytales 4 Kids'})
        head.insert(4, meta_author)
    
    if not head.find('meta', {'name': 'robots'}):
        meta_robots = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'index, follow'})
        head.insert(5, meta_robots)
    
    # Add Open Graph tags
    og_tags = [
        ('og:title', f'{story_title} - Classic Fairytale for Children'),
        ('og:description', meta_description),
        ('og:type', 'article'),
        ('og:url', f'https://fairytales4kids.com/stories/{story_title.lower().replace(" ", "-")}'),
        ('og:image', f'../../assets/images/{story_title.lower().replace(" ", "-")}.jpg')
    ]
    
    for prop, content in og_tags:
        if not head.find('meta', {'property': prop}):
            meta_og = soup.new_tag('meta', attrs={'property': prop, 'content': content})
            head.append(meta_og)
    
    # Add Twitter Card tags
    twitter_tags = [
        ('twitter:card', 'summary_large_image'),
        ('twitter:title', f'{story_title} - Classic Fairytale for Children'),
        ('twitter:description', meta_description)
    ]
    
    for name, content in twitter_tags:
        if not head.find('meta', {'name': name}):
            meta_twitter = soup.new_tag('meta', attrs={'name': name, 'content': content})
            head.append(meta_twitter)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def process_story_files():
    # Get the absolute path to the stories directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stories_dir = os.path.join(os.path.dirname(current_dir), 'src', 'pages', 'stories')
    
    for filename in os.listdir(stories_dir):
        if filename.endswith('.html') and filename != 'stories.html':
            file_path = os.path.join(stories_dir, filename)
            story_title = filename.replace('.html', '').replace('-', ' ').title()
            add_seo_elements(file_path, story_title)
            print(f"Updated SEO elements for {story_title}")

if __name__ == '__main__':
    process_story_files() 