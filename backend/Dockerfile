# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY . .

# Seed the database
RUN python -m app.db.seed

# Expose the application port
EXPOSE 8000

# Start FastAPI using the port provided by Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]