import gradio as gr
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv("config.env")

# Get API Keys from environment variables
CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Imgur API endpoint for image upload
IMGUR_UPLOAD_URL = "https://api.imgur.com/3/image"

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


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


def gradio_upload_images(files):
    """Gradio interface function to upload images directly."""
    if not files:
        return "No files selected."

    links = upload_multiple_images(files)
    return "\n".join(links)


def generate_description(image_url, user_description):
    """Generate a description using the OpenAI API."""
    completion = client.chat.completions.create(
        model="google/gemini-flash-8b-1.5-exp",
        messages=[
            {
                "role": "system",
                "content": """
                You are a QA automation expert tasked with creating Python test scripts for mobile applications based on screenshots. For each screenshot provided:
                1. Analyze the UI elements, features, and functionality visible.
                2. Generate a comprehensive set of test cases covering all major functionality.
                3. Create a Python script using pytest that implements these test cases.
                Your Python script should:
                - Use pytest as the testing framework.
                - Assume the existence of a MobileApp class that represents the app under test.
                - Include setup and teardown methods as needed.
                - Implement each test case as a separate test function.
                - Use descriptive function names prefixed with test_.
                - Include comments explaining the purpose of each test.
                - Use assertions to verify expected outcomes.
                Focus on user interactions, edge cases, and potential error scenarios. Ensure test cases are specific, actionable, and cover both positive and negative testing scenarios.
                Additionally, the user can describe what they want to test in a prompt box. Use this information to tailor the test cases accordingly.
                Respond with a Python script containing the test cases for the given screenshot.
                """,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_description,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
    )

    return completion.choices[0].message.content


def gradio_generate_descriptions(image_urls, user_description):
    """Gradio interface function to generate descriptions for uploaded images."""
    descriptions = []
    for url in image_urls.split("\n"):
        description = generate_description(url, user_description)
        descriptions.append(f"**Image URL:** {url}\n**Description:** {description}\n")

    return "\n".join(descriptions)


# Create the Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Upload Images to Imgur and Generate Descriptions")
    gr.Markdown("Drag and drop images to upload them directly.")
    gr.Markdown("Upload Images First, and Then Generate Descriptions.")

    # Drag-and-drop dialog at the top
    file_input = gr.File(file_count="multiple", label="Drag and Drop Images Here")

    # Upload Images button
    upload_button = gr.Button("Upload Images")

    # Textbox to display uploaded image URLs
    uploaded_urls = gr.Textbox(label="Uploaded Image URLs")

    # Textbox for user to describe what they want to test
    user_description_input = gr.Textbox(label="Describe what you want to test")

    # Generate Descriptions button
    generate_button = gr.Button("Generate Descriptions")

    # Markdown component to display generated descriptions
    descriptions_output = gr.Markdown(label="Generated Descriptions")

    # Connect the components to their respective functions
    upload_button.click(gradio_upload_images, inputs=file_input, outputs=uploaded_urls)
    generate_button.click(
        gradio_generate_descriptions,
        inputs=[uploaded_urls, user_description_input],
        outputs=descriptions_output,
    )

# Launch the interface
iface.launch()
