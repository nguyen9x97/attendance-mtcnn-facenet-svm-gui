# Realtime Face Recognition - Attendance Management System - User Interface
Face recognition is based on repo: https://github.com/davidsandberg/facenet and https://github.com/nkloi/simple_facenet
## Description
This project uses MTCNN for face detection, pretrained FaceNet model for feature extraction and SVM for classification. The results of face recognition are stored into the `csv` file, depend on `count` variable (for multiple reporting) or the confirmation (for single reporting). The **User Interface** is built for easy understanding.
## Compatibility
The code is tested using Tensorflow 1.14 under Ubuntu 18.04 with Python 3.5.6
#### List of library for this project:
* tensorflow==1.14
* scipy==1.1.0
* scikit-learn
* opencv-python
* h5py
* matplotlib
* Pillow
* requests
* psutil
* pandas
* vlc
## Installation
### 1. Install requirements
For installing the packages, use `pip install -r requirements.txt`
### 2. Download the pretrained model
Pretrained model [20180402-114759](https://drive.google.com/file/d/1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz/view) with architecture Inception-Resnet-v1 using the VGGFace2 dataset. Download and extract into `models` directory, result as below:

![model image](https://user-images.githubusercontent.com/55053550/91342893-e4d70a00-e805-11ea-9b9b-3c49316ff493.png)

## Overview of User Interface
Run the GUI by
