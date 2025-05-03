import os
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def clean_filename(title):
    """Clean the title to create a valid filename"""
    # Remove any non-alphanumeric characters except spaces and hyphens
    cleaned = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with hyphens and convert to lowercase
    return cleaned.lower().replace(' ', '-')

def get_story_content(file_path):
    """Read and parse the existing story content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return BeautifulSoup(content, 'html.parser')

def enhance_story_content(story_title, current_content):
    """Generate enhanced content for the story using ChatGPT"""
    prompt = f"""You are a fairy tale writer tasked with enhancing the story of "{story_title}". 
    The current content is:
    
    {current_content}
    
    Please enhance this story by:
    1. Enhancing the conflict of the story and making it more interesting
    2. Making sure the story is a good fit for an audience of children
    3. Including more dialogue between characters
    4. Expanding on character emotions and thoughts
    5. Maintaining the same moral lesson and plot structure
    6. Making sure each story has a rising action, climax, and resolution.
    
    Return only the enhanced story content, maintaining the same paragraph structure.
    Do not include any HTML tags or formatting."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fairy tale writer specializing in enhancing existing stories with richer details while maintaining their core message."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def update_story_page(file_path, enhanced_content):
    """Update the story page with enhanced content while preserving formatting"""
    soup = get_story_content(file_path)
    
    # Find the article tag
    article = soup.find('article')
    if article:
        # Clear existing content
        article.clear()
        
        # Split enhanced content into paragraphs
        paragraphs = enhanced_content.split('\n\n')
        
        # Add each paragraph as a new <p> tag
        for para in paragraphs:
            if para.strip():
                p_tag = soup.new_tag('p')
                p_tag.string = para.strip()
                article.append(p_tag)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def get_available_stories():
    """Get a list of available story files"""
    stories_dir = "../../src/pages/stories"
    story_files = [f for f in os.listdir(stories_dir) if f.endswith('.html')]
    return sorted(story_files)

def main():
    # Get list of available stories
    story_files = get_available_stories()
    
    # Display available stories
    print("\nAvailable stories to enhance:")
    print("-" * 30)
    for i, story_file in enumerate(story_files, 1):
        story_name = story_file.replace('.html', '').replace('-', ' ').title()
        print(f"{i}. {story_name}")
    
    # Get user selection
    while True:
        try:
            selection = int(input("\nEnter the number of the story you want to enhance: "))
            if 1 <= selection <= len(story_files):
                break
            print(f"Please enter a number between 1 and {len(story_files)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Get the selected story file
    selected_file = story_files[selection - 1]
    story_title = selected_file.replace('.html', '').replace('-', ' ').title()
    file_path = f"../../src/pages/stories/{selected_file}"
    
    # Get current content
    soup = get_story_content(file_path)
    article = soup.find('article')
    if not article:
        print("Error: Could not find story content in the file!")
        return
    
    # Extract current story content
    current_content = '\n\n'.join([p.get_text() for p in article.find_all('p')])
    
    # Generate enhanced content
    print(f"\nEnhancing story content for {story_title}...")
    enhanced_content = enhance_story_content(story_title, current_content)
    
    # Update the story page
    print("Updating story page...")
    update_story_page(file_path, enhanced_content)
    
    print(f"Successfully enhanced {story_title}!")

if __name__ == "__main__":
    main() 