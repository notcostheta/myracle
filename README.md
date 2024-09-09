# Automated Test Generation Tool (Myracle Takehome)

This tool allows you to upload images to Imgur and generate detailed descriptions for each image using the OpenRouter API. The generated descriptions are tailored for creating Python test scripts for mobile applications based on the provided screenshots.
> It's really half baked right now, though in the real world, we'll probably not be using gradio, so I was focused more on generating structured jsons instead of a pretty UI.
> And I've only spent like 3 hours on this.


## Features

- **Image Upload**: Upload multiple images to Imgur directly from the Gradio interface.
- **Structured Responses**: Receive json responses with detailed descriptions for each uploaded image.
- **Telemetry** : The tool logs the image upload and description generation requests which can be stored in a document database.
- **Plug-and-Play**: Can switch between different AI models, since we are using OpenRouterAPI.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system.
- An Imgur account and API keys.
- An OpenRouter account and API keys.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/notcostheta/myracle.git
   cd myracle
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up your API keys**:
   - Create a file named `config.env` in the root directory of the project.
   - Add your Imgur and OpenAI API keys to the `config.env` file:
     ```env
     IMGUR_CLIENT_ID=your_imgur_client_id
     IMGUR_CLIENT_SECRET=your_imgur_client_secret
     OPENROUTER_API_KEY=your_openai_api_key
     ```

2. **Source the environment variables**:
   - Ensure the environment variables are loaded correctly by running:
     ```bash
     source config.env
     ```

## Usage

1. **Launch the Gradio interface**:
   ```bash
   python app.py
   ```

2. **Upload Images**:
   - Drag and drop images into the designated area in the Gradio interface.
   - Click the "Upload Images" button to upload the images to Imgur.
   - The uploaded image URLs will be displayed in the "Uploaded Image URLs" textbox.

3. **Generate Descriptions**:
   - Enter a description of what you want to test in the "Describe what you want to test" textbox.
   - Click the "Generate Descriptions" button to generate descriptions for the uploaded images.
   - The generated test casese reponse will be displayed in the "Generated Descriptions" section.
