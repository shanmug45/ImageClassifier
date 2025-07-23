FROM tensorflow/tensorflow:latest
WORKDIR /app
COPY model_P3.h5 /app
COPY Model_Test.py /app
COPY output_ela.jpg /app
RUN apt-get install -your python3-opencv
RUN pip install --no-cache-dir opencv-python
RUN pip install --no-cache-dir pillow
CMD ["python", "Model_Test.py"]
