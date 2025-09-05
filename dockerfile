FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
RUN useradd -m -u 1000 user
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 --no-install-recommends -y \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*
  
RUN pip install --no-cache-dir gradio opencv-python pandas ultralytics onnx onnxruntime

USER user
WORKDIR /app
COPY --chown=user ./ /app

EXPOSE 1071
CMD ["python", "/app/UI/Main.py"]