from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem
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

        customer_request_account=QAction("müşteri hesap talepleri",self)
        customer_request_credit=QAction("müşteri kredi talepleri",self)

        customer_request.addActions([customer_request_account,customer_request_credit])
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
            self.open.new_tab(add_exchange_rate(),tabtitle)
        elif action.text() == "müşteri hesap talepleri":
            tabtitle = action.text() 
            self.open.new_tab(add_exchange_rate(),tabtitle)
        elif action.text() == "sistemi ilerletme":
            tabtitle = action.text() 
            self.open.new_tab(add_exchange_rate(),tabtitle)
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
        user_No = self.user_no_i.text()
        name= self.user_name_i.text()
        password = self.user_pass_i.text()
        phone = self.user_phone_i.text()
        mail = self.user_mail_i.text()
        address=self.user_address_i.text()
        query="INSERT INTO public.müşteri_bilgisi_tablosu (müsteri_no_tc, isim_soyisim, şifre, telefon_no, e_posta, adres) VALUES (%s,%s, %s, %s,%s, %s);"
        DB.Query(DB,query,user_No,name,password,phone,mail,address) 

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
        query="SELECT * FROM  public.müşteri_bilgisi_tablosu"
        raw_data=DB.Query(DB,query,None) 
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