import os
from huggingface_hub import hf_hub_download, login, logout


def DownloadHFModel(repo_id, file_name):
    login(os.environ["hf_read_model"])
    hf_hub_download(repo_id=repo_id, filename=file_name, local_dir="./Weight")
    logout()

if "__main__" == __name__:
    # Download Model
    REPO_ID = "blitzkrieg0000/yolov7_fault-detection"
    MODEL_FILE = "yolov7_ariza.onnx"
    DownloadHFModel(REPO_ID, MODEL_FILE)