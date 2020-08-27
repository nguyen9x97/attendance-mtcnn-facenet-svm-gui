from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as font
from datetime import date
from utils_gui import *
import pandas as pd
import os

root = Tk()
root.title("Attendance System")
root.geometry("1100x600")
myFont = font.Font(family="Helvetica", size=20)
myFont_1 = font.Font(size=15)
Label(root, text=" Realtime Face Recognition - Attendance System", font=myFont, fg="blue", bg="orange", padx=20, pady=25).grid(row=0, column=0, columnspan=10)

def exit_program():
    response = messagebox.askyesno("Exiting window", "Do you want to Exit?")
    #Label(frame_exit, text=response).pack()
    if response:
        root.quit()

def button_clear(entry):
    entry.delete(0, END)

def display_webcam(name, id):
    #print(len(name), len(id))
    if len(name) < 1 or len(id) < 1:
        messagebox.showwarning("Error", "Please fill in all forms!")
        return
    try:
        int(id)
    except:
        messagebox.showerror("Error ID", "Your ID does not contain letters!")
        return
    name_id = name + "_" + str(id)
    label_apply.config(text=name_id)
    btn_start.config(state=ACTIVE)
    #dis = Label(webcam_window, text=name_id, font=myFont_1, pady=10)
    #dis.grid(row=3, column=1)

def start_collect(name, id, camera):
    btn_start.config(state=DISABLED)
    add_student_webcam_android(name, id, camera)

# Collect webcam
def open_webcam():
    # Collection - webcam
    global webcam_window
    webcam_window = Toplevel()
    webcam_window.geometry("850x300")
    webcam_window.title("Collect dataset - Webcam")
    Label(webcam_window, text="Student name:", font=myFont_1).grid(row=0, column=0)
    Label(webcam_window, text="Student ID:", font=myFont_1).grid(row=1, column=0)
    name_entry = Entry(webcam_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    name_entry.grid(row=0, column=1)
    id_entry = Entry(webcam_window, width=50,font=myFont_1, bg='blue', fg='white', borderwidth=5)
    id_entry.grid(row=1, column=1)
    global label_apply
    label_apply = Label(webcam_window, font=myFont_1)
    label_apply.grid(row=3, column=1)
    btn_apply = Button(webcam_window, text="Apply", font=myFont_1, command=lambda: display_webcam(name_entry.get(), id_entry.get()))
    btn_apply.grid(row=2, column=1)
    Label(webcam_window, text="Check: Name_ID", font=myFont_1, pady=10).grid(row=3, column=0)
    btn_clear_name = Button(webcam_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(name_entry))
    btn_clear_name.grid(row=0, column=2)
    btn_clear_id = Button(webcam_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(id_entry))
    btn_clear_id.grid(row=1, column=2)
    global btn_start
    btn_start = Button(webcam_window, text="Start collect", font=myFont_1, pady=10, state=DISABLED, command=lambda: start_collect(name_entry.get(), id_entry.get(), "webcam"))
    btn_start.grid(row=4, column=1)
    btn_close = Button(webcam_window, text="Close window", font=myFont_1, pady=20, command=webcam_window.destroy).grid(row=5, column=2, columnspan=2)

# Collect camip
def open_camip():
    global camip_window
    camip_window = Toplevel()
    camip_window.geometry("850x300")
    camip_window.title("Collect dataset - Cam IP")
    Label(camip_window, text="Student name:", font=myFont_1).grid(row=0, column=0)
    Label(camip_window, text="Student ID:", font=myFont_1).grid(row=1, column=0)
    name_entry = Entry(camip_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    name_entry.grid(row=0, column=1)
    id_entry = Entry(camip_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    id_entry.grid(row=1, column=1)
    global label_apply
    label_apply = Label(camip_window, font=myFont_1)
    label_apply.grid(row=3, column=1)
    btn_apply = Button(camip_window, text="Apply", font=myFont_1,
                       command=lambda: display_webcam(name_entry.get(), id_entry.get()))
    btn_apply.grid(row=2, column=1)
    Label(camip_window, text="Check: Name_ID", font=myFont_1, pady=10).grid(row=3, column=0)
    btn_clear_name = Button(camip_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(name_entry))
    btn_clear_name.grid(row=0, column=2)
    btn_clear_id = Button(camip_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(id_entry))
    btn_clear_id.grid(row=1, column=2)
    global btn_start
    btn_start = Button(camip_window, text="Start collect", font=myFont_1, pady=10, state=DISABLED,
                       command=lambda: start_collect(name_entry.get(), id_entry.get(), "camip"))
    btn_start.grid(row=4, column=1)
    btn_close = Button(camip_window, text="Close window", font=myFont_1, pady=20,
                       command=camip_window.destroy).grid(
        row=5, column=2, columnspan=2)

# Collect android
def open_android():
    global android_window
    android_window = Toplevel()
    android_window.geometry("850x300")
    android_window.title("Collect dataset - Android")
    Label(android_window, text="Student name:", font=myFont_1).grid(row=0, column=0)
    Label(android_window, text="Student ID:", font=myFont_1).grid(row=1, column=0)
    name_entry = Entry(android_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    name_entry.grid(row=0, column=1)
    id_entry = Entry(android_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    id_entry.grid(row=1, column=1)
    global label_apply
    label_apply = Label(android_window, font=myFont_1)
    label_apply.grid(row=3, column=1)
    btn_apply = Button(android_window, text="Apply", font=myFont_1,
                       command=lambda: display_webcam(name_entry.get(), id_entry.get()))
    btn_apply.grid(row=2, column=1)
    Label(android_window, text="Check: Name_ID", font=myFont_1, pady=10).grid(row=3, column=0)
    btn_clear_name = Button(android_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(name_entry))
    btn_clear_name.grid(row=0, column=2)
    btn_clear_id = Button(android_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(id_entry))
    btn_clear_id.grid(row=1, column=2)
    global btn_start
    btn_start = Button(android_window, text="Start collect", font=myFont_1, pady=10, state=DISABLED,
                       command=lambda: start_collect(name_entry.get(), id_entry.get(), "android"))
    btn_start.grid(row=4, column=1)
    btn_close = Button(android_window, text="Close window", font=myFont_1, pady=20, command=android_window.destroy).grid(
        row=5, column=2, columnspan=2)

# Collection Frame
frame_collection = LabelFrame(root, text="Collect dataset", padx=5, pady=5)
frame_collection.grid(row=1, column=0)
btn_collect_webcam = Button(frame_collection, text="Webcam",font=myFont_1, padx=26, pady=10, command=open_webcam)
btn_collect_camip = Button(frame_collection, text="Camera IP",font=myFont_1, pady=10, command=open_camip)
btn_collect_webcam.grid(row=0, column=0)
btn_collect_camip.grid(row=1, column=0)
btn_collect_android = Button(frame_collection, text="Android", font=myFont_1, pady=20, command=open_android).grid(row=0, rowspan=2, column=1)

def align_dataset():
    response = messagebox.askyesno("Warning", "Do you want to align your dataset?")
    if response:
        align_faces()

def training_dataset():
    response = messagebox.askyesno("Warning", "Are you sure?")
    if response:
        training_svm()

def start_remove(name, id):
    btn_start.config(state=DISABLED)
    remove_student(name, id)

def open_remove_student():
    global remove_window
    remove_window = Toplevel()
    remove_window.geometry("850x300")
    remove_window.title("Remove student")
    Label(remove_window, text="Student name:", font=myFont_1).grid(row=0, column=0)
    Label(remove_window, text="Student ID:", font=myFont_1).grid(row=1, column=0)
    name_entry = Entry(remove_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    name_entry.grid(row=0, column=1)
    id_entry = Entry(remove_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    id_entry.grid(row=1, column=1)
    global label_apply
    label_apply = Label(remove_window, font=myFont_1)
    label_apply.grid(row=3, column=1)
    btn_apply = Button(remove_window, text="Apply", font=myFont_1,
                       command=lambda: display_webcam(name_entry.get(), id_entry.get()))
    btn_apply.grid(row=2, column=1)
    Label(remove_window, text="Check: Name_ID", font=myFont_1, pady=10).grid(row=3, column=0)
    btn_clear_name = Button(remove_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(name_entry))
    btn_clear_name.grid(row=0, column=2)
    btn_clear_id = Button(remove_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(id_entry))
    btn_clear_id.grid(row=1, column=2)
    global btn_start
    btn_start = Button(remove_window, text="Start remove", font=myFont_1, pady=10, state=DISABLED, command=lambda: start_remove(name_entry.get(), id_entry.get()))
    btn_start.grid(row=4, column=1)
    btn_close = Button(remove_window, text="Close window", font=myFont_1, pady=20,
                       command=remove_window.destroy).grid(
        row=5, column=2, columnspan=2)
# Training Frame
frame_training = LabelFrame(root, text="Training", padx=5, pady=5)
frame_training.grid(row=1, column=1)
btn_align = Button(frame_training, text="Align dataset", font=myFont_1, command=align_dataset)
btn_align.grid(row=0, column=0)
btn_remove = Button(frame_training, text="Remove student", font=myFont_1, command=open_remove_student)
btn_remove.grid(row=0, column=1)
btn_training = Button(frame_training, text="Training/Updating", font=myFont_1, pady=15, command=training_dataset)
btn_training.grid(row=1, column=0, columnspan=2)

#Testing Frame
frame_testing = LabelFrame(root, text="Testing", padx=5, pady=5)
frame_testing.grid(row=1, column=2)
btn_detection = Button(frame_testing, text="Face Detection", font=myFont_1, pady=8, command=face_detection_test)
btn_detection.grid(row=0, column=0)
btn_recognition = Button(frame_testing, text="Face Recognition", font=myFont_1, pady=8, command=face_recognition_test)
btn_recognition.grid(row=0, column=1)
btn_recognition_camip = Button(frame_testing, text="Face Recognition with cam IP", font=myFont_1, pady=8, command=face_recognition_camip)
btn_recognition_camip.grid(row=1, columnspan=2)

def display_report(object_1, year_1, month_1, day_1, confidence):
    if len(object_1) < 1 or len(year_1) < 1 or len(month_1) < 1 or len(day_1) < 1 or len(confidence) < 1:
        messagebox.showwarning("Error", "Please fill in all forms!")
        return
    try:
        int(day_1) and int(month_1) and int(year_1)
        float(confidence)
        if float(confidence) <= 0 or float(confidence) >= 1:
            messagebox.showerror("Error setting confidence", "Confidence must between interval (0, 1)")
            return
    except:
        messagebox.showerror("Error ID", "Your date and confidence does not contain letters!")
        return

    object_date = object_1 + "_" + str(year_1) + "-" + str(month_1).zfill(2) + "-" + str(day_1).zfill(2)
    label_apply.config(text=object_date)
    label_confidence.config(text="confidence = " + str(confidence))
    btn_start.config(state=ACTIVE)

def start_report_webcam(object_1, year_1, month_1, day_1, confidence, camera, count=0):
    btn_start.config(state=DISABLED)
    object_date = object_1 + "_" + str(year_1) + "-" + str(month_1).zfill(2) + "-" + str(day_1).zfill(2) + ".csv"
    if camera == "webcam":
        report_webcam_csv(object_date, float(confidence))
    elif camera == "android":
        report_android_csv(object_date, float(confidence), int(count))
    elif camera == "camip":
        report_camip_csv(object_date, float(confidence), int(count))

def open_report_webcam():
    global report_webcam_window
    report_webcam_window = Toplevel()
    report_webcam_window.geometry('750x400')
    report_webcam_window.title("Single reporting")
    Label(report_webcam_window, text="Subject name:", font=myFont_1).grid(row=0, column=0)
    Label(report_webcam_window, text="Date (YYYY/MM/DD):", font=myFont_1).grid(row=1, column=0)
    object_entry = Entry(report_webcam_window, width=27, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    object_entry.grid(row=0, column=1, columnspan=3)
    year_entry = Entry(report_webcam_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    year_entry.grid(row=1, column=1)
    month_entry = Entry(report_webcam_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    month_entry.grid(row=1, column=2)
    day_entry = Entry(report_webcam_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    day_entry.grid(row=1, column=3)
    btn_clear_year = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(year_entry))
    btn_clear_year.grid(row=2, column=1)
    btn_clear_month = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(month_entry))
    btn_clear_month.grid(row=2, column=2)
    btn_clear_day = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(day_entry))
    btn_clear_day.grid(row=2, column=3)

    today = date.today()
    year_entry.insert(0, str(today.year))
    month_entry.insert(0, str(today.month))
    day_entry.insert(0, str(today.day))

    global label_apply
    label_apply = Label(report_webcam_window, font=myFont_1)
    label_apply.grid(row=4, column=1, columnspan=4)
    global label_confidence
    label_confidence = Label(report_webcam_window, font=myFont_1)
    label_confidence.grid(row=6, column=1, columnspan=3)
    btn_apply = Button(report_webcam_window, text="Apply", font=myFont_1,pady=15, padx=25,
                       command=lambda: display_report(object_entry.get(), year_entry.get(), month_entry.get(), day_entry.get(), confidence_entry.get()))
    btn_apply.grid(row=3, column=2, pady=5)
    Label(report_webcam_window, text="Subject_Date:", font=myFont_1, pady=10).grid(row=4, column=0)
    btn_clear_object = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(object_entry))
    btn_clear_object.grid(row=0, column=4)
    #btn_clear_date = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(date_entry))
    #btn_clear_date.grid(row=1, column=2)
    Label(report_webcam_window, text="Confidence", font=myFont_1).grid(row=5, column=0)
    confidence_entry = Entry(report_webcam_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    confidence_entry.grid(row=6, column=0)
    confidence_entry.insert(0, "0.4")
    btn_clear_confidence = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(confidence_entry))
    btn_clear_confidence.grid(row=7, column=0)
    global btn_start
    btn_start = Button(report_webcam_window, text="Start report", font=myFont_1, pady=10, state=DISABLED,
                       command=lambda: start_report_webcam(object_entry.get(), year_entry.get(), month_entry.get(), day_entry.get(), confidence_entry.get(), "webcam"))
    btn_start.grid(row=5, column=2)
    btn_close = Button(report_webcam_window, text="Close window", font=myFont_1, pady=20,
                       command=report_webcam_window.destroy).grid(
        row=7, column=5, columnspan=2)

def display_report_camip_android(object_1, year_1, month_1, day_1, confidence, count):
    if len(object_1) < 1 or len(year_1) < 1 or len(month_1) < 1 or len(day_1) < 1 or len(confidence) < 1 or len(count) < 1:
        messagebox.showwarning("Error", "Please fill in all forms!")
        return
    try:
        int(day_1) and int(month_1) and int(year_1) and int(count)
        float(confidence)
        if float(confidence) <= 0 or float(confidence) >= 1:
            messagebox.showerror("Error setting confidence", "Confidence must between interval (0, 1)")
            return
        if int(count) < 0:
            messagebox.showerror("Error setting count", "count must be positive")
            return
    except:
        messagebox.showerror("Error ID", "Your date, confidence and count does not contain letters!")
        return

    object_date = object_1 + "_" + str(year_1) + "-" + str(month_1).zfill(2) + "-" + str(day_1).zfill(2)
    label_apply.config(text=object_date)
    label_confidence.config(text="confidence = " + str(confidence))
    label_count.config(text="count = " + str(count))
    btn_start.config(state=ACTIVE)

def open_report_android():
    global report_android_window
    report_android_window = Toplevel()
    report_android_window.geometry('750x400')
    report_android_window.title("Multiple reporting - Android")
    Label(report_android_window, text="Subject name:", font=myFont_1).grid(row=0, column=0)
    Label(report_android_window, text="Date (YYYY/MM/DD):", font=myFont_1).grid(row=1, column=0)
    object_entry = Entry(report_android_window, width=27, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    object_entry.grid(row=0, column=1, columnspan=3)
    year_entry = Entry(report_android_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    year_entry.grid(row=1, column=1)
    month_entry = Entry(report_android_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    month_entry.grid(row=1, column=2)
    day_entry = Entry(report_android_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    day_entry.grid(row=1, column=3)
    btn_clear_year = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(year_entry))
    btn_clear_year.grid(row=2, column=1)
    btn_clear_month = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                             command=lambda: button_clear(month_entry))
    btn_clear_month.grid(row=2, column=2)
    btn_clear_day = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                           command=lambda: button_clear(day_entry))
    btn_clear_day.grid(row=2, column=3)

    today = date.today()
    year_entry.insert(0, str(today.year))
    month_entry.insert(0, str(today.month))
    day_entry.insert(0, str(today.day))

    global label_apply
    label_apply = Label(report_android_window, font=myFont_1)
    label_apply.grid(row=4, column=1, columnspan=4)
    global label_confidence
    label_confidence = Label(report_android_window, font=myFont_1)
    label_confidence.grid(row=6, column=1, columnspan=3)
    btn_apply = Button(report_android_window, text="Apply", font=myFont_1, pady=15, padx=25,
                       command=lambda: display_report_camip_android(object_entry.get(), year_entry.get(), month_entry.get(),
                                                      day_entry.get(), confidence_entry.get(), count_entry.get()))
    btn_apply.grid(row=3, column=2, pady=5)
    Label(report_android_window, text="Subject_Date:", font=myFont_1, pady=10).grid(row=4, column=0)
    btn_clear_object = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                              command=lambda: button_clear(object_entry))
    btn_clear_object.grid(row=0, column=4)
    # btn_clear_date = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(date_entry))
    # btn_clear_date.grid(row=1, column=2)
    Label(report_android_window, text="Confidence", font=myFont_1).grid(row=5, column=0)
    confidence_entry = Entry(report_android_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    confidence_entry.grid(row=6, column=0)
    confidence_entry.insert(0, "0.4")
    btn_clear_confidence = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                                  command=lambda: button_clear(confidence_entry))
    btn_clear_confidence.grid(row=7, column=0)
    global label_count
    label_count = Label(report_android_window, font=myFont_1)
    label_count.grid(row=6, column=5)
    Label(report_android_window, text="Count", font=myFont_1).grid(row=5, column=4)
    count_entry = Entry(report_android_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    count_entry.grid(row=6, column=4)
    count_entry.insert(0, "0")
    btn_clear_count = Button(report_android_window, text="Clear", font=myFont_1, padx=5,
                                  command=lambda: button_clear(count_entry))
    btn_clear_count.grid(row=7, column=4)
    global btn_start
    btn_start = Button(report_android_window, text="Start report", font=myFont_1, pady=10, state=DISABLED,
                       command=lambda: start_report_webcam(object_entry.get(), year_entry.get(), month_entry.get(),
                                                           day_entry.get(), confidence_entry.get(), "android", count=count_entry.get()))
    btn_start.grid(row=5, column=2)
    btn_close = Button(report_android_window, text="Close window", font=myFont_1, pady=20,
                       command=report_android_window.destroy).grid(
        row=8, column=5, columnspan=2)

def open_report_camip():
    global report_camip_window
    report_camip_window = Toplevel()
    report_camip_window.geometry('750x400')
    report_camip_window.title("Multiple reporting - Cam IP")
    Label(report_camip_window, text="Subject name:", font=myFont_1).grid(row=0, column=0)
    Label(report_camip_window, text="Date (YYYY/MM/DD):", font=myFont_1).grid(row=1, column=0)
    object_entry = Entry(report_camip_window, width=27, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    object_entry.grid(row=0, column=1, columnspan=3)
    year_entry = Entry(report_camip_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    year_entry.grid(row=1, column=1)
    month_entry = Entry(report_camip_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    month_entry.grid(row=1, column=2)
    day_entry = Entry(report_camip_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    day_entry.grid(row=1, column=3)
    btn_clear_year = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(year_entry))
    btn_clear_year.grid(row=2, column=1)
    btn_clear_month = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                             command=lambda: button_clear(month_entry))
    btn_clear_month.grid(row=2, column=2)
    btn_clear_day = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                           command=lambda: button_clear(day_entry))
    btn_clear_day.grid(row=2, column=3)

    today = date.today()
    year_entry.insert(0, str(today.year))
    month_entry.insert(0, str(today.month))
    day_entry.insert(0, str(today.day))

    global label_apply
    label_apply = Label(report_camip_window, font=myFont_1)
    label_apply.grid(row=4, column=1, columnspan=4)
    global label_confidence
    label_confidence = Label(report_camip_window, font=myFont_1)
    label_confidence.grid(row=6, column=1, columnspan=3)
    btn_apply = Button(report_camip_window, text="Apply", font=myFont_1, pady=15, padx=25,
                       command=lambda: display_report_camip_android(object_entry.get(), year_entry.get(),
                                                                    month_entry.get(),
                                                                    day_entry.get(), confidence_entry.get(),
                                                                    count_entry.get()))
    btn_apply.grid(row=3, column=2, pady=5)
    Label(report_camip_window, text="Subject_Date:", font=myFont_1, pady=10).grid(row=4, column=0)
    btn_clear_object = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                              command=lambda: button_clear(object_entry))
    btn_clear_object.grid(row=0, column=4)
    # btn_clear_date = Button(report_webcam_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(date_entry))
    # btn_clear_date.grid(row=1, column=2)
    Label(report_camip_window, text="Confidence", font=myFont_1).grid(row=5, column=0)
    confidence_entry = Entry(report_camip_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    confidence_entry.grid(row=6, column=0)
    confidence_entry.insert(0, "0.4")
    btn_clear_confidence = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                                  command=lambda: button_clear(confidence_entry))
    btn_clear_confidence.grid(row=7, column=0)
    global label_count
    label_count = Label(report_camip_window, font=myFont_1)
    label_count.grid(row=6, column=5)
    Label(report_camip_window, text="Count", font=myFont_1).grid(row=5, column=4)
    count_entry = Entry(report_camip_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    count_entry.grid(row=6, column=4)
    count_entry.insert(0, "0")
    btn_clear_count = Button(report_camip_window, text="Clear", font=myFont_1, padx=5,
                             command=lambda: button_clear(count_entry))
    btn_clear_count.grid(row=7, column=4)
    global btn_start
    btn_start = Button(report_camip_window, text="Start report", font=myFont_1, pady=10, state=DISABLED,
                       command=lambda: start_report_webcam(object_entry.get(), year_entry.get(), month_entry.get(),
                                                           day_entry.get(), confidence_entry.get(), "camip",
                                                           count=count_entry.get()))
    btn_start.grid(row=5, column=2)
    btn_close = Button(report_camip_window, text="Close window", font=myFont_1, pady=20,
                       command=report_camip_window.destroy).grid(
        row=8, column=5, columnspan=2)

def open_csv():
    path = os.getcwd()
    path_csv = os.path.join(path, 'my_csv_reported')
    if not os.path.exists(path_csv):
        os.mkdir(path_csv)
    root.filename = filedialog.askopenfilename(
        initialdir=path_csv, title="Select a file", filetypes=(("csv files", "*.csv"), ("all file", "*.*")))
    #print(root.filename)
    df_student = pd.read_csv(root.filename, index_col=0)
    print(df_student)
    messagebox.showinfo("Notification", "Your result is displayed in terminal")

#Reporting Frame
frame_report = LabelFrame(root, text="Reporting", padx=5, pady=5)
frame_report.grid(row=2, column=1)
btn_report_webcam = Button(frame_report, text="Single report - Webcam", font=myFont_1, padx=26, command=open_report_webcam)
btn_report_webcam.grid(row=0, column=0)
btn_report_camip = Button(frame_report, text="Multiple report - Cam IP", font=myFont_1, padx=16, command=open_report_camip)
btn_report_camip.grid(row=1, column=0)
btn_report_android = Button(frame_report, text="Multiple report - Android", font=myFont_1, command=open_report_android)
btn_report_android.grid(row=2, column=0)
btn_report_result = Button(frame_report, text="See result", font=myFont_1, pady=25, command=open_csv)
btn_report_result.grid(row=0, rowspan=3, column=1)

def display_hand_report(object_1, year_1, month_1, day_1, name, id):
    if len(object_1) < 1 or len(year_1) < 1 or len(month_1) < 1 or len(day_1) < 1 or len(name) < 1 or len(id) < 1:
        messagebox.showwarning("Error", "Please fill in all forms!")
        return
    try:
        int(day_1) and int(month_1) and int(year_1) and int(id)
        #float(confidence)
        #if float(confidence) <= 0 or float(confidence) >= 1:
            #messagebox.showerror("Error setting confidence", "Confidence must between interval (0, 1)")
            #return
    except:
        messagebox.showerror("Error ID", "Your date and your ID does not contain letters!")
        return

    object_date = object_1 + "_" + str(year_1) + "-" + str(month_1).zfill(2) + "-" + str(day_1).zfill(2)
    name_id = name + "_" + str(id)
    label_apply.config(text=object_date)
    label_name.config(text=name_id)
    btn_start.config(state=ACTIVE)

def start_hand_report(object_1, year_1, month_1, day_1, name, id):
    btn_start.config(state=DISABLED)
    object_date = object_1 + "_" + str(year_1) + "-" + str(month_1).zfill(2) + "-" + str(day_1).zfill(2) + ".csv"
    name_id = name + " " + str(id)
    add_to_csv(name_id, object_date)
    messagebox.showinfo("Notification", "Successfully adding:" + "\n" + name_id)


def open_hand_report():
    global hand_report_window
    hand_report_window = Toplevel()
    hand_report_window.geometry('770x420')
    hand_report_window.title("Hand reporting")
    Label(hand_report_window, text="Subject name:", font=myFont_1).grid(row=0, column=0)
    Label(hand_report_window, text="Date (YYYY/MM/DD):", font=myFont_1).grid(row=1, column=0)
    object_entry = Entry(hand_report_window, width=28, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    object_entry.grid(row=0, column=1, columnspan=3)
    year_entry = Entry(hand_report_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    year_entry.grid(row=1, column=1)
    month_entry = Entry(hand_report_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    month_entry.grid(row=1, column=2)
    day_entry = Entry(hand_report_window, width=5, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    day_entry.grid(row=1, column=3)
    btn_clear_year = Button(hand_report_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(year_entry))
    btn_clear_year.grid(row=2, column=1)
    btn_clear_month = Button(hand_report_window, text="Clear", font=myFont_1, padx=5,
                             command=lambda: button_clear(month_entry))
    btn_clear_month.grid(row=2, column=2)
    btn_clear_day = Button(hand_report_window, text="Clear", font=myFont_1, padx=5,
                           command=lambda: button_clear(day_entry))
    btn_clear_day.grid(row=2, column=3)

    today = date.today()
    year_entry.insert(0, str(today.year))
    month_entry.insert(0, str(today.month))
    day_entry.insert(0, str(today.day))

    global label_apply
    label_apply = Label(hand_report_window, font=myFont_1)
    label_apply.grid(row=4, column=1, columnspan=4)
    btn_apply = Button(hand_report_window, text="Apply", font=myFont_1, pady=15, padx=25,
                       command=lambda: display_hand_report(object_entry.get(), year_entry.get(), month_entry.get(),
                                                      day_entry.get(), name_entry.get(), id_entry.get()))
    btn_apply.grid(row=3, column=2, pady=5)
    Label(hand_report_window, text="Subject_Date:", font=myFont_1, pady=10).grid(row=4, column=0)
    btn_clear_object = Button(hand_report_window, text="Clear", font=myFont_1, padx=5,
                              command=lambda: button_clear(object_entry))
    btn_clear_object.grid(row=0, column=4)

    global label_name
    label_name = Label(hand_report_window, font=myFont_1)
    label_name.grid(row=7, column=2, columnspan=3)

    global btn_start
    btn_start = Button(hand_report_window, text="Start report", font=myFont_1,
                       pady=10, state=DISABLED,
                       command=lambda: start_hand_report(object_entry.get(),year_entry.get(), month_entry.get(), day_entry.get(), name_entry.get(),id_entry.get()))
    btn_start.grid(row=8, column=2)
    btn_close = Button(hand_report_window, text="Close window", font=myFont_1, pady=20,
                       command=hand_report_window.destroy).grid(
        row=9, column=5, columnspan=2)

    Label(hand_report_window, text="Student name:", font=myFont_1).grid(row=5, column=0)
    Label(hand_report_window, text="Student ID:", font=myFont_1).grid(row=6, column=0)
    name_entry = Entry(hand_report_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    name_entry.grid(row=5, column=1, columnspan=5)
    id_entry = Entry(hand_report_window, width=50, font=myFont_1, bg='blue', fg='white', borderwidth=5)
    id_entry.grid(row=6, column=1, columnspan=5)

    btn_clear_name = Button(hand_report_window, text="Clear", font=myFont_1, padx=5,
                            command=lambda: button_clear(name_entry))
    btn_clear_name.grid(row=5, column=7)
    btn_clear_id = Button(hand_report_window, text="Clear", font=myFont_1, padx=5, command=lambda: button_clear(id_entry))
    btn_clear_id.grid(row=6, column=7)

#Others fame
frame_others = LabelFrame(root, text="Others", padx=5, pady=5)
frame_others.grid(row=2, column=2)
btn_hand = Button(frame_others, text="Hand report", font=myFont_1, command= open_hand_report)
btn_hand.pack()
btn_exit = Button(frame_others, text="Exit", font=myFont_1, padx=30, pady=20, command=exit_program)
btn_exit.pack()


root.mainloop()