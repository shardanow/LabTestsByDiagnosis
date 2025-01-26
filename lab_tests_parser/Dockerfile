FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "parser.py"]
