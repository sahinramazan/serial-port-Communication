
## RAMAZAN ŞAHİN

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QComboBox, \
    QPushButton, QLineEdit, QListWidget , QCheckBox

from PyQt5.QtCore import Qt,QTimer

import sys
import serial
import serial.tools.list_ports as listport
import struct


port=serial.Serial()


class Pencere(QWidget):
    
    def __init__(self):
        super().__init__()
        self.arayuz()
        self.show()

        

    def arayuz(self): # UI design
        self.setWindowTitle("GÖNDERİCİ")
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
        grid1.addWidget(self.pushbuttonBaglan, 1, 5, Qt.AlignLeft)
        self.pushbuttonBaglantiKes = QPushButton("Bağlantı Kes") 
        grid1.addWidget(self.pushbuttonBaglantiKes, 2, 5, Qt.AlignLeft)
        labelUpdateRate = QLabel("Update Rate(ms)")
        grid1.addWidget(labelUpdateRate, 1, 4, Qt.AlignLeft)
        self.comboboxUpdateRate = QComboBox()
        grid1.addWidget(self.comboboxUpdateRate,2,4,Qt.AlignRight)
        
        labelKapı1 = QLabel("Kapı1")
        grid1.addWidget(labelKapı1,3,1,Qt.AlignLeft)
        self.CheckboxDurumcheck1 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck1 , 4 , 1, Qt.AlignLeft)

        labelKapı2 = QLabel("Kapı2")
        grid1.addWidget(labelKapı2,3,2,Qt.AlignLeft)
        self.CheckboxDurumcheck2 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck2 , 4 , 2, Qt.AlignLeft)

        labelKapı3 = QLabel("Kapı3")
        grid1.addWidget(labelKapı3,3,3,Qt.AlignLeft)
        self.CheckboxDurumcheck3 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck3 , 4 , 3, Qt.AlignLeft)

        labelYangınA = QLabel("Yangın A.")
        grid1.addWidget(labelYangınA,3,4,Qt.AlignLeft)
        self.CheckboxDurumcheck4 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck4 , 4 , 4, Qt.AlignLeft)

        labelMotorU = QLabel("Motor U.")
        grid1.addWidget(labelMotorU,3,5,Qt.AlignLeft)
        self.CheckboxDurumcheck5 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck5 , 4 , 5, Qt.AlignLeft)

        labelSintineU = QLabel("Sintine U.")
        grid1.addWidget(labelSintineU,3,6,Qt.AlignLeft)
        self.CheckboxDurumcheck6 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck6 , 4 , 6, Qt.AlignLeft)

        labelTemizSu = QLabel("Temiz su U.")
        grid1.addWidget(labelTemizSu,3,7,Qt.AlignLeft)
        self.CheckboxDurumcheck7 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck7 , 4 , 7, Qt.AlignLeft)

        labelYakıtU = QLabel("Yakıt U.")
        grid1.addWidget(labelYakıtU,3,8,Qt.AlignLeft)
        self.CheckboxDurumcheck8 = QCheckBox()
        grid1.addWidget(self.CheckboxDurumcheck8 , 4 , 8, Qt.AlignLeft)


        hbox1.addLayout(grid1)
        vboxAna.addLayout(hbox1)
        vboxAna.addSpacing(80)
        hbox2=QHBoxLayout()
        grid2= QGridLayout()

        labelHiz = QLabel("Hız Deniz Mili")
        grid2.addWidget(labelHiz, 1, 1, Qt.AlignLeft)
        self.lineeditHiz = QLineEdit()
        self.lineeditHiz.setText("20")
        self.lineeditHiz.setFixedWidth(40)
        grid2.addWidget(self.lineeditHiz, 2, 1, Qt.AlignLeft)

        labelYon = QLabel("Yön ")
        grid2.addWidget(labelYon, 1, 2, Qt.AlignLeft)
        self.lineeditYon = QLineEdit()
        self.lineeditYon.setText("60")
        self.lineeditYon.setFixedWidth(40)
        grid2.addWidget(self.lineeditYon, 2, 2, Qt.AlignLeft)
        
        hbox2.addLayout(grid2)
        vboxAna.addLayout(hbox2)
        
        self.setLayout(vboxAna)
        self.ilkdurum()
        self.olaylar()
 

    def ilkdurum(self): 
        portlar=listport.comports()
        
        for cp in portlar:
            self.comboboxComPort.addItem(str(cp.device))
        ayarliste= ["8,O,1","8,E,1","8,N,2"]
        liste=["9600","14400", "19200", "38400", "57600", "115200"]
        updataRateliste = ["100","200","300"]
        self.comboboxUpdateRate.addItems(updataRateliste)
        self.comboboxBaudrate.addItems(liste)
        self.comboboxAyarlar.addItems(ayarliste)
        self.pushbuttonBaglantiKes.setEnabled(False)
        

    def olaylar(self): #olaylar
        self.pushbuttonBaglan.clicked.connect(self.baglan) #serial port açılış
        self.pushbuttonBaglantiKes.clicked.connect(self.baglantikes) #serial port kapanış
        
        

    def baglan(self):

        port.baudrate = int(self.comboboxBaudrate.currentText())
        ayar=self.comboboxAyarlar.currentText() # combobox ayarlarından ayarları alın

        port.bytesize = serial.EIGHTBITS

        if ayar[2] == "E":
            port.parity = serial.PARITY_EVEN
        if ayar[2] == "O":
            port.parity = serial.PARITY_ODD
        if ayar[2] == "N":                                      # kaç bit ile göndereceğimizi belirtiyor.
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
                self.timer.timeout.connect(self.gonder)
                self.timer.start(int(self.comboboxUpdateRate.currentText()))




    def baglantikes(self): #Bağlantı kapatma

        if port.is_open:
            
            port.close()
            if not port.is_open:
                self.pushbuttonBaglan.setEnabled(True)
                self.pushbuttonBaglantiKes.setEnabled(False)
                self.timer.stop()
  

    def gonder(self): #serial portttan veri gönder
        sayi=0
        if(self.CheckboxDurumcheck1.isChecked()):
            sayi=sayi+ 128
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck2.isChecked()):
            sayi=sayi+ 64
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck3.isChecked()):
            sayi=sayi+ 32
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck4.isChecked()):
            sayi=sayi+ 16
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck5.isChecked()):
            sayi=sayi+ 8
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck6.isChecked()):
            sayi=sayi+ 4
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck7.isChecked()):
            sayi=sayi+ 2
        else :
            sayi=sayi+0
        if(self.CheckboxDurumcheck8.isChecked()):
            sayi=sayi+ 1
        else :
            sayi=sayi+0

        if(self.lineeditHiz.text()==""):
            hiz = 0
        else:
            hiz=float(self.lineeditHiz.text())
        hizArray=struct.pack('f',hiz)


        if(self.lineeditYon.text()==""):
            yon = 0
        else:
            yon=float(self.lineeditYon.text())
        yonArray=struct.pack('f',yon)

        totalpack=bytes.fromhex('55')+hizArray+yonArray+sayi.to_bytes(1,byteorder='big')
        crc=self.compute_crc8(totalpack)
        print('crc: ',crc)
        totalpack=totalpack+crc.to_bytes(1,byteorder='big')+bytes.fromhex('AA')

        print('total pack :',totalpack)

        header=totalpack[:1]
        hizData=totalpack[1:5]
        yonData=totalpack[5:9]
        durumData=totalpack[9:10]
        print('Header :',int.from_bytes(header,byteorder=sys.byteorder))
        print("Hız Data:",struct.unpack('f',hizData)[0])
        print("Yon Data:",struct.unpack('f',yonData)[0])
        print("Durum Data:",bin(int.from_bytes(durumData, byteorder=sys.byteorder)))
        port.write(totalpack)
        
    def compute_crc8(self,datagram, initial_value=0):
        crc = initial_value
        # Verilerde bayt yineleme
        for byte in datagram:
            # Iterate bits in byte
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
