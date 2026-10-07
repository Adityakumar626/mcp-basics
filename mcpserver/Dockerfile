FROM python:3.11-slim

# Install uv by copying it from Astral's official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy requirements file
COPY requirements.txt . 

# Create virtual environment and install dependencies
RUN uv venv
RUN uv pip install --no-cache -r requirements.txt 

# Copy application code
COPY server.py .
COPY client-sse.py .
COPY client-stdio.py .

# Expose the port the server runs on
EXPOSE 8050

# Command to run the server
CMD ["uv", "run", "server.py"] 