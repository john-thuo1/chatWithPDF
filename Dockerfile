FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory 
WORKDIR /chat_app

# Change ownership of the working directory to the non-root user
RUN useradd -m -u 1000 user && chown -R user:user /chat_app

USER user

# Add user-local bin directory to PATH
ENV PATH="/home/user/.local/bin:$PATH"

COPY requirements.txt /chat_app/
RUN pip install -r requirements.txt

COPY . /chat_app/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Use the correct path for Linux containers (bin directory)
ENTRYPOINT [ "streamlit", "run", "App.py", "--server.port=8501"]
