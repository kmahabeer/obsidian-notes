import requests
import os
import re
import uuid
import sys
from logger import Logger
from datetime import datetime
import time


def extract_header(line):
    header_pattern = r"(#+)\s*(.+)"
    header_match = re.match(header_pattern, line.strip())
    if header_match:
        header_level = len(header_match.group(1))  # Count the number of '#' for level
        header_text = header_match.group(2).strip()  # Extract the text after the '#'
        return header_level, header_text
    return None


# Function to download an image from a URL
def download_image(url, download_folder):
    log.info(f"Starting the image download process from {download_folder}.")

    # Ensure the download folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Extract the file extension from the URL, default to .jpg if no extension is found
    if "." in url.split("/")[-1]:
        extension = os.path.splitext(url.split("/")[-1])[1]
    else:
        extension = ".jpg"  # Default extension if none is found in the URL

    # Generate a random image name
    image_name = f"{uuid.uuid4()}{extension}"
    image_path = os.path.join(download_folder, image_name)

    try:
        log.info(f"Attempting to download {url}")
        # Make the request to download the image
        response = requests.get(url, stream=True)
        log.info(f"Response: {response}")

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            log.info(f"Successfully downloaded: {image_name}")
            return True
        else:
            log.error(
                f"Failed to download {url} - HTTP Status Code: {response.status_code}"
            )
            return False
    except Exception as e:
        log.error(f"Error downloading {url}: {e}")
        return False


# Function to update the markdown files
def update_files(
    download_queue_file="image_downloader/download_queue.md",
    completed_file="image_downloader/completed_downloads.md",
):
    with open(download_queue_file, "r") as f:
        queue_content = f.readlines()

    url_pattern = r"-\s*(https?://\S+)"  # Pattern to match URLs
    # folder_pattern = r"###\s*(.+)"  # Pattern to match H3 folder paths

    # current_folder = None  # Variable to hold the current destination folder
    current_headers = []  # List to store the current hierarchy of headers
    new_queue = []
    completed = []

    for line in queue_content:
        # # Check if the line is an H3 heading (the folder path)
        # folder_match = re.match(folder_pattern, line.strip())
        header_details = extract_header(line)
        if header_details:  # folder_match:
            header_level, header_text = header_details

            if len(current_headers) >= header_level:
                current_headers = current_headers[: header_level - 1]
            current_headers.append(header_text)
            # current_folder = folder_match.group(1).strip()
            log.info(f"Destination folder: {'/'.join(current_headers)}")
            new_queue.append(line)  # Keep heading in the new qu eue
            continue

        # Check if the line contains a URL
        url_match = re.match(url_pattern, line.strip())
        if url_match and current_headers:
            url = url_match.group(1)
            download_folder = os.path.join(*current_headers)
            if download_image(url, download_folder):
                time.sleep(3)
                completed.append(line)  # Add to completed if download succeeds
            else:
                log.error(f"No headers found for URL {url}. Skipping.")
                new_queue.append(line)  # Keep in queue if download fails
        else:
            new_queue.append(line)  # Keep non-URL lines

    # Write updated queue back to the file
    with open(download_queue_file, "w") as f:
        f.writelines(new_queue)

    # Append completed links to the completed file
    with open(completed_file, "a") as f:
        f.writelines(completed)

    log.info("Download queue updated, completed downloads logged.")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    start_time = time.time()
    timestamp_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    script_name = os.path.splitext(os.path.basename(__file__))
    log = Logger(f"logs/{script_name[0]}.log")
    log.info(f"\nStarting {script_name} at {timestamp_start}")

    update_files()

    end_time = time.time()
    timestamp_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = end_time - start_time

    log.info(f"\nEnding {script_name} at {timestamp_end}")
    log.info(f"Script executed in {duration:.2f} seconds.\n")
