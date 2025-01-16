# chatWithPDF
This project allows you to upload a PDF document and ask questions about its content. It uses LangChain, OpenAI Embeddings, GPT-4, and the Facebook AI Similarity Search (FAISS) library to process the text in the PDF and provide answers to questions related to the document.

## Project Screen
![image](https://github.com/user-attachments/assets/17fef864-764e-453e-8bcc-fbc1365fa8a0)

## Installation

### Option 1: Run the App Locally (Without Docker)

1. Clone the repository:

   ```shell
   git clone https://github.com/john-thuo1/chatWithPDF
   cd chatWithPDF
   ```

2. Create a Virtual Environment:

    ```shell
    python -m venv env
    ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Create an OpenAI API Key and add it to your `.env` file:
   [OpenAI Platform](https://platform.openai.com/)
   ```shell
   OPENAI_API_KEY="your-secret-key"
   ```

5. Run the application:

   ```shell
   streamlit run App.py
   ```

### Option 2: Run the App Using Docker

1. **Clone the repository**:

   ```shell
   git clone https://github.com/john-thuo1/chatWithPDF
   cd chatWithPDF
   ```

2. **Build the Docker image**:

   First, ensure you have Docker installed and running on your system. Then, use the following command to build the image from the Dockerfile:

   ```shell
   docker-compose build
   ```

3. **Run the app with Docker**:

   After the build is complete, you can run the app in a container using Docker Compose:

   ```shell
   docker-compose up
   ```

   This will start the app and map port `8501` from the container to the host machine. The application will be available at `http://localhost:8501`.

4. **(Optional) Set up your OpenAI API Key**:

   If you're using Docker, you can set your OpenAI API Key using environment variables. Either:

   - Use a `.env` file (uncomment the `env_file` section in the `docker-compose.yml`).
   - Alternatively, pass the environment variable manually at runtime:
     ```shell
     OPENAI_API_KEY=your-secret-key docker-compose up
     ```

   You can also store the OpenAI API key in your `.env` file and ensure the file is loaded with the Docker Compose configuration.
