from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem,QDialog
from PyQt5.QtCore import QDate,QDateTime,Qt
from PyQt5 import QtGui
import sys

import numpy as np

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
        forward_system=QAction("Sistemi İlerletme",self)
        database_system=QAction("Sistem veritabanı",self)
        System.addAction(forward_system)
        System.addAction(database_system)

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
            self.open.new_tab(forward_system(),tabtitle)
        elif action.text() == "Sistem veritabanı":
            tabtitle = action.text() 
            self.open.new_tab(database_system(),tabtitle)
            

    
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
        if(raw_data==None  or raw_data== []  ):
            query="SELECT temsilci_id, isim_soyisim FROM public.temsilci_tablosu;"
            raw_data=DB.Query(DB,query,None)
        
        user_No = self.user_no_i.text()
        name= self.user_name_i.text()
        password = self.user_pass_i.text()
        phone = self.user_phone_i.text()
        mail = self.user_mail_i.text()
        address=self.user_address_i.text()
        query="INSERT INTO public.müşteri_bilgisi_tablosu (müsteri_no_tc, isim_soyisim, şifre, telefon_no, e_posta, adres,temsilci_id) VALUES (%s,%s, %s, %s,%s, %s,%s);"
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
        if(self.raw_data==None  or self.raw_data== [] ):
            query="INSERT INTO public.maaş_tablosu(maaş_id, maaş_miktarı)VALUES (%s, %s);"
            self.raw_data=DB.Query(DB,query,1,4000)


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
        query="SELECT COUNT(islem_no_id) FROM public.işlem_tablosu ;"
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
        self.load()

    def load(self):
        self.amount=self.bank_transaction_i.text()
        query="SELECT * FROM public.işlem_tablosu ORDER BY islem_no_id desc LIMIT %s ;"
        raw_data=DB.Query(DB,query,self.amount) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
 
        


    def Deadlock(self):
        will_want=[]
        query="SELECT is2.islem_no_id ,is2.islem_kaynak,is2.islem_hedef,is2.tarih FROM public.işlem_tablosu as is1, public.işlem_tablosu as is2  WHERE is2.islem_kaynak=is1.islem_hedef and is2.tarih=is1.tarih group by is2.islem_no_id ORDER BY is2.tarih,is2.islem_no_id ASC LIMIT %s"
        raw_data=DB.Query(DB,query,self.amount)
        for j in  range(0,len(raw_data)):
            will_want.append(raw_data[j][0])

        loop_amount=len(raw_data)
        total_list=[]
        next_wanted_amount=0
        
        
        total_amount=0
        for k in range(0,loop_amount-1):
            wanted_list=[]              
                        
            first_wanted=raw_data[k+next_wanted_amount][1]
            wanted=raw_data[k+next_wanted_amount][1]                        
            wanted_list.append(k)


            i=0
            while i<len(raw_data):
                if(wanted == raw_data[i][2] ):
                    if(first_wanted==raw_data[i][2] and first_wanted!=wanted):
                        break
                        
                    wanted= raw_data[i][1]
                    print("*"+wanted)
                    
                    if(wanted_list[0]==raw_data[i][0] ):
                        break
                    wanted_list.append(raw_data[i][0])
                    i=0 
                i+=1  


            next_wanted_amount=len(wanted_list)-1
                      
            total_amount+=len(wanted_list)
            
            if( total_amount>len(will_want) or  1==len(wanted_list) ):
                break
            
            total_list.append(wanted_list)         
            del wanted_list
         
        QMessageBox.about(self,"Bildirim","Analiz yapıldı: \n \t"+str(total_list))

class bank_state_info(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box= QHBoxLayout()

        table_headers=["Banka Toplam bakiye ","Gelir ","Gider"]
        self.table = QTableWidget()
        self.table.setColumnCount(3)
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
        query="SELECT  banka_anapara,banka_tarih FROM public.banka_bilgisi_tablosu;"
        raw_data=DB.Query(DB,query,None)
        date = QDateEdit((QDate(raw_data[0][1]).addDays(1*-1*30)))
        print(date.text())

        
        income_q = "SELECT SUM(tutar) FROM public.işlem_tablosu WHERE islem_hedef = 'Banka' AND tarih > %s"
        income =  DB.Query(DB,income_q,date.text())

        expense_q = "SELECT SUM(tutar) FROM public.işlem_tablosu WHERE islem_kaynak = 'BANKA' AND tarih > %s" 
        expense =  DB.Query(DB,expense_q,date.text()) 


        
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            
            self.table.setItem(row_number,0,QTableWidgetItem(str(raw_data[0][0])))
            self.table.setItem(row_number,1,QTableWidgetItem(str(income[0][0])))
            self.table.setItem(row_number,2,QTableWidgetItem(str(expense[0][0])))




class forward_system(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        query="SELECT * FROM public.banka_bilgisi_tablosu ORDER BY banka_id ASC "
        raw_data=DB.Query(DB,query,None)
          

        self.datetimeedit = QDateEdit(QDate(raw_data[0][2]),self)
        self.info_label = QLabel("Buaray bilgilendirme yazılacak")
        self.forward_button = QPushButton("Sistemi ilerletme")
        self.forward_button.clicked.connect(self.load)
        
        f_box.addWidget(self.info_label)
        f_box.addWidget(self.datetimeedit)
        f_box.addWidget(self.forward_button)
       
        self.setLayout(f_box)


    def load(self):
        time_date=self.datetimeedit.text()
        
        query="UPDATE public.banka_bilgisi_tablosu SET banka_tarih=%s WHERE banka_id=1; "
        DB.Query(DB,query,time_date)
        query="SELECT count (temsilci_id) FROM public.temsilci_tablosu; "
        customer_agent_amount=DB.Query(DB,query,None)
        print(customer_agent_amount)
        query="SELECT * FROM public.maaş_tablosu ORDER BY maaş_id ASC  "
        salary_amount=DB.Query(DB,query,None)
        print(salary_amount)
        salary_total=customer_agent_amount[0][0]*salary_amount[0][1]
        print(salary_total)
        query="UPDATE public.banka_bilgisi_tablosu SET  banka_anapara=banka_anapara-%s WHERE banka_id=1"
        DB.Query(DB,query,salary_total)

        #işlemi kaydetme
        query="SELECT COUNT(islem_no_id) FROM public.işlem_tablosu"
        p_key = DB.Query(DB,query)
        query = "INSERT INTO public.işlem_tablosu (islem_no_id, islem_kaynak, islem_hedef, işlem_çeşidi, tutar, kaynak_bakiye, hedef_bakiye, tarih) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        DB.Query(DB,query,p_key[0][0],'BANKA','Temsilciler','Maaş ödeme',salary_total,0,0,time_date)

        

        QMessageBox.about(self,"Bildirim","Sistem ilerledi"+time_date)


class database_system(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box= QHBoxLayout()
        

        self.ER_image =QLabel(self)
        self.ER_image.setPixmap(QtGui.QPixmap("sql.png"))
        #self.ER_image.setGeometry(0,0,1400,850)
        h_box.addWidget(self.ER_image)

        f_box.addItem(h_box)
        self.setLayout(f_box)
   

        
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle(" Banak Giriş")
        f_box = QVBoxLayout(self)
        self.setMinimumSize(300,200)
        self.user =QLabel("Banka No")
        self.password =QLabel("Şifre")
        self.user_i = QLineEdit(self)
        self.password_i = QLineEdit(self)
        self.buttonLogin = QPushButton('GİRİŞ ', self)
        self.buttonLogin.clicked.connect(self.login_control)
        
        f_box.addWidget(self.user)
        f_box.addWidget(self.user_i)
        f_box.addWidget(self.password)
        f_box.addWidget(self.password_i)
        f_box.addWidget(self.buttonLogin)
        self.setLayout(f_box)

    def login_control(self):
        global active_customer_agent_no
        global active_customer_agent_name

        user=self.user_i.text()
        password=self.password_i.text()
        
        query="SELECT * FROM public.banka_müdür_tablosu where banka_müdür_id=%s and şifre =%s "
        result=DB.Query(DB,query,user,password)
       
        if(result == [] or result==None):
            QMessageBox.warning(
                self, 'Error', 'kullanıcı no veya şifre yanlış')
        else:
            
            active_customer_agent_no=result[0][0]
            active_customer_agent_name=result[0][1]
            self.accept()
            


if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        Win = MainWindow()
        sys.exit(app.exec_())