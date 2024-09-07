import requests
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv("config.env")

CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")

# Imgur API endpoint for image upload
IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"


def upload_image_to_imgur(image_path):
    """Upload a single image to Imgur."""
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}

    with open(image_path, "rb") as image_file:
        response = requests.post(
            IMGUR_UPLOAD_URL, headers=headers, files={"image": image_file}
        )

    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        print(f"Failed to upload image: {response.status_code}")
        return None


def upload_multiple_images(image_paths):
    """Upload multiple images to Imgur."""
    uploaded_links = []

    for image_path in image_paths:
        link = upload_image_to_imgur(image_path)
        if link:
            uploaded_links.append(link)

    return uploaded_links


if __name__ == "__main__":
    # List of image paths to upload
    image_paths = ["images/01.jpg", "images/02.jpg"]

    # Upload images
    links = upload_multiple_images(image_paths)

    # Print the links of the uploaded images
    for link in links:
        print(f"Uploaded image link: {link}")
