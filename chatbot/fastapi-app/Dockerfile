# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install debugging tools
RUN apt-get update && apt-get install -y tree

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create necessary directories and copy files
COPY app/ /app/app/
COPY static/ /app/static/

# Verify file structure
RUN echo "=== Verifying File Structure ===" && \
    tree /app && \
    echo "=== Checking File Permissions ===" && \
    ls -la /app/app && \
    ls -la /app/static

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV PYTHONPATH=/app

# Create a startup verification script
RUN echo '#!/bin/bash\n\
echo "=== Environment Variables ==="\n\
env | grep -E "OPENAI|AZURE|PYTHON|PORT"\n\
echo "=== File Structure ==="\n\
tree /app\n\
echo "=== Starting Application ==="\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Run the startup script
CMD ["/app/start.sh"]