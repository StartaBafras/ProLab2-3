from cgi import print_arguments, print_form
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
class credit_requst_user(QWidget):
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

        main_money = self.main_money_i.text()
        term = self.credit_term_i.text()
        query="INSERT INTO public.kredi_talep_tablosu talep_id, talep_eden_id, talep_edilen_id, ana_para, vade_sayısı, talep_durumu)VALUES (?, ?, ?, ?, ?, ?);"
        raw_data=DB.Query(DB,query,None,None,2,main_money,query,0) 

       
        print(main_money,term)
        QMessageBox.about(self,"bildirim","talep alındı")
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
        query="SELECT * FROM public.İşlem_tablosu ;"
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
        cur_kind_id= self.combo_kind.currentIndex()
        print(cur_kind_id)     
        QMessageBox.about(self,"bildirim","talep alındı") 



class update_user_info(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        self.cur_user_no="2020"
        query="SELECT* FROM public.müşteri_bilgisi_tablosu WHERE müsteri_no_tc = %s;"
        self.raw_data=DB.Query(DB,query,self.cur_user_no)
        print(self.raw_data)

        self.user_no = QLabel("müşteri no/TÇ no")
        self.user_no_i = QLineEdit(str(self.raw_data[0][0]))
        
        
        self.user_name = QLabel("isim soyisim")
        self.user_name_i = QLineEdit(str(self.raw_data[0][1]))
      

        self.user_pass = QLabel("Şifre")
        self.user_pass_i = QLineEdit(str(self.raw_data[0][2]))
       

        self.user_phone = QLabel("telefon no")
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
        DB.Query(DB,query,user_No,name,password,phone,mail,address,self.cur_user_no) 

        QMessageBox.about(self,"bildirim","Bilgileriniz güncellendi")
class money_withdraw_deposit(QWidget):
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
        query="SELECT * FROM public.İşlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def pull(self):
        print("çekildi")
        QMessageBox.about(self,"bildirim","Para"+ "çekildi")
    def push(self):
        print( "yattı")
        QMessageBox.about(self,"bildirim","Para "+"yatırıldı")

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
        self.push_button = QPushButton("borçu yatır ")
        self.push_button.clicked.connect(self.push)

        h_box.addWidget(self.push_button)
    
      
        f_box.addWidget(self.table)
        f_box.addWidget(self.amount_money)
        f_box.addWidget(self.amount_money_i)
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

    def push(self):
        print( "yattı")
        QMessageBox.about(self,"bildirim","Borç ödemesi yapıldı")


class money_transfer(QWidget):
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

        self.target_account = QLabel("hedef hesap no ")
        self.target_account_i = QLineEdit()
        self.amount_= QLabel("")
        

        self.amount_money = QLabel("TUTAR :")
        self.amount_money_i = QLineEdit("0")
        self.push_button = QPushButton("Taranfer yap ")
        self.push_button.clicked.connect(self.push)

        h_box.addWidget(self.push_button)
    
      
        f_box.addWidget(self.table)
        f_box.addWidget(self.target_account)
        f_box.addWidget(self.target_account_i)
        f_box.addWidget(self.amount_money)
        f_box.addWidget(self.amount_money_i)
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
        query="SELECT * FROM public.İşlem_tablosu ;"
        raw_data=DB.Query(DB,query,None) 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))



class delete_user_account(QWidget):
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
        self.delete_button = QPushButton("Hesabı Sil")
        self.delete_button.clicked.connect(self.delete)


        f_box.addWidget(self.table)
        f_box.addWidget(self.delete_button)

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
    def delete(self):
        QMessageBox.about(self,"bildirim","Hesap silme talebi alındı")


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

        user=self.user_i.text()
        password=self.password_i.text()
        
        query="SELECT * FROM public.müşteri_bilgisi_tablosu where müsteri_no_tc=%s and şifre =%s "
        result=DB.Query(DB,query,user,password)
        active_user_no=result[0][0]
        active_user_name=result[0][1]
        active_user_agent_no=result[0][6]
        print(result,active_user_no,active_user_name,active_user_agent_no)
        if(result == [] or result==None):
            QMessageBox.warning(
                self, 'Error', 'müşteri no veya şifre yanlış')
        else:
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
sys.exit(app.exec_())"""