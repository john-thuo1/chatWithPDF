# DocuChat AI
This project allows users to upload PDF documents and ask questions about their content. 

## Project Screen
![image](https://github.com/user-attachments/assets/6e6c1810-5729-4e59-83a0-5518c7538b74)


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

4. Create your own OpenAI API Key
   [OpenAI Platform](https://platform.openai.com/) . You will be prompted to enter it in the application.
   ```shell
   OPENAI_API_KEY="your-secret-key"
   ```

5. Run the application:

   ```shell
   streamlit run App.py
   ```
