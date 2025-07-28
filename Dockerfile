FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Add retry + timeout flags to pip
RUN pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

COPY app/ app/
COPY input/ input/
COPY output/ output/

# Create output directory if it doesn't exist
RUN mkdir -p output

CMD ["python", "app/main.py", "Student", "Summarize key concepts from chemistry notes"]
