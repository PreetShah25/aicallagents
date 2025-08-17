# Multi-purpose image for UI (Streamlit) and API (Flask)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy repo
COPY . /app

# Install Python deps
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install openai twilio flask

# Default command runs Streamlit UI; override in docker-compose for API
EXPOSE 8501 8000
CMD ["streamlit", "run", "src/ace_pro/app/streamlit_app.py", "--server.address=0.0.0.0"]
