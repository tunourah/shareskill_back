# Base image
FROM python:3.9

# Set working directory
WORKDIR /usr/src/backend

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all application files
COPY . .

# Expose application port (for local testing only)
EXPOSE 8000

# Start with gunicorn on the correct port Render assigns
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT"]
