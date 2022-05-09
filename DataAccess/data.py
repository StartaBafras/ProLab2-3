
import sys
import psycopg2
from psycopg2 import Error


hostname='localhost'
database='demo'
username='postgres'
pass1='242526'
port_id=5432


class DB:
    def __init__(self):
        self.connection : psycopg2.connection 

    #baglantı açma fonksiyonu    
    def DBconnect(self):
        try:
            self.connection=psycopg2.connect(dbname=database,
                                    user=username,
                                    password =pass1,
                                    host=hostname,
                                    port= port_id )     
        except (Exception,Error) as error:
            print("PostgreSQL bağlanırken hata oluştu:", error)
        print("bağlandı")
        return self.connection


    #baglantı kapama  fonksiyonu    
    def closeDBconnect(self):
        try:
            self.connection.close()
        except (Exception,Error) as error:
            print("PostgreSQL bağlantısı kapanmadı",error)

        print("PostgreSQL bağlantısı kapandı")   



    def Query(self,query:str,*info):
      
        try:
            self.connection=self.DBconnect(self)
            cursor=self.connection.cursor()
            cursor.execute(query,info)
        except (Exception,Error) as error:
            print("sorgu hatası",error)
        try:
            record=cursor.fetchall()
            
        except (Exception,Error) as error:
            record=self.connection.commit()#neY ?
        self.closeDBconnect(self)

        return record   
    
    