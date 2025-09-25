import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib.parse
import time
import sqlite3

def setup_database(db_path):
    """
    Sets up the SQLite database and creates the 'downloaded_files' table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloaded_files (
            filename TEXT PRIMARY KEY,
            download_date TEXT
        )
    ''')
    conn.commit()
    return conn

def is_file_downloaded(conn, filename):
    """
    Checks if a filename exists in the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM downloaded_files WHERE filename = ?", (filename,))
    return cursor.fetchone() is not None

def add_downloaded_file(conn, filename):
    """
    Adds a new filename to the database.
    """
    cursor = conn.cursor()
    download_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT OR REPLACE INTO downloaded_files (filename, download_date) VALUES (?, ?)", 
                   (filename, download_date))
    conn.commit()

def sanitize_filename(name):
    """
    Sanitizes a string to be a valid filename by removing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*\']', '', name).strip()

def download_bing_images(output_directory, conn, days=30):
    """
    Downloads images from the Bing Image Archive API, checking against the database.
    """
    base_url = "https://www.bing.com"
    api_url = f"{base_url}/HPImageArchive.aspx?format=js&idx=0&n={days}&mkt=en-US"

    os.makedirs(output_directory, exist_ok=True)
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        images_data = response.json().get("images", [])

        if not images_data:
            print("No Bing images found.")
            return

        print(f"Starting Bing images download for the last {days} days...")
        count = 0
        for image in images_data:
            image_title = sanitize_filename(image.get("title", "").replace(" ", "_") or "bing_image")
            filename = f"{image_title}.jpg"
            
            if is_file_downloaded(conn, filename):
                print(f"Skipping {filename}, already in database.")
                continue

            image_url = base_url + image["url"]
            image_path = os.path.join(output_directory, filename)

            print(f"Downloading {filename}...")
            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status()
            with open(image_path, "wb") as image_file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    image_file.write(chunk)
            
            add_downloaded_file(conn, filename)
            count += 1

        print(f"{count} Bing Image(s) Downloaded!")
    except Exception as e:
        print(f"An error occurred during Bing download: {e}")

def download_spotlight_images(output_directory, conn, num_images=10):
    """
    Scrapes and downloads images from windows10spotlight.com, checking against the database.
    """
    main_url = "https://windows10spotlight.com/"
    os.makedirs(output_directory, exist_ok=True)

    try:
        response = requests.get(main_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        intermediate_links = soup.find_all('a', href=re.compile(r'images/'))
        if not intermediate_links:
            print("Could not find intermediate image links on the main page.")
            return

        unique_urls = set()
        for link_tag in intermediate_links:
            unique_urls.add(link_tag.get('href'))

        downloaded_count = 0
        for intermediate_url in list(unique_urls)[:num_images]:
            if downloaded_count >= num_images:
                break
            
            if not intermediate_url.startswith('http'):
                intermediate_url = urllib.parse.urljoin(main_url, intermediate_url)

            intermediate_response = requests.get(intermediate_url, headers={'User-Agent': 'Mozilla/5.0'})
            intermediate_response.raise_for_status()
            intermediate_soup = BeautifulSoup(intermediate_response.content, 'lxml')

            final_image_link = intermediate_soup.find('a', href=re.compile(r'wp-content/uploads/.*'))

            if not final_image_link:
                print(f"Could not find the final image link on {intermediate_url}. Skipping.")
                continue

            img_url = final_image_link.get('href')
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(intermediate_url, img_url)

            filename = sanitize_filename(os.path.basename(urllib.parse.urlparse(img_url).path))
            image_path = os.path.join(output_directory, filename)
            
            if is_file_downloaded(conn, filename):
                print(f"Skipping {filename}, already in database.")
                continue

            print(f"Downloading {filename}...")
            image_response = requests.get(img_url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            image_response.raise_for_status()
            with open(image_path, "wb") as image_file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    image_file.write(chunk)
            
            add_downloaded_file(conn, filename)
            downloaded_count += 1
            time.sleep(1)

        print(f"{downloaded_count} Spotlight image(s) downloaded!")
    except Exception as e:
        print(f"An error occurred during Spotlight download: {e}")
    

def push_images_to_repo():
    """
    Pushes new images to an existing GitHub repository.
    """
    repo_dir = r"C:\Users\User\Desktop\pythonfiles\BingImages"
    try:
        os.chdir(repo_dir)
        print("Pushing images to GitHub repository...")
        os.system("git add .")
        os.system('git commit -m "Add new images"')
        os.system("git push")
        print("Images pushed to GitHub repository.")
    except FileNotFoundError:
        print(f"Error: Directory '{repo_dir}' not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred during git push: {e}")

# Main execution block
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    output_directory = r"C:\Users\User\Desktop\pythonfiles\BingImages"
    db_path = os.path.join(output_directory, "downloads.db")
    
    conn = setup_database(db_path)

    # Download from Bing
    download_bing_images(output_directory, conn, days=30)
    
    # Download from Windows Spotlight
    download_spotlight_images(output_directory, conn, num_images=10)
    
    # You can get the count from the database to decide if you need to push
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM downloaded_files")
    total_downloaded = cursor.fetchone()[0]

    if total_downloaded > 0:
        push_images_to_repo()
    
    conn.close()
    
    input("Press Enter to close...")
    sys.exit(0)