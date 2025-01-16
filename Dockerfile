FROM python:3.12.3-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /chat_app

COPY requirements.txt /chat_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /chat_app/


EXPOSE 8501

CMD ["streamlit", "run", "App.py"]
