# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /web-app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask's default port
EXPOSE 5000

# Default command to run the Flask app
CMD ["python", "app.py"]
