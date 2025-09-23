import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib.parse
import time

def sanitize_filename(name):
    """
    Sanitizes a string to be a valid filename by removing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*\']', '', name).strip()

def download_bing_images(output_directory, days=30):
    """
    Downloads images from the Bing Image Archive API.
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
        global count
        count = 0
        for image in images_data:
            image_url = base_url + image["url"]
            image_title = sanitize_filename(image.get("title", "").replace(" ", "_") or "bing_image")
            image_path = os.path.join(output_directory, f"{image_title}.jpg")

            if os.path.exists(image_path):
                continue

            print(f"Downloading {image_title}...")
            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status()
            with open(image_path, "wb") as image_file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    image_file.write(chunk)
            
            count += 1

        print(f"{count} Bing Image(s) Downloaded!")
    except Exception as e:
        print(f"An error occurred during Bing download: {e}")

def download_spotlight_images(output_directory, num_images=10):
    """
    Scrapes and downloads images from windows10spotlight.com by navigating to
    an intermediate page and then finding the final image link.
    """
    main_url = "https://windows10spotlight.com/"
    os.makedirs(output_directory, exist_ok=True)

    try:
        # Step 1: Get the main page to find links to the intermediate image pages
        # print(f"Fetching main page: {main_url}")
        response = requests.get(main_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        # Find all <a> tags that contain "/images/" in their href
        intermediate_links = soup.find_all('a', href=re.compile(r'images/'))
        if not intermediate_links:
            print("Could not find intermediate image links on the main page.")
            return

        # Use a set to store unique intermediate URLs to avoid duplicates
        unique_urls = set()
        for link_tag in intermediate_links:
            unique_urls.add(link_tag.get('href'))

        global downloaded_count
        downloaded_count = 0
        for intermediate_url in list(unique_urls)[:num_images]:
            if downloaded_count >= num_images:
                break
            
            if not intermediate_url.startswith('http'):
                intermediate_url = urllib.parse.urljoin(main_url, intermediate_url)

            # print(f"Navigating to intermediate page: {intermediate_url}")
            intermediate_response = requests.get(intermediate_url, headers={'User-Agent': 'Mozilla/5.0'})
            intermediate_response.raise_for_status()
            intermediate_soup = BeautifulSoup(intermediate_response.content, 'lxml')

            # Step 2: Find the final image link on the intermediate page
            final_image_link = intermediate_soup.find('a', href=re.compile(r'wp-content/uploads/.*'))

            if not final_image_link:
                print(f"Could not find the final image link on {intermediate_url}. Skipping.")
                continue

            img_url = final_image_link.get('href')
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(intermediate_url, img_url)

            img_title = sanitize_filename(os.path.basename(urllib.parse.urlparse(img_url).path))
            image_path = os.path.join(output_directory, img_title)

            if os.path.exists(image_path):
                # print(f"Skipping {img_title}, already downloaded.")
                continue
            
            # print(f"Downloading {img_title} from {img_url}...")
            image_response = requests.get(img_url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            image_response.raise_for_status()
            with open(image_path, "wb") as image_file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    image_file.write(chunk)
            
            # print(f"Successfully downloaded {img_title}.")
            downloaded_count += 1
            time.sleep(1) # Be polite to the server

        print(f"{downloaded_count} Spotlight image(s) downloaded!")
    except Exception as e:
        print(f"An error occurred during Spotlight download: {e}")
    

def push_images_to_repo():
    """
    Pushes new images to an existing GitHub repository.
    NOTE: This assumes a Git repository has already been initialized in the directory.
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

    # Download from Bing
    download_bing_images(output_directory, days=30)
    
    # Download from Windows Spotlight
    download_spotlight_images(output_directory, num_images=10)
    if count != 0  or downloaded_count != 0:
        # Push to GitHub
        push_images_to_repo()
    input("Press Enter to close...")
    sys.exit(0)
