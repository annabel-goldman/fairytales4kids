import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from pathlib import Path

class PageChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.html'):
            print(f"New page detected: {event.src_path}")
            generate_sitemap()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.html'):
            print(f"Page modified: {event.src_path}")
            generate_sitemap()

def generate_sitemap():
    try:
        subprocess.run(['python', 'scripts/generate_sitemap.py'], check=True)
        print("Sitemap updated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating sitemap: {e}")

def main():
    # Create the public directory if it doesn't exist
    Path("public").mkdir(exist_ok=True)
    
    # Initial sitemap generation
    generate_sitemap()
    
    # Set up the file watcher
    event_handler = PageChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='src/pages', recursive=True)
    observer.start()
    
    try:
        print("Watching for changes in pages directory...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main() 