FROM tensorflow/tensorflow:2.4.1-gpu

# First three is needed for OpenCV. https://stackoverflow.com/a/63377623
RUN apt update && apt install -y \
    ffmpeg=3.4.8-0ubuntu0.2 \
    libsm6 \
    libxext6 \
    less \ 
    exiftool

# Avoid re-downloading weights when other things
# change.
RUN mkdir -p /root/.keras-ocr && ( \
    cd /root/.keras-ocr && \
    curl -L -o craft_mlt_25k.h5 https://github.com/faustomorales/keras-ocr/releases/download/v0.8.4/craft_mlt_25k.h5 && \
    curl -L -o crnn_kurapan.h5 https://github.com/faustomorales/keras-ocr/releases/download/v0.8.4/crnn_kurapan.h5 \
    )

WORKDIR /tmp
COPY ./requirements.txt /tmp
RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]

WORKDIR /usr/src

ENV LC_ALL C