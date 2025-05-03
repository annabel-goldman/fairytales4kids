import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import re
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def get_story_symbol(story_title):
    """Generate a key object or symbol that represents the story"""
    prompt = f"""Given the fairy tale title "{story_title}", provide a single, specific object or symbol that best represents the story.
    For example:
    - For "Little Red Riding Hood" -> "red hood"
    - For "Cinderella" -> "glass slipper"
    - For "Snow White" -> "poisoned apple"
    
    Return only the object/symbol, nothing else."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fairy tale expert who can identify key symbols and objects from stories."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def clean_filename(title):
    """Clean the title to create a valid filename"""
    # Remove any non-alphanumeric characters except spaces and hyphens
    cleaned = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with hyphens and convert to lowercase
    return cleaned.lower().replace(' ', '-')

def generate_story_content(story_title):
    """Generate HTML content for the story using ChatGPT"""
    cleaned_title = clean_filename(story_title)
    prompt = f"""Create an HTML page for a fairy tale titled "{story_title}". 
    The page should follow this exact structure:
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Read the classic fairytale of {story_title}, a timeless children's story perfect for bedtime reading. A beloved tale that teaches important life lessons to young readers.">
        <meta name="keywords" content="{story_title}, fairytale, children's story, bedtime story, classic fairytale, moral story for kids">
        <meta name="author" content="Fairytales 4 Kids">
        <meta name="robots" content="index, follow">
        <meta property="og:title" content="{story_title} - Classic Fairytale for Children">
        <meta property="og:description" content="Read the classic fairytale of {story_title}, a timeless children's story perfect for bedtime reading. A beloved tale that teaches important life lessons to young readers.">
        <meta property="og:type" content="article">
        <meta property="og:url" content="https://fairytales4kids.com/stories/{cleaned_title}">
        <meta property="og:image" content="../../assets/images/{cleaned_title}.jpg">
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{story_title} - Classic Fairytale for Children">
        <meta name="twitter:description" content="Read the classic fairytale of {story_title}, a timeless children's story perfect for bedtime reading.">
        <title>{story_title} - Fairytales 4 Kids</title>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3709806584351963"
         crossorigin="anonymous"></script>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="../../styles/styles.css">
        <link rel="stylesheet" href="../../styles/story.css">
    </head>
    <body>
        <header>
            <a href="../stories.html" class="back-button">Back to Stories</a>
            <div class="header-content">
                <img src="../../assets/images/{cleaned_title}.jpg" alt="{story_title}" class="title-image">
                <h1>{story_title}</h1>
            </div>
        </header>
        <main>
            <article>
                [Insert the story content here, broken into paragraphs]
            </article>
        </main>
        <footer>
            <footer>&copy; 2024 Fairytales 4 Kids. All rights reserved. Made with ❤️ for young readers everywhere.</footer>
        </footer>
    </body>
    </html>
    
    The story should be engaging and appropriate for children. Include multiple paragraphs to make it easy to read.
    Return only the HTML content, no markdown or other formatting."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fairy tale writer creating HTML content."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_story_image(story_title):
    """Generate an image for the story using DALL-E"""
    # Get the key symbol for the story
    story_symbol = get_story_symbol(story_title)
    
    # Create a detailed prompt that describes the desired style
    prompt = f"""Create a cartoon image of a {story_symbol} in the following specific style:
    - Flat vector illustration with bold dark brown outlines
    - Simple, clean shapes with minimal details
    - Solid colors with subtle texture
    - Light powder blue background
    - Single centered object
    - Soft shadow underneath
    - Clean, minimalist design like a modern children's book illustration
    - Style similar to a basic emoji design"""
    
    # Generate the image
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    # Get the image URL
    image_url = response.data[0].url
    
    # Download the image
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    
    # Save the image with cleaned filename
    image_filename = f"../../src/assets/images/{clean_filename(story_title)}.jpg"
    image.save(image_filename, "JPEG")
    
    return image_filename

def update_stories_html(story_title):
    """Update the stories.html file to include the new story"""
    # Read the current stories.html
    with open('../../src/pages/stories.html', 'r') as f:
        html_content = f.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the stories-grid div
    stories_grid = soup.find('div', class_='stories-grid')
    
    # Create new story card with proper formatting
    new_story = soup.new_tag('a', href=f"stories/{clean_filename(story_title)}.html", **{'class': 'story-card'})
    
    # Add a newline and indentation before the new card
    stories_grid.append('\n    ')
    
    # Create image tag
    img = soup.new_tag('img', 
                       src=f"../assets/images/{clean_filename(story_title)}.jpg",
                       alt=story_title,
                       **{'class': 'story-card-image'})
    new_story.append('\n        ')
    new_story.append(img)
    
    # Create content div
    content_div = soup.new_tag('div', **{'class': 'story-card-content'})
    new_story.append('\n        ')
    new_story.append(content_div)
    
    # Create h2 tag
    h2 = soup.new_tag('h2')
    h2.string = story_title
    content_div.append('\n            ')
    content_div.append(h2)
    content_div.append('\n        ')
    
    new_story.append('\n    ')
    
    # Add the new story card to the grid
    stories_grid.append(new_story)
    stories_grid.append('\n')
    
    # Format the entire HTML document
    formatted_html = soup.prettify()
    
    # Write the updated HTML back to the file
    with open('../../src/pages/stories.html', 'w') as f:
        f.write(formatted_html)

def main():
    # Get story title from user
    story_title = input("Enter the title of the fairy tale: ")
    
    # Generate image
    print("Generating image...")
    image_path = generate_story_image(story_title)
    print(f"Image generated and saved to {image_path}")
    
    # Generate HTML content
    html_content = generate_story_content(story_title)
    
    # Save HTML file in the stories directory
    html_filename = f"../../src/pages/stories/{clean_filename(story_title)}.html"
    with open(html_filename, 'w') as f:
        f.write(html_content)
    
    # Update stories.html
    print("Updating stories.html...")
    update_stories_html(story_title)
    print("stories.html updated successfully!")
    
    print(f"Successfully generated {story_title}!")

if __name__ == "__main__":
    main() 