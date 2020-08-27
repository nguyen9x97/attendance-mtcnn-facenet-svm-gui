# Realtime Face Recognition - Attendance Management System - User Interface
Face recognition is based on repo: https://github.com/davidsandberg/facenet and https://github.com/nkloi/simple_facenet
## Description
This project uses MTCNN for face detection, pretrained FaceNet model for feature extraction and SVM for classification. The results of face recognition are stored into the `csv` file, depend on `count` variable (for multiple reporting) or confirmation of users (for single reporting). The **User Interface** is built for easy understanding.
## Compatibility
The code is tested using `Tensorflow 1.14` under `Ubuntu 18.04` with `Python 3.5.6`
#### List of libraries for this project:
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
Pretrained model [20180402-114759](https://drive.google.com/file/d/1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz/view) with Inception-Resnet-v1 architecture using the VGGFace2 dataset. Download and extract into `models` folder, result as below:

![model image](https://user-images.githubusercontent.com/55053550/91342893-e4d70a00-e805-11ea-9b9b-3c49316ff493.png)

## Overview of User Interface
Run the GUI by `$ python attendance_gui.py` for **virtual environment** and `$ python3 attendance_gui.py` for **base environment**, result as below:

![gui_overview](https://user-images.githubusercontent.com/55053550/91413973-138cc900-e876-11ea-9366-8dd08e8fa6d8.png)

### 1. Collect dataset
The program uses **MTCNN algorithm** to detect face, then captures (requires only one face) and saves the image to the `your_dataset` folder.
* For collection using android smartphone, download the **IP Webcam** apps in CHPlay and *start server* to get the IP address, then find the ``http://192.168.1.138:8080/video`` in ``utils_gui.py`` file and replace with your own IP address.
* For camera IP, this project uses YooSee camera. Because ``FFMPEG`` **lib** does not support TCP for YooSee Camera, I use the **VLC Player** instead, so the fps is low but the frame is not broken. Replace the ``rtsp://admin:khoinguyen997@192.168.1.148:554/onvif1`` with your  ``rtsp``.
### 2. Training and evaluating
After collecting dataset, use ``Align dataset`` button to crop and align all faces into 182x182 size, the results are saved in the ``face_align`` folder. The dataset of faces_aligned should be checked before training.
#### 2.1 Training
Click the button ``Training/Updating`` to training the model.
#### 2.2 Evaluate
For evaluate, repare the dataset with same structure as the training set, then run ``$ python eval_svm.py``
### 3. Testing
After training model, use the saved model to testing result.
* Face Detection: using local webcam as default, change the ``video_file`` from **None** to your own address for video file.
* Face Recognition: similar to Face Detection.
### 4. Reporting
The confidence is initialized to 0.4, which is the threshold for Face Recognition, you can increase the confidence for reducing false positive.
### 5. Hand report
This option will be used for "hand report" if the system cannot recognize the face.
