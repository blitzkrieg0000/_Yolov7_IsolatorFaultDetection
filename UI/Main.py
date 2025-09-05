import os
import sys
sys.path.append(os.getcwd())

from Lib.Const import COLOR_MAP, LABELS
from Lib.DetectFaultOnnx import DetectFaults

import cv2
import gradio as gr

demoImages = [
    "data/DJI_20240905095004_0007_W.JPG",
    "data/DJI_20240905091530_0003_W.JPG",
    "data/DJI_20240905094647_0003_W.JPG",
    "data/DJI_20240905094647_0003_Z.JPG",
    "data/DJI_20240905101846_0005_W.JPG",
    "data/16_3450.png", 
    "data/16_3735.png",
    "data/16_3900.png",
    "data/19_00350.png",
    "data/25_00272.png",
    "data/67_02661.png"
]


def Warning():
    gr.Info("DGH ARGE YAZILIM DANIŞMANLIK ENERJİ İNŞAAT SAN.TİC.LTD.ŞTİ", duration=0.5)

with gr.Blocks(css="footer{display:none !important}") as block:
    gr.Markdown("## Yüksek Gerilim Hattı İzolatörlerinin Arıza Tespiti - Demo")
    gr.Markdown("**Ark İzi, Kırık ve Eksik İzolatör Hatalarını Tespit Eder**")
    with gr.Row():
        with gr.Column():
            inputImage = gr.Image(label="Fotoğraf")

        with gr.Column():
            thresholdSlider = gr.Slider(0, 1, value=0.25, label="Model Eşik Değeri", info="0 ve 1 arası seçiniz.")
            iouThresholdSlider = gr.Slider(0, 1, value=0.45, label="IOU (Intersection Over Union) Eşik Değeri", info="0 ve 1 arası seçiniz.")
            with gr.Accordion("Demo Görsellerden Seçebilirsiniz", open=False):
                imageGallery = gr.Examples(
                    examples=[
                        os.path.join("data", img_name) for img_name in sorted(os.listdir("data"))
                    ],
                    inputs=[inputImage],
                    label="Örnekler",
                    cache_examples=False,
                    examples_per_page=7
                )
            processButton = gr.Button("Tespit Et")

    results = gr.Textbox(label="Log")
    gr.HTML("</hr>")
    processedImageGallery = gr.Gallery(
        label="Sonuçlar",
        rows=1, 
        columns=2, 
        object_fit="contain", 
        height="auto"
    )

    annotatedImage = gr.AnnotatedImage(color_map=COLOR_MAP)

    @processButton.click(outputs=[processedImageGallery, annotatedImage, results], inputs=[inputImage, thresholdSlider, iouThresholdSlider])
    def Process(image, model_threshold, iouThresholdSlider):
        if image is None:
            raise gr.Warning("Lütfen görüntü yükleyiniz veya hazır seçiniz!", duration=3)
        
        img0, boxes, labels = DetectFaults(image, model_threshold, iouThresholdSlider)

        if len(boxes) == 0:
            raise gr.Error("Bir Hata ile Karşılaşıldı: Görüntüde Tespit Yapılamadı 💥!", duration=5)

        sections = []
        for b, c in zip(boxes, labels):
            sections+=[(b, LABELS[c])]

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return [img0], (image, sections), "Görüntü İşlendi!"
  
    block.load(Warning)


block.queue(max_size=10)
block.launch(server_name="0.0.0.0", server_port=1071)

