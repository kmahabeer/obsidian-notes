import requests
import os
import re
import uuid


def generate_random_name(extension):
    return f"{uuid.uuid4()}{extension}"


# Function to download an image from a URL
def download_image(url, download_folder):
    # Ensure the download folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Extract the file extension from the URL, default to .jpg if no extension is found
    if "." in url.split("/")[-1]:
        extension = os.path.splitext(url.split("/")[-1])[1]
    else:
        extension = ".jpg"  # Default extension if none is found in the URL

    # Generate a random image name
    image_name = "img-" + generate_random_name(extension)
    image_path = os.path.join(download_folder, image_name)

    try:
        print(f"Attempting to download {url}")
        # Make the request to download the image
        response = requests.get(url, stream=True)
        print(response)
        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Successfully downloaded: {image_name}")
            return True
        else:
            print(
                f"Failed to download {url} - HTTP Status Code: {response.status_code}"
            )
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


# Function to update the markdown files
def update_files(
    download_queue_file="download_queue.md", completed_file="completed_downloads.md"
):
    with open(download_queue_file, "r") as f:
        queue_content = f.readlines()

    url_pattern = r"-\s*(https?://\S+)"  # Pattern to match URLs
    folder_pattern = r"###\s*(.+)"  # Pattern to match H3 folder paths

    current_folder = None  # Variable to hold the current destination folder
    new_queue = []
    completed = []

    for line in queue_content:
        # Check if the line is an H3 heading (the folder path)
        folder_match = re.match(folder_pattern, line.strip())
        if folder_match:
            current_folder = folder_match.group(1).strip()
            print(f"Destination folder: {current_folder}")
            new_queue.append(line)  # Keep heading in the new qu eue
            continue

        # Check if the line contains a URL
        url_match = re.match(url_pattern, line.strip())
        if url_match and current_folder:
            url = url_match.group(1)
            if download_image(url, current_folder):
                completed.append(line)  # Add to completed if download succeeds
            else:
                new_queue.append(line)  # Keep in queue if download fails
        else:
            new_queue.append(line)  # Keep non-URL lines

    # Write updated queue back to the file
    with open(download_queue_file, "w") as f:
        f.writelines(new_queue)

    # Append completed links to the completed file
    with open(completed_file, "a") as f:
        f.writelines(completed)

    print("Download queue updated, completed downloads logged.")


# Run the function
update_files()
