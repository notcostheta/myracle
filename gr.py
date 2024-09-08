import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables
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


def gradio_add_images(files):
    """Gradio interface function to add images to the list."""
    if not files:
        return "No files selected."

    # Store the paths of the selected files in a global list
    global image_paths
    image_paths.extend(files)

    return f"Added {len(files)} images to the list."


def gradio_upload_images():
    """Gradio interface function to upload all stored images."""
    global image_paths
    if not image_paths:
        return "No images to upload."

    links = upload_multiple_images(image_paths)
    image_paths = []  # Clear the list after uploading
    return "\n".join(links)


# Initialize the list to store image paths
image_paths = []

# Create the Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Upload Images to Imgur")
    gr.Markdown("Drag and drop images to add them to the upload list.")
    gr.Markdown("Add Images First, Then Click Upload Images.")

    # Drag-and-drop dialog at the top
    file_input = gr.File(file_count="multiple", label="Drag and Drop Images Here")

    # Add Images button
    add_images_button = gr.Button("Add Images")

    # Status textbox
    output_text = gr.Textbox(label="Upload Status")

    # Upload Images button
    upload_button = gr.Button("Upload Images")

    # Connect the components to their respective functions
    add_images_button.click(gradio_add_images, inputs=file_input, outputs=output_text)
    upload_button.click(gradio_upload_images, outputs=output_text)

# Launch the interface
iface.launch()
