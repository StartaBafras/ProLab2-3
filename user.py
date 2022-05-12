from cgi import print_arguments, print_form
from glob import glob
from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem,QDialog
from PyQt5.QtCore import QDate,QDateTime,Qt
import sys

from numpy import piecewise
from DataAccess.data import DB



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAnk 0F SYStem")
        self.create_menu()
        self.setMinimumSize(900,500)
        self.open=Window()
        self.setCentralWidget(self.open) 
        self.show()
    def create_menu(self):
        menubar = self.menuBar()
    
        
        operation=menubar.addMenu("İşlemler")


        money_withdraw_deposit= QAction("para yatırma ve çekme",self)

        debt_payment=QAction("kredi borçu ödeme",self)
        money_transfer=QAction("Tranfer yapma",self)
        operation.addActions([ money_withdraw_deposit,debt_payment,money_transfer ])
        

   
        user_info=menubar.addMenu("Bilgi")
        
        user_credit_info=QAction("kredi borçu bilgisi",self)
        user_transaction_info = QAction("işlem geçmişi",self)
        update_user_info = QAction("kişisel bilgi güncelleme",self)
        
        user_info.addActions([user_credit_info,user_transaction_info ,update_user_info])
        

        

        user_request=menubar.addMenu("Talep Etme")

        credit_requst_user=QAction("kredi talebi oluştur",self)
        open_user_account=QAction("hesap açma talebi oluştur",self)
        delete_user_account=QAction("hesap silme talebi oluştur",self)

        user_request.addActions([credit_requst_user,open_user_account,delete_user_account])
    
    
        
        operation.triggered.connect(self.response)
        user_info.triggered.connect(self.response)
        user_request.triggered.connect(self.response)


    def response(self,action):
        if action.text() == "para yatırma ve çekme":
            tabtitle = action.text()
            self.open.new_tab(money_withdraw_deposit(),tabtitle)
        elif action.text() == "kredi borçu ödeme":
            tabtitle = action.text() 
            self.open.new_tab(debt_payment(),tabtitle)
        elif action.text() == "Tranfer yapma":
            tabtitle = action.text() 
            self.open.new_tab(money_transfer(),tabtitle)
        elif action.text() == "kredi borçu bilgisi":
            tabtitle = action.text() 
            self.open.new_tab(user_credit_info(),tabtitle)
        elif action.text() == "işlem geçmişi":
            tabtitle = action.text() 
            self.open.new_tab(user_transaction_info(),tabtitle)
        elif action.text() == "kişisel bilgi güncelleme":
            tabtitle = action.text() 
            self.open.new_tab(update_user_info(),tabtitle)
        elif action.text() == "kredi talebi oluştur":
            tabtitle = action.text() 
            self.open.new_tab(credit_requst_user(),tabtitle)
        elif action.text() == "hesap açma talebi oluştur":
            tabtitle = action.text() 
            self.open.new_tab(open_user_account(),tabtitle)
        elif action.text() == "hesap silme talebi oluştur":
            tabtitle = action.text() 
            self.open.new_tab(delete_user_account(),tabtitle)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget=QTabWidget()
        self.tabwidget.addTab(money_withdraw_deposit(),"para yatırma ve çekme")
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

class credit_requst_user(QWidget): ## Şu anki faiz oranı ekrana yazdırılacak ve ödenecek borç miktarı onay butonunda gösterilecek.
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        self.main_money = QLabel("Ana para miktarı")
        self.main_money_i = QLineEdit()
        
        
        self.credit_term = QLabel("vade sayısı/ay")
        self.credit_term_i = QLineEdit()

        self.save_button = QPushButton("Kayıt Et")
        self.save_button.clicked.connect(self.request)

        f_box.addWidget(self.main_money)
        f_box.addWidget(self.main_money_i)
        f_box.addWidget(self.credit_term)
        f_box.addWidget(self.credit_term_i)
        f_box.addWidget(self.save_button)
        self.setLayout(f_box)


    def request(self):
        global active_user_no

        main_money = self.main_money_i.text()
        term = self.credit_term_i.text()

        customer_q = "SELECT temsilci_id FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc=%s;"
        customer_id = DB.Query(DB,customer_q,active_user_no) #Temsilci id bulundu
        
        
        credit_id = "SELECT talep_id FROM public.kredi_talep_tablosu WHERE talep_id >= all(SELECT talep_id FROM public.kredi_talep_tablosu);"
        credit_id = DB.Query(DB,credit_id) # Benzersiz anahtarın en son kaçıncı yerde kaldığı bulundu

        query="INSERT INTO public.kredi_talep_tablosu (talep_id, talep_eden_id, talep_edilen_id, ana_para, vade_sayısı, talep_durumu)VALUES (%s, %s, %s, %s, %s, %s);"
        
        control_zero = len(credit_id) # İlk giriş olup olmadığı kontrol ediliyor 

        try:
            if control_zero == 0:
                raw_data=DB.Query(DB,query,1,active_user_no,customer_id[0][0],main_money,term,0)
                QMessageBox.about(self,"Bildirim","Talep Alındı")

            else:
                raw_data=DB.Query(DB,query,credit_id[0][0]+1,active_user_no,customer_id[0][0],main_money,term,0)
                QMessageBox.about(self,"Bildirim","Talep Alındı")

        except IndexError:
                QMessageBox.about(self,"Hata","İndex Hatası")
        



class user_transaction_info(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        table_headers=["İşlem No","Kaynak","Hedef","İşlem","Tutar","Kaynak Bakiye","Hedef Bakiye","Tarih"]
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("İşlemleri  gör")
        self.load_button.clicked.connect(self.load)

   
        h_box.addWidget(self.load_button)
      
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
    def load(self):
        query="SELECT * FROM public.işlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))



class open_user_account(QWidget):
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()

        self.combo_kind = QComboBox(self)
        query="SELECT  kur_id,kur_ismi FROM kurlar_tablosu order by kur_id"
        raw_data=DB.Query(DB,query) 
     
        for i in raw_data:
            self.combo_kind.addItem(str(i[1])) 
        
        self.kind_label=QLabel()
        self.kind_label.setText("Hesap türü seçiniz")



        self.save_button = QPushButton("talep oluştur")
        self.save_button.clicked.connect(self.request)  
        f_box.addWidget(self.kind_label)
        f_box.addWidget(self.combo_kind)
        f_box.addWidget(self.save_button)
        self.setLayout(f_box)
    

    def request(self,i):
        global active_user_no

        cur_kind_id= self.combo_kind.currentIndex()
        print(cur_kind_id)

        customer_q = "SELECT temsilci_id FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc=%s;"
        customer_id = DB.Query(DB,customer_q,active_user_no)

        query="Select COUNT (talep_id) From public.hesap_açma_talep_tablosu"
        
        key_id=DB.Query(DB,query)
        key=key_id[0]

        save_request="INSERT INTO public.hesap_açma_talep_tablosu (talep_id, talep_eden_id, talep_edilen_id, kur_id, talep_durumu)VALUES (%s, %s, %s, %s, %s);"

        DB.Query(DB,save_request,key,active_user_no,customer_id[0][0],cur_kind_id,0)
        QMessageBox.about(self,"Bildirim","Talep Alındı")



class update_user_info(QWidget):

    global active_user_no

    def __init__(self):
        super().__init__()

        f_box = QFormLayout()

        query="SELECT* FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc = %s;"
        self.raw_data=DB.Query(DB,query,active_user_no)
        print(self.raw_data)

        self.user_no = QLabel("Müşteri No/T.C No")
        self.user_no_i = QLineEdit(str(self.raw_data[0][0]))
        
        
        self.user_name = QLabel("İsim Soyisim")
        self.user_name_i = QLineEdit(str(self.raw_data[0][1]))
      

        self.user_pass = QLabel("Şifre")
        self.user_pass_i = QLineEdit(str(self.raw_data[0][2]))
       

        self.user_phone = QLabel("Telefon Numarası")
        self.user_phone_i = QLineEdit(str(self.raw_data[0][3]))


        self.user_mail = QLabel("E-posta")
        self.user_mail_i = QLineEdit(str(self.raw_data[0][4]))
        

        self.user_address = QLabel("Adres")
        self.user_address_i= QLineEdit(str(self.raw_data[0][5]))

        self.save_button = QPushButton("Kayıt Et")
        self.save_button.clicked.connect(self.update_func)


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

    def update_func(self):
        user_No = self.user_no_i.text()
        name= self.user_name_i.text()
        password = self.user_pass_i.text()
        phone = self.user_phone_i.text()
        mail = self.user_mail_i.text()
        address=self.user_address_i.text()
        query="UPDATE public. müşteri_bilgisi_tablosu SET  müsteri_no_tc =%s, isim_soyisim=%s, şifre=%s, telefon_no=%s, e_posta=%s, adres=%s WHERE müsteri_no_tc =%s ;"
        DB.Query(DB,query,user_No,name,password,phone,mail,address,active_user_no) 

        QMessageBox.about(self,"Bildirim","Bilgileriniz Başarıyla Güncellendi")


class money_withdraw_deposit(QWidget):
    global active_user_agent_no
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        table_headers=["Hesap No","Bakiye","Birimi"]
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.amount_money = QLabel("TUTAR:")
        self.amount_money_i = QLineEdit("0")
        self.push_button = QPushButton("parayı yatır ")
        self.push_button.clicked.connect(self.push)
        self.pull_button = QPushButton("parayı çek ")
        self.pull_button.clicked.connect(self.pull)


   
        h_box.addWidget(self.push_button)
        h_box.addWidget(self.pull_button)
      
        f_box.addWidget(self.table)
        f_box.addWidget(self.amount_money)
        f_box.addWidget(self.amount_money_i)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()
    
    def load(self):
        query="SELECT hesap_id,bakiye,hesap_türü FROM public.müşteri_hesap_tablosu  WHERE müşteri_no= %s ORDER BY hesap_id;"
        raw_data=DB.Query(DB,query,active_user_no) 

        if raw_data != None:
            new_data = []

            exchange_rate_q = "SELECT kur_ismi FROM public.kurlar_tablosu WHERE kur_id=%s"

            for i in raw_data:
                i = list(i)
                exchange_rate = DB.Query(DB,exchange_rate_q,i[2])
                i[2] = exchange_rate[0][0]
                new_data.append(i)
                

            self.table.setRowCount(0)
            for row_number, row_data in enumerate(new_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    
    def pull(self):
        try:
            account_no= self.table.item(self.table.currentRow(),0).text()
            balance = self.table.item(self.table.currentRow(),1).text()
            amount = self.amount_money_i.text()
            exchange_rate = self.table.item(self.table.currentRow(),2).text()

            balance_query="UPDATE public.müşteri_hesap_tablosu SET bakiye=%s  WHERE hesap_id=%s;"
            amount_new = float(float(balance)-float(amount))
            DB.Query(DB,balance_query,amount_new,account_no)
            

            actine_user_name_q = "SELECT isim_soyisim FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc = %s"
            user_name = DB.Query(DB,actine_user_name_q,active_user_no)

            p_key_q="SELECT COUNT(islem_no_id) FROM public.işlem_tablosu"
            p_key = DB.Query(DB,p_key_q)

            
            save_process_q = "INSERT INTO public.işlem_tablosu (islem_no_id, islem_kaynak, islem_hedef, işlem_çeşidi, tutar, kaynak_bakiye, hedef_bakiye, tarih) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            DB.Query(DB,save_process_q,p_key[0][0],account_no,user_name[0][0],'Para Çekme',amount,balance,amount_new,'2017-03-14')

            QMessageBox.about(self,"Bildirim",str(amount) + exchange_rate +" çekildi")
            self.load()
            
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir hesap seçimi yapılmadı")

       
    def push(self):
        try:
            account_no= self.table.item(self.table.currentRow(),0).text()
            balance = self.table.item(self.table.currentRow(),1).text()
            amount = self.amount_money_i.text()
            exchange_rate = self.table.item(self.table.currentRow(),2).text()

            balance_query="UPDATE public.müşteri_hesap_tablosu SET bakiye=%s  WHERE hesap_id=%s;"
            amount_new = float(float(balance)+float(amount))
            DB.Query(DB,balance_query,amount_new,account_no)


            actine_user_name_q = "SELECT isim_soyisim FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc = %s"
            user_name = DB.Query(DB,actine_user_name_q,active_user_no)

            p_key_q="SELECT COUNT(islem_no_id) FROM public.işlem_tablosu"
            p_key = DB.Query(DB,p_key_q)

            
                
            save_process_q = "INSERT INTO public.işlem_tablosu (islem_no_id, islem_kaynak, islem_hedef, işlem_çeşidi, tutar, kaynak_bakiye, hedef_bakiye, tarih) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            DB.Query(DB,save_process_q,p_key[0][0],account_no,user_name[0][0],'Para Yatırma',amount,balance,amount_new,'2017-03-14')

            QMessageBox.about(self,"Bildirim",str(amount) + exchange_rate +" yatırıldı")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir hesap seçimi yapılmadı")

class debt_payment(QWidget):
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        table_headers=["İşlem No","Kaynak","Hedef","İşlem","Tutar","Kaynak Bakiye","Hedef Bakiye","Tarih"]
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.amount_money = QLabel("Taksit Tutarı :")
        self.amount_money_i = QLineEdit("0")
        self.push_button = QPushButton("Borcu yatır ")
        self.push_button.clicked.connect(self.push)

        h_box.addWidget(self.push_button)
    
      
        f_box.addWidget(self.table)
        f_box.addWidget(self.amount_money)
        f_box.addWidget(self.amount_money_i)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()
    def load(self):
        query="SELECT * FROM public.işlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def push(self):
        print( "yattı")
        QMessageBox.about(self,"bildirim","Borç ödemesi yapıldı")


class money_transfer(QWidget):
    global active_user_no
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()
        h_box = QHBoxLayout()

        table_headers=["Hesap No","Bakiye","Birimi"]
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.target_account = QLabel("Hedef Hesap")
        self.combo_kind = QComboBox(self)

        #query="SELECT h.hesap_id b.ad_soyad FROM pulic.müşteri_hesap_tablosu as h, müşteri_bilgi_tablosu as b"
        query="SELECT b.isim_soyisim, h.hesap_id, k.kur_ismi FROM public.müşteri_hesap_tablosu as h, public.müşteri_bilgisi_tablosu as b, public.kurlar_tablosu as k WHERE h."
        self.raw_data=DB.Query(DB,query) 

        for i in self.raw_data:
            self.combo_kind.addItem("Kullanıcı: " + str(i[0]) + " Hesap No: " + str(i[1]))
        

        self.amount_money = QLabel("TUTAR :")
        self.amount_money_i = QLineEdit("0")
        self.push_button = QPushButton("Taranfer yap ")
        self.push_button.clicked.connect(self.push)

        h_box.addWidget(self.push_button)
    
      
        f_box.addWidget(self.table)
        f_box.addWidget(self.target_account)
        f_box.addWidget(self.combo_kind)
        f_box.addWidget(self.amount_money)
        f_box.addWidget(self.amount_money_i)
        f_box.addItem(h_box)
        self.setLayout(f_box)

        #self.load()
    def load(self):
        """
        #query="SELECT hesap_id,bakiye,hesap_türü FROM public.müşteri_hesap_tablosu  WHERE müşteri_no= %s ORDER BY hesap_id;"
        #raw_data=DB.Query(DB,query,active_user_no) 

        if raw_data != None:
            new_data = []

            exchange_rate_q = "SELECT kur_ismi FROM public.kurlar_tablosu WHERE kur_id=%s"

            for i in raw_data:
                i = list(i)
                exchange_rate = DB.Query(DB,exchange_rate_q,i[2])
                i[2] = exchange_rate[0][0]
                new_data.append(i)
                

            self.table.setRowCount(0)
            for row_number, row_data in enumerate(new_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))"""

    def push(self):
        print( "yattı")
        QMessageBox.about(self,"bildirim","Para Transferi yapıldı")



class user_credit_info(QWidget):
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        table_headers=["İşlem No","Kaynak","Hedef","İşlem","Tutar","Kaynak Bakiye","Hedef Bakiye","Tarih"]
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()

    def load(self):
        query="SELECT * FROM public.işlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))



class delete_user_account(QWidget):
    global active_user_no
    def __init__(self):
        super().__init__()  
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        table_headers=["Hesap No","Bakiye","Birimi"]
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.delete_button = QPushButton("Hesabı Sil")
        self.delete_button.clicked.connect(self.delete)


        f_box.addWidget(self.table)
        f_box.addWidget(self.delete_button)

        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()

    def load(self):
        query="SELECT hesap_id,bakiye,hesap_türü FROM public.müşteri_hesap_tablosu  WHERE müşteri_no= %s ORDER BY hesap_id;"
        raw_data=DB.Query(DB,query,active_user_no) 

        if raw_data != None:
            new_data = []

            exchange_rate_q = "SELECT kur_ismi FROM public.kurlar_tablosu WHERE kur_id=%s"

            for i in raw_data:
                i = list(i)
                exchange_rate = DB.Query(DB,exchange_rate_q,i[2])
                i[2] = exchange_rate[0][0]
                new_data.append(i)
                

            self.table.setRowCount(0)
            for row_number, row_data in enumerate(new_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def delete(self):
        account_no= self.table.item(self.table.currentRow(),0).text()


        customer_q = "SELECT temsilci_id FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc=%s;"
        customer_id = DB.Query(DB,customer_q,active_user_no)

        query="Select COUNT(talep_id) From public.hesap_silme_talep_tablosu"
        
        key_id=DB.Query(DB,query)
        key=key_id[0]

        save_request="INSERT INTO public.hesap_silme_talep_tablosu (talep_id, talep_eden_id, talep_edilen_id, silinecek_hesap_no, talep_durumu)VALUES (%s, %s, %s, %s, %s);"

        DB.Query(DB,save_request,key,active_user_no,customer_id[0][0],account_no,0)

        QMessageBox.about(self,"Bildirim","Numarası " + account_no+ "olan hesap için hesap silme talebi alındı.")


# aktif kullanıcı bilgileri 
active_user_no=""
active_user_name=""
active_user_agent_no=-1

class Login(QDialog):
     
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle("Giriş")
        f_box = QVBoxLayout(self)
        self.setMinimumSize(300,200)
        self.user =QLabel("müşteri no")
        self.password =QLabel("sifre")
        self.user_i = QLineEdit(self)
        self.password_i = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.login_control)
        
        f_box.addWidget(self.user)
        f_box.addWidget(self.user_i)
        f_box.addWidget(self.password)
        f_box.addWidget(self.password_i)
        f_box.addWidget(self.buttonLogin)
        self.setLayout(f_box)

    def login_control(self):
        global active_user_no
        global active_user_name
        user=self.user_i.text()
        password=self.password_i.text()

        query="SELECT * FROM public.müşteri_bilgisi_tablosu where müsteri_no_tc=%s and şifre =%s "
        result=DB.Query(DB,query,user,password) #Asıl
        #result=DB.Query(DB,query,1,1)

        print(result)
        if(result == [] or result==None):
            QMessageBox.warning(
                self, 'Error', 'Müşteri No Veya Şifre Yanlış')
        else:
            active_user_no=user
            active_user_name=result[0][1]
            self.accept()
            QMessageBox.about(self, 'Hoş Geldiniz', "PiBank'a Hoş Geldin " + active_user_name)
            

if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        Win = MainWindow()
        sys.exit(app.exec_())
"""
app = QApplication(sys.argv)

Win = MainWindow()
sys.exit(app.exec_())"""