import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="keras-ocr",
    version="1.0.0",
    description="A packaged and flexible version of the CRAFT text detector and Keras CRNN recognition model.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Fausto Morales, Seyoung Park",
    author_email="seyoung.arts.park@protonmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["keras_ocr"],
    include_package_data=True,
    install_requires=[
      'essential_generators',
      'tqdm',
      'imgaug',
      'validators',
      'fonttools',
      'editdistance',
      'pyclipper',
      'shapely',
      # 'efficientnet==1.0.0',    # Needed for detection.py
      'keras',
      'numpy',
      'yapf',
      'tensorflow==2.3.1',
      'h5py<=2.10.0',
      'Pillow==7.1.0',
    ],
)
