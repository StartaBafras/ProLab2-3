
from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem,QDialog
from PyQt5.QtCore import QDate,QDateTime,Qt
import sys
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
     
        customer = menubar.addMenu("müşteri işlem")

        add_customer = QAction("müşteri Ekleme",self)
        delete_customer = QAction("müşteri düzenleme ve silme",self)
        

        customer.addActions([add_customer,delete_customer ])
        

  
        customer_info=menubar.addMenu("Müşteri bilgi")
        
        customer_transaction = QAction("müşteri işlem geçmişi",self)
        customer_state_info = QAction("müşteri genel durumu",self)
        
        customer_info.addActions([customer_transaction,customer_state_info])
        

        
     
        customer_request=menubar.addMenu("Müşteri talep")

        customer_request_account_open=QAction("müşteri hesap açma talepleri",self)
        customer_request_account_delete=QAction("müşteri hesap silme talepleri",self)
        customer_request_credit=QAction("müşteri kredi talepleri",self)

        customer_request.addActions([customer_request_account_open,customer_request_account_delete,customer_request_credit])
        customer.triggered.connect(self.response)
        customer_info.triggered.connect(self.response)
        customer_request.triggered.connect(self.response)
    def response(self,action):
        if action.text() == "müşteri Ekleme":
            tabtitle = action.text()
            self.open.new_tab(add_customer(),tabtitle)
        elif action.text() == "müşteri düzenleme ve silme":
            tabtitle = action.text() 
            self.open.new_tab(delete_and_update_customer(),tabtitle)
        elif action.text() == "müşteri işlem geçmişi":
            tabtitle = action.text() 
            self.open.new_tab(customer_transaction(),tabtitle)
        elif action.text() == "müşteri genel durumu":
            tabtitle = action.text() 
            self.open.new_tab(customer_state_info(),tabtitle)
        elif action.text() == "müşteri hesap açma talepleri":
            tabtitle = action.text() 
            self.open.new_tab(customer_request_account_open(),tabtitle)
        elif action.text() == "müşteri hesap silme talepleri":
            tabtitle = action.text() 
            self.open.new_tab(customer_request_account_delete(),tabtitle)
        elif action.text() == "müşteri kredi talepleri":
            tabtitle = action.text() 
            self.open.new_tab(customer_request_credit(),tabtitle)
        
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget=QTabWidget()
        self.tabwidget.addTab(add_customer(),"müşteri Ekleme")
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
        

        self.user_no = QLabel("müşteri no/TÇ no")
        self.user_no_i = QLineEdit()
        
        
        self.user_name = QLabel("isim soyisim")
        self.user_name_i = QLineEdit()
      

        self.user_pass = QLabel("Şifre")
        self.user_pass_i = QLineEdit()


        self.user_phone = QLabel("telefon no")
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
        query="INSERT INTO public.müşteri_bilgisi_tablosu (müsteri_no_tc, isim_soyisim, şifre, telefon_no, e_posta, adres, temsilci_id) VALUES (%s,%s, %s, %s,%s, %s,%s);"
        DB.Query(DB,query,user_No,name,password,phone,mail,address,raw_data[0][0]) 

        QMessageBox.about(self,"bildirim","yeni müşteri eklendi")



class delete_and_update_customer(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
        table_headers=["Müşteri no /T.Ç. no","İsim soyisim","Şifre","Telefon numarası","E-posta","Adres"]
         
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("müşterileri gör")
        self.load_button.clicked.connect(self.load)
        self.delete_button = QPushButton("müşteriyi sil")
        self.delete_button.clicked.connect(self.delete)

        self.update_button = QPushButton("müşteriyi düzenle")
        self.update_button.clicked.connect(self.uptade_func)

        h_box.addWidget(self.update_button)
        h_box.addWidget(self.load_button)
        h_box.addWidget(self.delete_button)  
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
    def load(self):
        global active_customer_agent_no
        query="SELECT * FROM  public.müşteri_bilgisi_tablosu where temsilci_id = %s ;"
        raw_data=DB.Query(DB,query,active_customer_agent_no)
        print(raw_data,active_customer_agent_no)
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def delete(self):
        try:
            user_no = self.table.item(self.table.currentRow(),0).text()
            print(user_no)
            query="DELETE FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc = %s"
            DB.Query(DB,query,user_no)
            QMessageBox.about(self,"bildirim"," müşteri silindi")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")

    def uptade_func(self):
        print("sd")
        try:
            user_no = self.table.item(self.table.currentRow(),0).text()  
            name= self.table.item(self.table.currentRow(),1).text()
            password = self.table.item(self.table.currentRow(),2).text()
            phone =self.table.item(self.table.currentRow(),3).text()
            mail = self.table.item(self.table.currentRow(),4).text()
            address=self.table.item(self.table.currentRow(),5).text()
            print(user_no,name,password,phone,mail,address)
            query="UPDATE public.müşteri_bilgisi_tablosu SET müsteri_no_tc=%s, isim_soyisim=%s, şifre=%s, telefon_no=%s, e_posta=%s, adres=%s WHERE müsteri_no_tc=%s ;"
            DB.Query(DB,query,user_no,name,password,phone,mail,address,user_no)
            QMessageBox.about(self,"bildirim"," müşteri bilgileri güncellendi")
            self.load()

        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")

class customer_transaction(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
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
        self.load()
    def load(self):
        query="SELECT * from işlem_tablosu where islem_kaynak In  (select   hesap_id :: CHARACTER from müşteri_bilgisi_tablosu as b, müşteri_hesap_tablosu as h,temsilci_tablosu as te where h.müşteri_no=b.müsteri_no_tc and te.temsilci_id=b.temsilci_id and b.temsilci_id=%s ) ;"
        raw_data=DB.Query(DB,query,active_customer_agent_no) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
                
        query=" SELECT * from işlem_tablosu where islem_hedef In (select   hesap_id :: CHARACTER from müşteri_bilgisi_tablosu as b, müşteri_hesap_tablosu as h,temsilci_tablosu as te where h.müşteri_no=b.müsteri_no_tc and te.temsilci_id=b.temsilci_id and b.temsilci_id=%s ) "
        raw_data=DB.Query(DB,query,active_customer_agent_no) 
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
class customer_state_info(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
        table_headers=["Müşteri No","İsim Soyisim","Toplam Bakiye","Gelir","Gider"]
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton(" Müşteri  genel durum gör")
        self.load_button.clicked.connect(self.load)

   
        h_box.addWidget(self.load_button)
      
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()
    def load(self):
        query="SELECT  h.müşteri_no, isim_soyisim, sum(bakiye) FROM müşteri_bilgisi_tablosu as b ,müşteri_hesap_tablosu as h WHERE h.müşteri_no=b.müsteri_no_tc  and  temsilci_id=%s group by h.müşteri_no ,isim_soyisim;"
        
        #query="SELECT * from işlem_tablosu where islem_kaynak ::integer In (select  hesap_id from müşteri_bilgisi_tablosu as b, müşteri_hesap_tablosu as h,temsilci_tablosu as te where h.müşteri_no=b.müsteri_no_tc and te.temsilci_id=b.temsilci_id and b.temsilci_id=%s ) ;"
        raw_data=DB.Query(DB,query,active_customer_agent_no) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))



class customer_request_account_open(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
        table_headers=["Müşteri no","İsim Soyisim","Hesap türü","Talep No","kur_id"]
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("Talepleri  gör")
        self.load_button.clicked.connect(self.load)
        self.accept_button = QPushButton("ONAY")
        self.accept_button.clicked.connect(self.accepted)
        self.Not_accept_button = QPushButton("RED")
        self.Not_accept_button.clicked.connect(self.Notaccepted)

   
        h_box.addWidget(self.accept_button)
        h_box.addWidget(self.load_button)

        h_box.addWidget(self.Not_accept_button)  
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
    def load(self):
        global active_customer_agent_no
        query="SELECT distinct talep_eden_id, isim_soyisim, kur_ismi ,talep_id,k.kur_id FROM public.hesap_açma_talep_tablosu as h ,kurlar_tablosu as k,müşteri_bilgisi_tablosu as m where h.talep_eden_id = m.müsteri_no_tc  and k.kur_id = h.kur_id  and talep_edilen_id = %s and talep_durumu <> 1 and talep_durumu <> 2"
        raw_data=DB.Query(DB,query,str(active_customer_agent_no) )
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        


    def accepted(self):
        try:
            user_no= self.table.item(self.table.currentRow(),0).text()
            account_kind= self.table.item(self.table.currentRow(),4).text()
            request_no = self.table.item(self.table.currentRow(),3).text()
            
            query="UPDATE public.hesap_açma_talep_tablosu SET  talep_durumu=2 WHERE talep_id=%s;"
            DB.Query(DB,query,request_no )
            query="SELECT COUNT(hesap_id) FROM public.müşteri_hesap_tablosu;"
            amount=DB.Query(DB,query,None)
            a=amount[0][0]
            a=a+1
            query="INSERT INTO public.müşteri_hesap_tablosu (hesap_id, müşteri_no, hesap_türü, bakiye) VALUES (%s, %s, %s, %s);"
            DB.Query(DB,query,a,user_no,account_kind,0)
            QMessageBox.about(self,"bildirim"," Talep onaylandı")
            
            self.load()

        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")
   
    def Notaccepted(self):
        try:
            request_no = self.table.item(self.table.currentRow(),3).text()
            print(request_no)
            query="UPDATE public.hesap_açma_talep_tablosu SET  talep_durumu=1 WHERE talep_id=%s;"
            DB.Query(DB,query,request_no )
            QMessageBox.about(self,"bildirim"," Talep reddedildi")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")
            
class customer_request_account_delete(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
        table_headers=[" Müşteri no","İsim Soyisim","Silincek Hesap No","Talep No"]
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("Talepleri  gör")
        self.load_button.clicked.connect(self.load)
        self.accept_button = QPushButton("ONAY")
        self.accept_button.clicked.connect(self.accepted)
        self.Not_accept_button = QPushButton("RED")
        self.Not_accept_button.clicked.connect(self.Notaccepted)

   
        h_box.addWidget(self.accept_button)
        h_box.addWidget(self.load_button)

        h_box.addWidget(self.Not_accept_button)  
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()
        
    def load(self):
        global active_customer_agent_no
        query="SELECT distinct talep_eden_id, isim_soyisim,silinecek_hesap_no, talep_id FROM public.hesap_silme_talep_tablosu as h , müşteri_bilgisi_tablosu as m where h.talep_eden_id = m.müsteri_no_tc   and talep_edilen_id = %s and talep_durumu <> 1 and talep_durumu <> 2 "
        raw_data=DB.Query(DB,query,str(active_customer_agent_no) )
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        

    def accepted(self):
        try:
            request_no = self.table.item(self.table.currentRow(),3).text()
            account_no=self.table.item(self.table.currentRow(),2).text()

            print(request_no) 
            query="DELETE FROM public.hesap_silme_talep_tablosu  WHERE talep_id=%s ;"
            DB.Query(DB,query,request_no )
            
            query="DELETE FROM public.müşteri_hesap_tablosu WHERE hesap_id = %s AND bakiye =0 RETURNING * ;"
            raw_data=DB.Query(DB,query,account_no)
            if(raw_data == [] or raw_data==None  ):
                QMessageBox.about(self,"AttributeError","bakiye sıfır olamdığından silinmedi !")

            else:
                QMessageBox.about(self,"bildirim"," Talep onaylandı")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")
   
   
    def Notaccepted(self):
        try:
            request_no = self.table.item(self.table.currentRow(),3).text()
            print(request_no)
            query="UPDATE public.hesap_silme_talep_tablosu SET  talep_durumu=1 WHERE talep_id=%s;"
            DB.Query(DB,query,request_no )
            QMessageBox.about(self,"bildirim"," Talep reddedildi")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")

   


class customer_request_credit(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box=QHBoxLayout()
        table_headers=["Müşteri No","İsim Soyisim","Ana para","Vade Sayısı","Talep No"]
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        for col_number, col_data in enumerate(table_headers):
            self.table.setHorizontalHeaderItem(col_number,QTableWidgetItem(str(col_data)))

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_button = QPushButton("Talepleri  Gör")
        self.load_button.clicked.connect(self.load)
        self.accept_button = QPushButton("ONAY")
        self.accept_button.clicked.connect(self.accepted)
        self.Not_accept_button = QPushButton("RED")
        self.Not_accept_button.clicked.connect(self.Notaccepted)

   
        h_box.addWidget(self.accept_button)
        h_box.addWidget(self.load_button)

        h_box.addWidget(self.Not_accept_button)  
      
        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)
        self.load()
    def load(self):
        global active_customer_agent_no
        query="SELECT talep_eden_id ,isim_soyisim,ana_para,vade_sayısı,talep_id FROM public.kredi_talep_tablosu as k,public.müşteri_bilgisi_tablosu as m  where m.müsteri_no_tc=k.talep_eden_id  and talep_edilen_id=%s and talep_durumu <> 1 and talep_durumu <> 2;"
        raw_data=DB.Query(DB,query,str(active_customer_agent_no) )
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def accepted(self):
        try:
            request_no = self.table.item(self.table.currentRow(),4).text()
            customer_no = self.table.item(self.table.currentRow(),0).text()
            main_money = self.table.item(self.table.currentRow(),2).text()
            term_amount = self.table.item(self.table.currentRow(),3).text()
            
            #talebin onaylasması
            query="UPDATE public.kredi_talep_tablosu SET  talep_durumu=2 WHERE talep_id=%s;"
            DB.Query(DB,query,request_no )
            #faiz bilgileri alınması
            query= "SELECT * FROM public.faiz_tablosu ORDER BY faiz_id ASC "
            raw_data_2=DB.Query(DB,query,None) 
            #kredi_id alınması
            query= "SELECT COUNT(kredi_id) FROM public.kredi_tablosu "
            amount=DB.Query(DB,query,None)
            a=amount[0][0]
            a=a+1

            #kredi tablosuna bilgilerin girilmesi 
            self.credit_time=QDateTimeEdit(QDateTime.currentDateTime())
            query="INSERT INTO public.kredi_tablosu(kredi_id, kredi_sahibi_no, alınna_ana_para, faiz_oranı, gecikme_faiz_oranı, ödenen_ay,vade_sayısı,ödenen_ana_para,ödenen_faiz, gecikme_ayı, verilme_tarih) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            DB.Query(DB,query,a,customer_no,main_money,raw_data_2[0][2],raw_data_2[1][2],0,term_amount,0,0,0,self.credit_time.text())
            
            #kredinini hesaba aktarılması
            #hesap var mı?
            query="SELECT * FROM müşteri_hesap_tablosu WHERE  müşteri_no=%s AND  hesap_türü=0"
            raw_data_3=DB.Query(DB,query,customer_no)
            account_id=0
            new_balance=0
            if(raw_data_3 != [] and raw_data_3!=None and None!=raw_data_3[0][3] ):
                new_balance=float(raw_data_3[0][3])
                account_id=raw_data_3[0][0]
            
            #hesap yoksa
            if(raw_data_3 == [] or raw_data_3==None):
                
                query="SELECT COUNT ( hesap_id) FROM public.müşteri_hesap_tablosu;"
                amount=DB.Query(DB,query,None)
                a=amount[0][0]
                a=a+1
                account_id=a
                 
                query="INSERT INTO public.müşteri_hesap_tablosu(hesap_id,müşteri_no, hesap_türü, bakiye) VALUES (%s, %s, %s, %s);"
                raw_data_3=DB.Query(DB,query,a,customer_no,0,0)
                new_balance=0
                QMessageBox.about(self,"bildirim"," hesap açıldı")
            
            #parayı yatırma
            curent_balance=new_balance+float(main_money)
            
            query="UPDATE public.müşteri_hesap_tablosu SET  bakiye=%s WHERE hesap_id=%s "
            raw_data_3=DB.Query(DB,query,curent_balance,account_id)
                
            #işlem tablosuna ekleme
            query="SELECT COUNT(islem_no_id) FROM public.işlem_tablosu"
            p_key = DB.Query(DB,query)
            query = "INSERT INTO public.işlem_tablosu (islem_no_id, islem_kaynak, islem_hedef, işlem_çeşidi, tutar, kaynak_bakiye, hedef_bakiye, tarih) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            DB.Query(DB,query,p_key[0][0],'BANKA',account_id,'Kredi verme',main_money,0,new_balance,'2017-03-14')
            

            QMessageBox.about(self,"bildirim"," Talep onaylandı")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")
   
    def Notaccepted(self):
        try:
            request_no = self.table.item(self.table.currentRow(),4).text()
            print(request_no)
            query="UPDATE public.kredi_talep_tablosu SET  talep_durumu=1 WHERE talep_id=%s;"
            DB.Query(DB,query,request_no )
            QMessageBox.about(self,"bildirim"," Talep reddedildi")
            self.load()
        
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")
   


# aktif temsilci bilgileri 
global active_customer_agent_no
global active_customer_agent_name


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle(" Temsilci Giriş")
        f_box = QVBoxLayout(self)
        self.setMinimumSize(300,200)
        self.user =QLabel("kullanıcı no")
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
        global active_customer_agent_no

        user=self.user_i.text()
        password=self.password_i.text()
        
        query="SELECT * FROM public.temsilci_tablosu where temsilci_id=%s and şifre =%s "
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
"""
app = QApplication(sys.argv)
Win = MainWindow()
sys.exit(app.exec_())
"""