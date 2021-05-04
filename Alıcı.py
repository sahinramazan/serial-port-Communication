
## RAMAZAN ŞAHİN

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QComboBox, \
    QPushButton, QLineEdit, QListWidget , QCheckBox

from PyQt5.QtCore import Qt,QTimer

import sys
import serial
import serial.tools.list_ports as listport
import struct
import sqlite3 as sl
import time
import datetime


port=serial.Serial()




class Pencere(QWidget):
    
    def __init__(self):
        super().__init__()
        self.arayuz()
        self.show()

    def arayuz(self): 
        self.setWindowTitle("ALICI") 
        vboxAna=QVBoxLayout()
        hbox1=QHBoxLayout()
        grid1=QGridLayout()
        labelComport=QLabel("COM Port")
        grid1.addWidget(labelComport,1,1,Qt.AlignLeft)
        self.comboboxComPort = QComboBox()
        grid1.addWidget(self.comboboxComPort,2,1,Qt.AlignLeft)
        labelBaudrate=QLabel("Baudrate")
        grid1.addWidget(labelBaudrate, 1, 2, Qt.AlignLeft)
        self.comboboxBaudrate = QComboBox()
        grid1.addWidget(self.comboboxBaudrate, 2, 2, Qt.AlignLeft)
        labelAyarlar = QLabel("Ayarlar")
        grid1.addWidget(labelAyarlar, 1, 3, Qt.AlignLeft)
        self.comboboxAyarlar = QComboBox()
        grid1.addWidget(self.comboboxAyarlar, 2, 3, Qt.AlignLeft)
        self.pushbuttonBaglan = QPushButton("Bağlan")
        grid1.addWidget(self.pushbuttonBaglan, 1, 4, Qt.AlignLeft)
        self.pushbuttonBaglantiKes = QPushButton("Bağlantı Kes") 
        grid1.addWidget(self.pushbuttonBaglantiKes, 2, 4, Qt.AlignLeft)
        
        

        
        self.labelKapi1 = QLabel("Kapı1")
        grid1.addWidget(self.labelKapi1,3,1,Qt.AlignLeft)
        self.labelKapi2 = QLabel("Kapı2")
        grid1.addWidget(self.labelKapi2,3,2,Qt.AlignLeft)
        self.labelKapi3 = QLabel("Kapı3")
        grid1.addWidget(self.labelKapi3,3,3,Qt.AlignLeft)
        self.labelYangınA = QLabel("Yangın A.")
        grid1.addWidget(self.labelYangınA,3,4,Qt.AlignLeft)
        self.labelMotorU = QLabel("Motor U.")
        grid1.addWidget(self.labelMotorU,3,5,Qt.AlignLeft)
        self.labelSintineU = QLabel("Sintine U.")
        grid1.addWidget(self.labelSintineU,3,6,Qt.AlignLeft)
        self.labelTemizSu = QLabel("Temiz su U.")
        grid1.addWidget(self.labelTemizSu,3,7,Qt.AlignLeft)
        self.labelYakitU = QLabel("Yakıt U.")
        grid1.addWidget(self.labelYakitU,3,8,Qt.AlignLeft)
   
        hbox1.addLayout(grid1)
        vboxAna.addLayout(hbox1)
        vboxAna.addSpacing(80)
        hbox2=QHBoxLayout()
        grid2= QGridLayout()

        labelHiz = QLabel("Hız Deniz Mili")
        grid2.addWidget(labelHiz, 1, 1, Qt.AlignLeft)
        self.labelHiz1 = QLabel("")
        grid2.addWidget(self.labelHiz1, 2, 1, Qt.AlignLeft)
   

        labelYon = QLabel("Yön ")
        grid2.addWidget(labelYon, 1, 2, Qt.AlignLeft)
        self.labelYon1 = QLabel("")
        grid2.addWidget(self.labelYon1, 2, 2, Qt.AlignLeft)
       

        hbox2.addLayout(grid2)
        vboxAna.addLayout(hbox2)
        vbox1 = QVBoxLayout()
    
        
        self.setLayout(vboxAna)
        self.ilkdurum()
        self.olaylar()
        
    def ilkdurum(self): #initialize
        portlar=listport.comports()
        # Tüm seri arayüzleri combobox'a yerleştirme
        for cp in portlar:
            self.comboboxComPort.addItem(str(cp.device))
        ayarliste= ["8,O,1","8,E,1","8,N,2"]
        liste=["9600","14400", "19200", "38400", "57600", "115200"]
        self.comboboxBaudrate.addItems(liste)
        self.comboboxAyarlar.addItems(ayarliste)
        self.pushbuttonBaglantiKes.setEnabled(False)
        
    def olaylar(self): 
        self.pushbuttonBaglan.clicked.connect(self.baglan) #serial port açma
        self.pushbuttonBaglantiKes.clicked.connect(self.baglantikes) #serial port kapama
        
    def baglan(self):

        port.baudrate = int(self.comboboxBaudrate.currentText())
        ayar=self.comboboxAyarlar.currentText() 

        port.bytesize = serial.EIGHTBITS

        if ayar[2] == "E":
            port.parity = serial.PARITY_EVEN
        if ayar[2] == "O":
            port.parity = serial.PARITY_ODD
        if ayar[2] == "N":
            port.parity = serial.PARITY_NONE
        if ayar[4] == "1":
            port.stopbits = serial.STOPBITS_ONE
        if ayar[4] == "2":
            port.stopbits = serial.STOPBITS_TWO
        port.port = self.comboboxComPort.currentText()
        if not port.is_open:
            port.open()
            if port.is_open:
                self.pushbuttonBaglan.setEnabled(False)
                self.pushbuttonBaglantiKes.setEnabled(True)
                self.timer=QTimer()
                self.timer.timeout.connect(self.verial)
                self.timer.start(100)

    def baglantikes(self): #close connection

        if port.is_open:
            port.close()
            if not port.is_open:
                self.pushbuttonBaglan.setEnabled(True)
                self.pushbuttonBaglantiKes.setEnabled(False)
                self.timer.stop()

    def verial(self): 
        veritabani = sl.connect("veritabanı.db")
        cursor = veritabani.cursor()

        tarih = datetime.datetime.now()

        veri=""
        if port.is_open:
            gelenVeri = port.read(port.in_waiting)
            
            if not gelenVeri==b'':
                print(gelenVeri)
                header=gelenVeri[:1]
                hizData=gelenVeri[1:5]
                yonData=gelenVeri[5:9]
                durumData=gelenVeri[9:10]
                gelendata = gelenVeri[0:10]


                crc = self.compute_crc8(gelendata)
                print("gelen crc = ",int.from_bytes(gelenVeri[10:11],byteorder=sys.byteorder))
                if(crc==int.from_bytes(gelenVeri[10:11],byteorder=sys.byteorder)):

                    print("Gelen Data Doğrudur")

                    print("crc = ",crc)
                    print(hizData)
                
                    print('Header :',int.from_bytes(header,byteorder=sys.byteorder))

                    self.labelHiz1.setText(str((struct.unpack('f',hizData)[0])))
                    self.labelYon1.setText(str(struct.unpack('f',yonData)[0]))
                    
                    xHizData = struct.unpack('f',hizData)[0]
                    yYondata = struct.unpack('f',yonData)[0]
                    print("Hız Data:",xHizData) 
                    print("Yon Data:",yYondata)
                    databit = bin(int.from_bytes(durumData, byteorder=sys.byteorder))[2:].zfill(8)   #8 digite zorluor 0 ekliyor
                    print("Durum Data:",databit)
                    vdurum = int(databit)
                    cursor.execute("INSERT INTO veri VALUES(?,?,?,?)",(tarih,xHizData,yYondata,vdurum))
                    veritabani.commit()

                    uzunlukDataBit=len(databit)
                    print(uzunlukDataBit)

                    if(databit[0]=="1"):
                        self.labelKapi1.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelKapi1.setStyleSheet("background-color: red")
                    if(databit[1]=="1"):
                        self.labelKapi2.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelKapi2.setStyleSheet("background-color: red")
                    if(databit[2]=="1"):
                        self.labelKapi3.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelKapi3.setStyleSheet("background-color: red")
                    if(databit[3]=="1"):
                        self.labelYangınA.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelYangınA.setStyleSheet("background-color: red")
                    if(databit[4]=="1"):
                        self.labelMotorU.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelMotorU.setStyleSheet("background-color: red")
                    if(databit[5]=="1"):
                        self.labelSintineU.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelSintineU.setStyleSheet("background-color: red")
                    if(databit[6]=="1"):
                        self.labelTemizSu.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelTemizSu.setStyleSheet("background-color: red")
                    if(databit[7]=="1"):
                        self.labelYakitU.setStyleSheet("background-color: lightgreen")
                    else:
                        self.labelYakitU.setStyleSheet("background-color: red")
  
    def compute_crc8(self,datagram, initial_value=0):   #crc8 hesaplama
        crc = initial_value
        # Verilerde bayt yineleme
        for byte in datagram:
            # Bitleri bayt olarak Yinele
            for _ in range(0, 8):
                if (crc >> 7) ^ (byte & 0x01):
                    crc = ((crc << 1) ^ 0x07) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
                byte = byte >> 1
        return crc


#main

if __name__=="__main__":
    app=QApplication(sys.argv)
    pen=Pencere()
    sys.exit(app.exec())
