# Lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install the Python libraries
# We use --no-cache-dir to keep the container size small
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the Hugging Face model during the build
# This adds the model directly into the image so it doesn't download on every startup
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', top_k=None)"

# Copy the actual application code into the container
COPY app.py .

# Expose the port that Hugging Face expects
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]

