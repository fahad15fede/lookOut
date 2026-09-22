FROM python:3.11-slim

WORKDIR /app

COPY vision/requirements.txt .

# CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ultralytics pulls regular opencv-python.
# Remove both OpenCV variants, then install only headless OpenCV.
RUN pip uninstall -y opencv-python opencv-python-headless && \
    pip install --no-cache-dir opencv-python-headless

COPY vision/src ./src
COPY vision/tests ./tests

CMD ["python", "src/main.py"]