FROM tensorflow/tensorflow:2.4.1-gpu

# First three is needed for OpenCV. https://stackoverflow.com/a/63377623
RUN apt update && apt install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    less \
    ranger

# Avoid re-downloading weights when other things
# change.
RUN mkdir -p /root/.keras-ocr && ( \
    cd /root/.keras-ocr && \
    curl -L -o craft_mlt_25k.h5 https://github.com/faustomorales/keras-ocr/releases/download/v0.8.4/craft_mlt_25k.h5 && \
    curl -L -o crnn_kurapan.h5 https://github.com/faustomorales/keras-ocr/releases/download/v0.8.4/crnn_kurapan.h5 \
    )

# setup.cfg
RUN pip install \
    essential_generators \
    tqdm \
    imgaug \
    validators \
    fonttools \
    editdistance \
    pyclipper \
    shapely \
    efficientnet==1.0.0

# Pipfile
RUN pip install \
    pandas \
    ipython \
    jupyterlab \
    numpy \
    matplotlib \
    keras \
    mypy \
    pylint \
    pytest \
    pytest-cov \
    yapf \
    scikit-learn \
    sphinx==1.8.3 \
    m2r==0.2.1 \
    'h5py<=2.10.0' \
    Pillow==7.1.0 \
    jedi==0.17.2
# We need Pillow because of https://github.com/pytorch/vision/issues/1714

# Makefile
RUN pip uninstall opencv-python -y \
    && pip install --no-cache-dir opencv-contrib-python-headless

RUN pip install tensorboard

COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]

WORKDIR /usr/src

ENV LC_ALL C