from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import sqlite3
import datetime
from datetime import date
import cv2, os, numpy

ui,_=loadUiType('design/Face-recognition.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.LOGIN.clicked.connect(self.login)
        self.LOGOUT.clicked.connect(self.logout)
        self.CLOSE.clicked.connect(self.close_window)
        self.TRAINLINK1.clicked.connect(self.show_training_form)
        self.ATTLINK1.clicked.connect(self.show_attendance_entry_form)
        self.REPORTSLINK1.clicked.connect(self.show_report_form)
        self.ELIGIBILITYLINK1.clicked.connect(self.show_status_form)
        self.PREVIOUSRECO.clicked.connect(self.show_mainform)
        self.PREVIOUSPAGE.clicked.connect(self.show_mainform)
        self.PREVIOUSREPORT.clicked.connect(self.show_mainform)
        self.PREVIOUSREPORT_2.clicked.connect(self.show_mainform)
        self.TRAINBUTTON.clicked.connect(self.start_training)
        self.RECORD.clicked.connect(self.record_attendance)
        self.dateEdit.setDate(date.today())
        self.dateEdit_2.setDate(date.today())
        self.dateEdit_3.setDate(date.today())
        self.dateEdit.dateChanged.connect(self.show_selected_date_report)
        self.dateEdit_2.dateChanged.connect(self.show_eligibility_report)
        self.spinBox.valueChanged.connect(self.show_eligibility_report)
        self.tabWidget.setStyleSheet("QTabWidget::pane{border:0;}")
        try:
            con = sqlite3.connect("face-reco.db")
            con.execute("CREATE TABLE IF NOT EXISTS attendance(attendanceid INTEGER, name TEXT, matric_number INTEGER, sex TEXT, category TEXT, attendancedate TEXT, time TEXT)")
            con.commit()
            print("Table created successfully")
        except:
            print("Error in database")


    ### LOGIN PROCESS ###
    def login(self):
        pw = self.PASSWORD.text()
        if(pw=="123"):
            self.PASSWORD.setText("")
            self.LOGIN.setText("")
            self.tabWidget.setCurrentIndex(1)
        else:
            self.invalidmessage.setText("Invalid Password...")
            self.PASSWORD.setText("")


    ### LOG OUT PROCESS ###
    def logout(self):
        self.tabWidget.setCurrentIndex(0)


    ### CLOSE WINDOW PROCESS ###
    def close_window(self):
        self.close()


    ### SHOW MAIN FORM ###
    def show_mainform(self):
        self.tabWidget.setCurrentIndex(1)        


    ### SHOW TRAINING FORM ###
    def show_training_form(self):
        self.tabWidget.setCurrentIndex(2)


    ### SHOW ATTENDANCE ENTRY FORM ###
    def show_attendance_entry_form(self):
        self.tabWidget.setCurrentIndex(3)


    ### SHOW REPORT FORM ###
    def show_report_form(self):
        self.tabWidget.setCurrentIndex(4)
        self.REPORTTABLE.setRowCount(0)
        self.REPORTTABLE.clear()
        con = sqlite3.connect("face-reco.db")
        cursor = con.execute("SELECT * FROM attendance")
        result = cursor.fetchall()
        r=0
        c=0
        for row_number,row_data in enumerate(result):
            r+=1
            c=0
            for column_number,data in enumerate(row_data):
                c+=1
        self.REPORTTABLE.setColumnCount(c)

        for row_number,row_data in enumerate(result):
            self.REPORTTABLE.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.REPORTTABLE.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        self.REPORTTABLE.setHorizontalHeaderLabels(['Id','Name', 'Matric number', 'Sex', 'Category', 'Date', 'Time'])        
        self.REPORTTABLE.setColumnWidth(0,10)
        self.REPORTTABLE.setColumnWidth(1,100)
        self.REPORTTABLE.setColumnWidth(2,50)
        self.REPORTTABLE.setColumnWidth(3,10)
        self.REPORTTABLE.setColumnWidth(4,50)
        self.REPORTTABLE.setColumnWidth(5,70)
        self.REPORTTABLE.setColumnWidth(6,10)
        self.REPORTTABLE.verticalHeader().setVisible(False)


    ### SHOW SELECTED DATE REPORTS ###
    def show_selected_date_report(self):
        self.REPORTTABLE.setRowCount(0)
        self.REPORTTABLE.clear()
        con = sqlite3.connect("face-reco.db")
        cursor = con.execute("SELECT * FROM attendance WHERE attendancedate = '"+ str((self.dateEdit.date()).toPyDate()) +"'")
        result = cursor.fetchall()
        r=0
        c=0
        for row_number,row_data in enumerate(result):
            r+=1
            c=0
            for column_number,data in enumerate(row_data):
                c+=1
        self.REPORTTABLE.setColumnCount(c)

        for row_number,row_data in enumerate(result):
            self.REPORTTABLE.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.REPORTTABLE.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        self.REPORTTABLE.setHorizontalHeaderLabels(['Id','Name', 'Matric number', 'Sex', 'Category', 'Date', 'Time'])        
        self.REPORTTABLE.setColumnWidth(0,10)
        self.REPORTTABLE.setColumnWidth(1,100)
        self.REPORTTABLE.setColumnWidth(2,50)
        self.REPORTTABLE.setColumnWidth(3,10)
        self.REPORTTABLE.setColumnWidth(4,50)
        self.REPORTTABLE.setColumnWidth(5,70)
        self.REPORTTABLE.setColumnWidth(6,10)
        self.REPORTTABLE.verticalHeader().setVisible(False)


    def show_status_form(self):
        self.tabWidget.setCurrentIndex(5)
        self.STATUSTABLE.setRowCount(0)
        self.STATUSTABLE.clear()
        con = sqlite3.connect("face-reco.db")
        cursor = con.execute('SELECT * FROM attendance')
        result = cursor.fetchall()
        r=0
        c=0
        for row_number,row_data in enumerate(result):
            r+=1
            c=0
            for column_number,data in enumerate(row_data):
                c+=1
        self.STATUSTABLE.setColumnCount(c)

        for row_number,row_data in enumerate(result):
            self.STATUSTABLE.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.STATUSTABLE.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        self.STATUSTABLE.setHorizontalHeaderLabels(['Id','Name', 'Matric number', 'Sex', 'Category', 'Date', 'Time'])        
        self.STATUSTABLE.setColumnWidth(0,10)
        self.STATUSTABLE.setColumnWidth(1,100)
        self.STATUSTABLE.setColumnWidth(2,50)
        self.STATUSTABLE.setColumnWidth(3,10)
        self.STATUSTABLE.setColumnWidth(4,50)
        self.STATUSTABLE.setColumnWidth(5,70)
        self.STATUSTABLE.setColumnWidth(6,10)
        self.STATUSTABLE.verticalHeader().setVisible(False)


    def show_eligibility_report(self):
        self.STATUSTABLE.setRowCount(0)
        self.STATUSTABLE.clear()
        con = sqlite3.connect("face-reco.db")
        command_drop = con.execute('DROP TABLE IF EXISTS eligibility;')
        command_create = f"""
SELECT
	name,
    matric_number,
    sex,
    category,
    COUNT(name) AS classes_attended,
	IIF(COUNT(name)/ {float(self.spinBox.value())} > 0.6, 'eligible', 'not eligible') AS eligible
FROM
	attendance 
WHERE
	attendancedate >= '{str((self.dateEdit_3.date()).toPyDate())}' AND attendancedate <= '{str((self.dateEdit_2.date()).toPyDate())}'
GROUP BY
	name;
   """
        
        cursor = con.execute(command_create)
        result = cursor.fetchall()
        r=0
        c=0
        for row_number,row_data in enumerate(result):
            r+=1
            c=0
            for column_number,data in enumerate(row_data):
                c+=1
        self.STATUSTABLE.setColumnCount(c)

        for row_number,row_data in enumerate(result):
            self.STATUSTABLE.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.STATUSTABLE.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        self.STATUSTABLE.setHorizontalHeaderLabels(['Name','Matric number', 'Sex', 'Category','Classes_attended','Eligibility'])        
        self.STATUSTABLE.setColumnWidth(0,100)
        self.STATUSTABLE.setColumnWidth(1,10)
        self.STATUSTABLE.setColumnWidth(2,10)
        self.STATUSTABLE.setColumnWidth(3,50)
        self.STATUSTABLE.setColumnWidth(4,5)
        self.STATUSTABLE.setColumnWidth(5,50)
        self.STATUSTABLE.verticalHeader().setVisible(False)


    ### TRAINING PROCESS ###
    def start_training(self):
        haar_file = 'haarcascade_files/haarcascade_frontalface_default.xml'
        datasets = 'database'
        sub_data = self.traineeName.text()
        path = os.path.join(datasets,sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
            print("The new directory is created")
            (width,height) = (130,100)
            face_cascade = cv2.CascadeClassifier(haar_file)
            webcam = cv2.VideoCapture(0)
            count = 1
            while count < int(self.traineeCAPTURES.text()) + 1:
                print(count)
                (_,im) = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray,1.3,4)
                for (x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
                    face = gray[y:y+h,x:x+w]
                    face_resize = cv2.resize(face,(width,height))
                    cv2.imwrite('%s/%s.png'%(path,count),face_resize)
                count += 1
                cv2.imshow('OpenCV',im)
                key = cv2.waitKey(10)
                if key == 27:
                    break
            webcam.release()
            cv2.destroyAllWindows()  
            path=""
            QMessageBox.information(self,"Attendance System","Training Completed Successfully")  
            self.traineeName.setText("")
            self.traineeCAPTURES.setText("100")


    ### RECORD ATTENDANCE ###
    def record_attendance(self):
        self.currentstatus.setText("Process started.. Waiting..")        
        haar_file = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_file)
        datasets = 'database'
        (images,labels,names,id) =([],[],{},0)
        for(subdirs,dirs,files) in os.walk(datasets):
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(datasets,subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + "/" + filename
                    label = id
                    images.append(cv2.imread(path,0))
                    labels.append(int(label))
                id += 1
        (images,labels) = [numpy.array(lis) for lis in [images,labels]]
        print(images,labels)
        (width, height) = (130,100)
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(images,labels)   
        webcam = cv2.VideoCapture(0)
        cnt=0
        while True:
            (_,im) = webcam.read()
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
                face = gray[y:y+h,x:x+w]
                face_resize = cv2.resize(face,(width,height))
                prediction = model.predict(face_resize)
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)
                if(prediction[1]<800):
                    cv2.putText(im,'%s-%.0f'%(names[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255))
                    print(names[prediction[0]])
                    self.currentstatus.setText("Detected face - " + names[prediction[0]])        


                    attendanceid =0
                    available = False
                    try:
                        connection = sqlite3.connect("face-reco.db")
                        cursor = connection.execute("SELECT MAX(attendanceid) from attendance")
                        result = cursor.fetchall()
                        if result:
                            for maxid in result:
                                attendanceid = int(maxid[0])+1
                    except:
                        attendanceid=1
                    print(attendanceid)    

                    try:
                        con = sqlite3.connect("face-reco.db")
                        cursor = con.execute("SELECT * FROM attendance WHERE name='"+ str(names[prediction[0]]) +"' and attendancedate = '"+ str(date.today()) +"'")
                        result = cursor.fetchall()
                        if result:
                            available=True
                        if(available==False):
                            con.execute("INSERT INTO attendance VALUES("+ str(attendanceid) +",'"+ str(names[prediction[0]]) +"',"+ str(self.traineeMat.text()) +",'"+ str(self.traineeSex.text()) +"','"+ str(self.traineeCat.text()) +"','"+ str(date.today()) +"', '"+ str(datetime.datetime.now().time().strftime('%H:%M')) +"')")
                            con.commit()   
                    except:
                        print("Error in database insert")
                    print("Attendance Registered successfully")
                    self.currentstatus.setText("Attendance registered for " + names[prediction[0]])            
                    cnt=0

                else:
                    cnt+=1
                    cv2.putText(im,'UnKnown',(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0))
                    if(cnt>100):
                        print("Unknown person")
                        self.currentstatus.setText("Unknown Person ")        
                        cv2.imwrite('unKnown.jpg',im)
                        cnt=0
            cv2.imshow("Face Recognition",im)
            key = cv2.waitKey(10)
            if key==27:
                break
        webcam.release()
        cv2.destroyAllWindows()        











def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()    
