# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Ensure the script has executable permissions
RUN chmod +x /app/wait_for_file.sh

# Copy requirements.txt separately for better caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "analyzer.py"]
