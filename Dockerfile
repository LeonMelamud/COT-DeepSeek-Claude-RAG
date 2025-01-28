FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy necessary files for installation
COPY pyproject.toml README.md ./

# Copy the application code
COPY rat/ rat/
COPY web/ web/
COPY rat_claude.py .

# Create uploads directory
RUN mkdir -p uploads

# Install the package and dependencies
RUN pip install --no-cache-dir .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=web.app

# Expose port for web interface
EXPOSE 5000

# Command to run the application
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--reload"]
