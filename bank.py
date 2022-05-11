from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem
from PyQt5.QtCore import QDate,QDateTime,Qt
from PyQt5 import QtGui
import sys

from DataAccess.data import DB


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank of System / Banka Müdürü Panel")
        self.create_menu()
        self.setMinimumSize(900,500)
        self.open=Window()
        self.setCentralWidget(self.open) 
        self.show()
        """icon = QtGui.QIcon()#icon ekleme
        icon.addPixmap(QtGui.QPixmap("icon_app.jfif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)"""
    
    def create_menu(self):
        menubar = self.menuBar()
        
        customer = menubar.addMenu("Müşteri İşlem")

        add_customer = QAction("Müşteri Ekleme",self)
        
        customer.addAction(add_customer)
        


        bank_info=menubar.addMenu("Banka Bilgi")
        
        bank_transaction = QAction("Banka İşlem Geçmişi ve Deadlock Analiz",self)
        bank_state_info = QAction("Banka Genel Durumu",self)
        
        bank_info.addActions([bank_transaction,bank_state_info])
        

      
        rate_and_interest=menubar.addMenu("Kur ve Faiz")

        add_exchange_rate=QAction("Yeni Kur Ekleme",self)
        update_exchange_rate=QAction("Kur Fiyatı Belirleme",self)
        interest=QAction("Kredi ve Gecikme Faiz Oranını Belirleme",self)

        rate_and_interest.addActions([add_exchange_rate,update_exchange_rate,interest])
         
   
 
        salary=menubar.addMenu("Maaş")
        update_salary=QAction("Çalışan Maaş  Belirleme",self)
        salary.addAction(update_salary)

             
        System=menubar.addMenu("Sistem")
        forward_system=QAction("sistemi İlerletme",self)
        System.addAction(forward_system)

        customer.triggered.connect(self.response)
        bank_info.triggered.connect(self.response)
        rate_and_interest.triggered.connect(self.response)
        salary.triggered.connect(self.response)
        System.triggered.connect(self.response)

    def response(self,action):
        if action.text() == "Müşteri Ekleme":
            tabtitle = action.text()
            self.open.new_tab(add_customer(),tabtitle)
        elif action.text() == "Banka İşlem Geçmişi ve Deadlock Analiz":
            tabtitle = action.text() 
            self.open.new_tab(bank_transaction(),tabtitle)
        elif action.text() == "Banka Genel Durumu":
            tabtitle = action.text() 
            self.open.new_tab(bank_state_info(),tabtitle)
        elif action.text() == "Yeni Kur Ekleme":
            tabtitle = action.text() 
            self.open.new_tab(add_exchange_rate(),tabtitle)
        elif action.text() == "Kur Fiyatı Belirleme":
            tabtitle = action.text() 
            self.open.new_tab(update_exchange_rate(),tabtitle)
        elif action.text() == "Kredi ve Gecikme Faiz Oranını Belirleme":
            tabtitle = action.text() 
            self.open.new_tab(interest(),tabtitle)
        elif action.text() == "Çalışan Maaş  Belirleme":
            tabtitle = action.text() 
            self.open.new_tab(update_salary(),tabtitle)
        elif action.text() == "Sistemi İlerletme":
            tabtitle = action.text() 
            self.open.new_tab(add_exchange_rate(),tabtitle)
            

    
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget=QTabWidget()
        self.tabwidget.addTab(add_customer(),"Müşteri Ekleme")
        self.tabwidget.setTabsClosable(True)
        h_box=QHBoxLayout()
        h_box.addWidget(self.tabwidget)
        self.setLayout(h_box)
        self.tabwidget.tabCloseRequested.connect(self.close_function)
        self.show()

    def close_function(self,index):
        self.tabwidget.removeTab(index)

    def new_tab(self,w_name,tabtitle):
        self.tabwidget.addTab(w_name,tabtitle)

class add_customer(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        

        self.user_no = QLabel("Müşteri No/T.C. No")
        self.user_no_i = QLineEdit()
        
        
        self.user_name = QLabel("İsim Soyisim")
        self.user_name_i = QLineEdit()
      

        self.user_pass = QLabel("Şifre")
        self.user_pass_i = QLineEdit()


        self.user_phone = QLabel("Telefon Numarası")
        self.user_phone_i = QLineEdit()


        self.user_mail = QLabel("E-posta")
        self.user_mail_i = QLineEdit()


        self.user_address = QLabel("Adres")
        self.user_address_i= QLineEdit()

        self.save_button = QPushButton("Kayıt Et")
        self.save_button.clicked.connect(self.save)


        f_box.addWidget(self.user_no)
        f_box.addWidget(self.user_no_i)
        f_box.addWidget(self.user_name)
        f_box.addWidget(self.user_name_i)
        f_box.addWidget(self.user_pass)
        f_box.addWidget(self.user_pass_i)
        f_box.addWidget(self.user_phone)
        f_box.addWidget(self.user_phone_i)
        f_box.addWidget(self.user_mail)
        f_box.addWidget(self.user_mail_i)
        f_box.addWidget(self.user_address)
        f_box.addWidget(self.user_address_i)
        f_box.addWidget(self.save_button)

        self.setLayout(f_box)

    def save(self):
        query=" SELECT temsilci_id, count(temsilci_id) as sıralama FROM public.müşteri_bilgisi_tablosu	group by temsilci_id order by sıralama asc limit 1"
        raw_data=DB.Query(DB,query,None)
        if(raw_data==None  or raw_data== [] or raw_data[0][0] == None ):
            query="SELECT temsilci_id, isim_soyisim FROM public.temsilci_tablosu;"
            raw_data=DB.Query(DB,query,None)
        
        user_No = self.user_no_i.text()
        name= self.user_name_i.text()
        password = self.user_pass_i.text()
        phone = self.user_phone_i.text()
        mail = self.user_mail_i.text()
        address=self.user_address_i.text()
        query="INSERT INTO public.müşteri_bilgisi_tablosu (müsteri_no_tc, isim_soyisim, şifre, telefon_no, e_posta, adres) VALUES (%s,%s, %s, %s,%s, %s);"
        DB.Query(DB,query,user_No,name,password,phone,mail,address,raw_data[0][0]) 

        QMessageBox.about(self,"Bildirim","Yeni Müşteri Eklendi")
    

class add_exchange_rate(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()      
        self.rate_name = QLabel("Kur İsmi")
        self.rate_name_i = QLineEdit()
        
        
        self.rate_value = QLabel("Kur Fiyatı")
        self.rate_value_i = QLineEdit()

        self.save_button = QPushButton("Yeni Kuru Kayıt Et")
        self.save_button.clicked.connect(self.save)
        
        f_box.addWidget(self.rate_name)
        f_box.addWidget(self.rate_name_i)
        f_box.addWidget(self.rate_value)
        f_box.addWidget(self.rate_value_i)
        f_box.addWidget(self.save_button)
       
        self.setLayout(f_box)
    
    def save(self):
        name=self.rate_name_i.text()
        value=self.rate_value_i.text()
        query="Select COUNT (kur_id)From public.kurlar_tablosu"
        
        amount=DB.Query(DB,query,name,value) 
        a=amount[0]
        
        query="INSERT INTO public.kurlar_tablosu(kur_id, kur_ismi, kur_fiyatı) VALUES (%s ,%s ,%s);"
        self.raw_data=DB.Query(DB,query,a,name,value) 
        
        QMessageBox.about(self,"Bildirim","Yeni Kur Eklendi")

class update_exchange_rate(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()    

        self.combo_kind = QComboBox(self)
        query="SELECT*FROM kurlar_tablosu order by kur_id"
        self.raw_data=DB.Query(DB,query) 
     
        for i in self.raw_data:
            self.combo_kind.addItem(str(i[1]))
        
        self.rate_kind_label=QLabel()
        self.rate_kind_label.setText("Kur seçiniz")
        self.new_rate_info=QLabel()
        self.new_rate_info.setText("Yeni fiyatı giriniz")
        self.rate_amount_label=QLabel()
        self.rate_amount_label_i = QLineEdit()
        
        
        self.combo_kind.activated[str].connect(self.onChanged)      
                
    
   

        self.save_button = QPushButton("Güncelle")
        self.save_button.clicked.connect(self.save)  
        f_box.addWidget(self.rate_kind_label)
        f_box.addWidget(self.combo_kind)
        f_box.addWidget(self.rate_amount_label)
        f_box.addWidget(self.new_rate_info)
        f_box.addWidget(self.rate_amount_label_i)
        f_box.addWidget(self.save_button)
        self.setLayout(f_box)

    def onChanged(self, text):
        self.rate_index=self.combo_kind.currentIndex()
        
        self.rate_amount_label.setText("Anlık "+text +" Fiyatı :"+str(self.raw_data[self.rate_index][2]))
        self.rate_amount_label.adjustSize()
        

    def save(self):
        query="UPDATE public.kurlar_tablosu SET kur_id= %s, kur_ismi=%s, kur_fiyatı= %s WHERE kur_id=%s;"
        cur_kind_id= self.combo_kind.currentIndex()
        new_amount=self.rate_amount_label_i.text()
        DB.Query(DB,query,cur_kind_id,str(self.raw_data[self.rate_index][1]),new_amount,cur_kind_id) 
       
     
        QMessageBox.about(self,"Bildirim","Kur Fiyatı Güncellendi")

class update_salary(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        query="SELECT*FROM maaş_tablosu order by maaş_id"
        self.raw_data=DB.Query(DB,query) 


        self.textlabel=QLabel()
        self.textlabel.setText("Anlık Maaş Miktarı :"+str(self.raw_data[0][1]))
       
        self.update_salary_label=QLabel("Yeni Maaş Miktarı Giriniz")
        self.update_salary_label_i = QLineEdit(str(self.raw_data[0][1]))

      
        self.save_button = QPushButton("Yeni Maaş Miktarı Belirle")
        self.save_button.clicked.connect(self.save)  

        f_box.addWidget(self.textlabel)
        f_box.addWidget(self.update_salary_label)
        f_box.addWidget(self.update_salary_label_i)
        f_box.addWidget(self.save_button)
        self.setLayout(f_box)
    
    
    def save(self):
        value=self.update_salary_label_i.text()
        query=" UPDATE public.maaş_tablosu SET maaş_id = 0, maaş_miktarı=%s WHERE  maaş_id=0;"
        self.raw_data=DB.Query(DB,query,value) 
        QMessageBox.about(self,"Bildirim","Yeni Maaş Miktarı Belirlendi")



class interest(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        query= "SELECT * FROM public.faiz_tablosu ORDER BY faiz_id ASC "
        self.raw_data=DB.Query(DB,query) 
        self.textlabel=QLabel()
        self.textlabel.setText("Anlık Kredi Faiz Oranı :"+str(self.raw_data[0][2])+" \nAnlık Gecikme Faiz Oranı :"+str(self.raw_data[1][2]))
       
        self.interest_label=QLabel("Yeni kredi faiz oranı giriniz")
        self.interest_label_i = QLineEdit(str(self.raw_data[0][2]))
        self.delay_interest_label=QLabel("Yeni Gecikme Faiz Oranı Giriniz")
        self.delay_interest_label_i = QLineEdit(str(self.raw_data[1][2]))

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save)  

        f_box.addWidget(self.textlabel)
        f_box.addWidget(self.interest_label)
        f_box.addWidget(self.interest_label_i)
        f_box.addWidget(self.delay_interest_label)
        f_box.addWidget(self.delay_interest_label_i)
        f_box.addWidget(self.save_button)
        self.setLayout(f_box)

    def save(self):
        interest_value=self.interest_label_i.text()
        delay_interest_value=self.delay_interest_label_i.text()
        query= "UPDATE public.faiz_tablosu SET faiz_id = 0, faiz_adı='kredi faizi', faiz_miktarı=%s WHERE faiz_id=0;"
        self.raw_data=DB.Query(DB,query,interest_value) 
        query= "UPDATE public.faiz_tablosu SET faiz_id = 1, faiz_adı='geçikme faizi', faiz_miktarı=%s WHERE faiz_id=1;"
        self.raw_data=DB.Query(DB,query,delay_interest_value) 
        QMessageBox.about(self,"Bildirim","Faiz Oranları Güncellendi")

class bank_transaction(QWidget):
    def __init__(self):
        super().__init__()
        query="SELECT COUNT(islem_no_id) FROM public.İşlem_tablosu ;"
        amount=DB.Query(DB,query,None) 
        
        a=amount[0][0]
        
        f_box = QFormLayout()
        h_box= QHBoxLayout()
        table_headers=["İşlem No","Kaynak","Hedef","İşlem","Tutar","Kaynak Bakiye","Hedef Bakiye","Tarih"]
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.textlabel=QLabel("İşlem Miktarı :"+str(a))
        self.bank_transaction=QLabel("Görmek İstediğiniz İşlem Miktarı Giriniz")
        self.bank_transaction_i = QLineEdit(str(a))
        self.load_button = QPushButton("İşlemleri Listele")
        self.load_button.clicked.connect(self.load)
        self.Deadlock_button = QPushButton("Listelenen İşlemlere Deadlock Analizi Yap")
        self.Deadlock_button.clicked.connect(self.Deadlock)  

        f_box.addWidget(self.textlabel)
        f_box.addWidget(self.bank_transaction)
        f_box.addWidget(self.bank_transaction_i)
        h_box.addWidget(self.load_button)
        h_box.addWidget(self.Deadlock_button)
    
      
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
    def load(self):
        query="SELECT * FROM public.İşlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
 
        


    def Deadlock(self):
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(self.raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
      



class bank_state_info(QWidget):
    def __init__(self):
        super().__init__()
        query="SELECT COUNT(islem_no_id) FROM public.İşlem_tablosu ;"
        amount=DB.Query(DB,query,None) 
        
        f_box = QFormLayout()
        h_box= QHBoxLayout()
        table_headers=["İşlem No","Kaynak","Hedef","İşlem","Tutar","Kaynak Bakiye","Hedef Bakiye","Tarih"]
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)      
        
        self.load_button = QPushButton("Listele")
        self.load_button.clicked.connect(self.load)
        
        h_box.addWidget(self.load_button)
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()


    def load(self):
        query="SELECT * FROM public.İşlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))







        
app = QApplication(sys.argv)
Win = MainWindow()
sys.exit(app.exec_())