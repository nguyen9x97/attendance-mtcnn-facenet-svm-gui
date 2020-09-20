import cv2
import os
import numpy as np
from facenet.face_contrib import *
from align.align_mtcnn import *
from train_svm_gui import *
import time
import vlc
import re
import shutil
from tkinter import messagebox
import pandas as pd
from tkinter import Toplevel

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def add_complete_percent(frame, count, faces):
    if faces is not None:
        for face in faces:
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (255, 255, 0), 2)
    cv2.putText(frame, str(count) + "%", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                thickness=3, lineType=2)

def add_student_camip(name_id, dirpath, camera_http='rtsp://admin:khoinguyen997@192.168.1.148:554:554/onvif1'):
    #Because FFMPEG does not support tcp for Yoosee Camera, uses vlc library instead
    player = vlc.MediaPlayer(camera_http)
    player.video_set_scale(0.25)
    face_detection = Detection()
    countt = 1
    player.play()
    time.sleep(3)
    start = time.time()
    while True:
        player.video_take_snapshot(0, dirpath + '/' + name_id + '_' + str(countt).zfill(4) + '.png', 0, 0)
        # player.video_take_snapshot(0, './images/snapshot{0}.tmp.png'.format(count), 1920, 1080)
        frame = cv2.imread(dirpath + '/' + name_id + '_' + str(countt).zfill(4) + '.png')

        faces = face_detection.find_faces(frame)
        add_complete_percent(frame, countt, faces)
        if len(faces) == 1:
            countt += 1
        # cv2.imshow('frame', frame)
        frame75 = rescale_frame(frame, percent=75)
        cv2.imshow('camip', frame75)
        if countt > 100:
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
    player.stop()
    end = time.time()
    total_minute = (end - start) / 60
    print('Add face data excecution time: ' + str(end - start) + ' second')
    print('Total minutes:', total_minute)
    cv2.destroyAllWindows()
    messagebox.showinfo("Information", "The collection is complete \n" + "Collection excecution time: " + str(
        format(end - start, ".2f")) + "s")

def add_student_webcam_android(name, id, camera, android_http="http://192.168.1.138:8080/video"):
    name_id = name + "_" + id
    path = os.getcwd()
    path_face = os.path.join(path, 'your_dataset')

    if not os.path.exists(path_face):
        os.mkdir(path_face)

    dirpath = os.path.join(path_face, name_id)

    try:
        os.mkdir(dirpath)
    except:
        #print('Directory already exist:', name_id)
        messagebox.showerror("Error collecting", name_id + " already exists!")
        return
    else:
        print("Successfully created directory:", name_id)

    count = 1

    # Start collect images
    if camera == "camip":
        add_student_camip(name_id, dirpath)
        return
    elif camera == "webcam":
        cap = cv2.VideoCapture(0)
    else:
        # Use ip webcam for android
        cap = cv2.VideoCapture(android_http)
    face_detection = Detection()
    start = time.time()
    while True:
        ret, frame = cap.read()
        faces = face_detection.find_faces(frame)
        # frame50 = rescale_frame(frame, percent=50)
        if len(faces) == 1:
            cv2.imwrite(dirpath + '/' + name_id + '_' + str(count).zfill(4) + '.jpg', frame)
            count += 1
        add_complete_percent(frame, count, faces)
        if camera == "webcam":
            cv2.imshow('webcam', frame)
        else:
            frame75 = rescale_frame(frame, percent=75)
            cv2.imshow('android', frame75)
        if count > 100:
            break
        elif cv2.waitKey(1) == ord('q'):  # 50 = 200 anh
            break

    cap.release()
    end = time.time()
    total_minute = (end - start) / 60
    print('Add face data excecution time: ' + str(end - start) + ' second')
    print('Total minutes:', total_minute)
    cv2.destroyAllWindows()
    messagebox.showinfo("Information", "The collection is complete \n" + "Collection excecution time: " + str(
        format(end - start, ".2f")) + "s")

def align_faces():
    start = time.time()
    align_mtcnn('your_dataset', 'face_align')
    end = time.time()
    #total_minute = (end - start) / 60
    #print('Aligning excecution time: ' + str(end - start) + ' second')
    #print('Total minutes:', total_minute)
    messagebox.showinfo("Information", "The alignment is complete \n" + "Aligning excecution time: " + str(format(end-start, ".2f")) + "s")

def training_svm():
    start = time.time()
    train('face_align/', 'models/20180402-114759.pb', 'models/your_model.pkl')
    end = time.time()
    #total_minute = (end - start) / 60
    #print('Training excecution time: ' + str(end - start) + ' second')
    #print('Total minutes:', total_minute)
    messagebox.showinfo("Information", "Your training is complete \n" + "Training excecution time: " + str(
        format(end - start, ".2f")) + "s")

def remove_student(name, id):
    name_id = name + "_" + id
    path = os.getcwd()
    path_face = os.path.join(path, 'your_dataset')
    path_face_align = os.path.join(path, 'face_align')
    dirpath = os.path.join(path_face, name_id)
    dirpath_align = os.path.join(path_face_align, name_id)
    try:
        shutil.rmtree(dirpath)
        shutil.rmtree(dirpath_align)
    except:
        #print('Directory does not exist:', name_id)
        messagebox.showerror("Error removing", name_id + " does not exists!")
    else:
        #print("Successfully removed directory:", name_id)
        messagebox.showinfo("Information", "Successfully removed directory: " + name_id)

def add_overlays_detection_test(frame, frame_rate, faces):
    if faces is not None:
        for face in faces:
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (255, 255, 0), 2)
    cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def face_detection_test(video_file = None, output_file = None):
    # Set record file
    #video_file = None
    #output_file = None

    if video_file is not None:
        cap = cv2.VideoCapture(video_file)
    else:
        cap = cv2.VideoCapture(0)
    face_detection = Detection()

    # Set fps
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    ret, frame = cap.read()
    width = frame.shape[1]
    height = frame.shape[0]
    if output_file is not None:
        video_format = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, video_format, 20, (width, height))

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if (frame_count % frame_interval) == 0:
            faces = face_detection.find_faces(frame)
            # print(len(faces))
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0
        add_overlays_detection_test(frame, frame_rate, faces)
        frame_count += 1
        if video_file is not None:
            frame75 = rescale_frame(frame, percent=75)
            cv2.imshow('Video', frame75)
        else:
            cv2.imshow('Video', frame)
        if output_file is not None:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if output_file is not None:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

def add_overlays_recog_test(frame, faces, frame_rate, colors, confidence=0.4):
    if faces is not None:
        for idx, face in enumerate(faces):
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
            if face.name and face.prob:
                if face.prob > confidence:
                    class_name = face.name
                else:
                    class_name = 'Unknown'
                    # class_name = face.name
                cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            colors[idx], thickness=3, lineType=2)
                cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[idx], thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def face_recognition_test(model_checkpoint = 'models', classifier = 'models/your_model.pkl', video_file = None, output_file = None):
    #Set confidence
    confidence = 0.4

    # Set model
    #model_checkpoint = 'models'
    #classifier = 'models/your_model.pkl'
    #video_file = None
    #output_file = None

    # Set fps
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    if video_file is not None:
        video_capture = cv2.VideoCapture(video_file)
    else:
        # Use internal camera
        video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    width = frame.shape[1]
    height = frame.shape[0]
    if output_file is not None:
        video_format = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, video_format, 20, (width, height))
    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays_recog_test(frame, faces, frame_rate, colors, confidence= confidence)

        frame_count += 1
        if video_file is not None:
            frame75 = rescale_frame(frame, percent=75)
            cv2.imshow('Video', frame75)
        else:
            cv2.imshow('Video', frame)
        if output_file is not None:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    if output_file is not None:
        out.release()
    video_capture.release()
    cv2.destroyAllWindows()

def face_recognition_camip(model_checkpoint = 'models', classifier = 'models/your_model.pkl', camip_http = 'rtsp://admin:khoinguyen997@192.168.1.148:554/onvif1'):
    # Set confidence
    confidence = 0.4

    # Set fps
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    # Set VLC
    player = vlc.MediaPlayer(camip_http)
    player.video_set_scale(0.25)

    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))

    player.play()
    time.sleep(3)

    while True:
        # Capture frame-by-frame
        player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)
        frame = cv2.imread('.snapshot.tmp.png')

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays_recog_test(frame, faces, frame_rate, colors, confidence=confidence)
        frame_count += 1
        frame75 = rescale_frame(frame, percent=75)
        cv2.imshow('Video', frame75)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    player.stop()

def add_to_csv(student_name, csv_name):
    name = re.findall('.+[A-z]', student_name)
    mssv = re.findall('[0-9]+', student_name)
    mssv = [int(i) for i in mssv]
    #csv_name = 'test_8.csv'
    path = os.getcwd()
    path_csv = os.path.join(path, 'my_csv_reported')
    if not os.path.exists(path_csv):
        os.mkdir(path_csv)
    path_csv_file = os.path.join(path_csv, csv_name)
    try:
        student_df = pd.read_csv(path_csv_file, index_col=0)
    except:
        student_df = pd.DataFrame()
        student_df['MSSV'] = mssv
        student_df['Ho Ten'] = name
        student_df.index = np.arange(1, len(student_df) + 1)
        student_df.to_csv(path_csv_file)

    if len(student_df) >= 1:
        if int(mssv[0]) not in student_df['MSSV'].values:
            student_df.loc[len(student_df)+1] = [mssv[0], name[0]]
            student_df.to_csv(path_csv_file)

def add_multi_to_csv(names_dict, csv_name):
    for name in names_dict:
        add_to_csv(name, csv_name)

def add_csv_with_count(names_dict, csv_name, count_threshold):
    for name, count in names_dict.items():
        if count > count_threshold:
            add_to_csv(name, csv_name)

def add_overlays_webcam_report(frame, faces, frame_rate, colors, confidence=0.4):
    if faces is not None:
        for idx, face in enumerate(faces):
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
            if face.name and face.prob:
                if face.prob > confidence:
                    class_name = face.name
                else:
                    class_name = 'Unknown'
                    # class_name = face.name
                cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            colors[idx], thickness=3, lineType=2)
                cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[idx], thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    #cv2.putText(frame, 'Number of students: ' + str(len(lst_student)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                #(233, 53, 57), thickness=3, lineType=2)

    if len(faces) != 1:
        cv2.putText(frame, "Require only one face", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255),
                    thickness=2, lineType=2)

def create_blank_image(width, height, rgb_color=(255, 255, 255)):
    image = np.zeros((height, width, 3), np.uint8)

    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def add_to_blank_frame(image, lst_student):
    cv2.putText(image, 'Number of students: ' + str(len(lst_student)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 0, 0), thickness=2, lineType=2)
    count = 80
    for index, name in lst_student:
        cv2.putText(image, str(index) + '. ' + name, (10, count), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), thickness=2,
                    lineType=1)
        count += 30

def report_webcam_csv(csv_name, confidence, model_checkpoint = 'models', classifier = 'models/your_model.pkl', video_file = None, output_file = None):
    start_1 = time.time()
    global lst_student
    lst_student = []
    time_per_student = []

    # Set fps
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    if video_file is not None:
        video_capture = cv2.VideoCapture(video_file)
    else:
        # Use internal camera
        video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    width = frame.shape[1]
    height = frame.shape[0]
    if output_file is not None:
        video_format = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, video_format, 20, (width, height))
    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        image_1 = create_blank_image(500, height)

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays_webcam_report(frame, faces, frame_rate, colors, confidence=confidence)

        frame_count += 1

        # Want to save?
        if len(faces) == 1:
            if faces[0].prob > confidence:
                if faces[0].name not in lst_student:
                    start_rp = time.time()
                    top_resp = Toplevel()
                    top_resp.after(3000, top_resp.destroy)
                    #print(faces[0].name)
                    #print(type(faces[0].name)): string
                    #response = messagebox.askyesno("Face detected", faces[0].name + "\n" + "Want to save?")
                    response = messagebox.askyesno("Face detected", faces[0].name, parent=top_resp, default="yes")
                    if response:
                        top_resp.destroy()
                        lst_student.append(faces[0].name)
                        add_to_csv(faces[0].name, csv_name)
                        end_rp = time.time()
                        print("Time per student:", end_rp - start_rp)
                        time_per_student.append(end_rp-start_rp)

        if len(lst_student) >= 1:
            if len(lst_student) > 5:
                add_to_blank_frame(image_1, list(enumerate(lst_student, start=1))[-5:])
            else:
                add_to_blank_frame(image_1, list(enumerate(lst_student, start=1)))

        if video_file is not None:
            frame75 = rescale_frame(frame, percent=75)
            cv2.imshow('Video', frame75)
        else:
            final = cv2.hconcat([frame, image_1])
            #cv2.imshow('Video', frame)
            cv2.imshow('Video', final)
        if output_file is not None:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    if output_file is not None:
        out.release()
    video_capture.release()
    cv2.destroyAllWindows()
    end_1 = time.time()
    print("Time per student:", time_per_student)
    print('Total Execute time:', end_1 - start_1)

def add_overlays_android_report(frame, faces, frame_rate, colors, confidence=0.5):
    if faces is not None:
        for idx, face in enumerate(faces):
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
            if face.name and face.prob:
                if face.prob > confidence:
                    class_name = face.name
                else:
                    class_name = 'Unknown'
                    # class_name = face.name
                if class_name != 'Unknown':
                    names_dict[class_name] = names_dict.get(class_name, 0) + 1
                cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            colors[idx], thickness=3, lineType=2)
                cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors[idx], thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)
    cv2.putText(frame, 'Number of students: ' + str(len(names_dict)), (120, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (233, 53, 57), thickness=3, lineType=2)
    count = 80
    for name, dem in names_dict.items():
        cv2.putText(frame, name + ': ' + str(dem), (10, count), cv2.FONT_HERSHEY_SIMPLEX, 1, (57, 53, 233), thickness=3, lineType=2)
        count += 40

def report_android_csv(csv_name, confidence, count_threshold, model_checkpoint = 'models',
                       classifier = 'models/your_model.pkl', video_file = "http://192.168.1.138:8080/video", output_file = None):
    global names_dict
    names_dict = {}

    # Set fps
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    if video_file is not None:
        video_capture = cv2.VideoCapture(video_file)
    else:
        # Use internal camera
        video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    width = frame.shape[1]
    height = frame.shape[0]
    if output_file is not None:
        video_format = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, video_format, 20, (width, height))
    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays_android_report(frame, faces, frame_rate, colors, confidence=confidence)

        frame_count += 1
        frame75 = rescale_frame(frame, percent=75)
        cv2.imshow('Video', frame75)
        if output_file is not None:
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    if output_file is not None:
        out.release()
    video_capture.release()
    cv2.destroyAllWindows()

    # Add to csv
    add_csv_with_count(names_dict, csv_name, count_threshold)

def report_camip_csv(csv_name, confidence, count_threshold, model_checkpoint = 'models',
                       classifier = 'models/your_model.pkl', camip_http = "rtsp://admin:khoinguyen997@192.168.1.148:554/onvif1"):
    global names_dict
    names_dict = {}

    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    # Set VLC
    player = vlc.MediaPlayer(camip_http)
    player.video_set_scale(0.25)

    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))

    player.play()
    time.sleep(3)

    while True:
        # Capture frame-by-frame
        player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)
        frame = cv2.imread('.snapshot.tmp.png')

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays_android_report(frame, faces, frame_rate, colors, confidence=confidence)
        frame_count += 1
        frame75 = rescale_frame(frame, percent=75)
        cv2.imshow('Video', frame75)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    player.stop()

    # Add to csv
    add_csv_with_count(names_dict, csv_name, count_threshold)
