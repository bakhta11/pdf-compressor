# Use lightweight Python image
FROM python:3.11-slim

# Install Ghostscript (for PDF compression)
RUN apt-get update && apt-get install -y ghostscript && apt-get clean

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
