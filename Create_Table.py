import sys 
from PyQt5.QtWidgets import QApplication,  QPushButton, QLabel,QGridLayout, QHBoxLayout,QVBoxLayout,QWidget,QRadioButton,QFileDialog
from PyQt5.QtCore import Qt
import csv

class Exam(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        #프로그램 형태 만들기
        grid = QGridLayout()
        grid.addWidget(QLabel("Database Type :"),0,0) 
        grid.addWidget(QLabel("CSV Path:"),1,0)
        grid.addWidget(QLabel("Result Path :"),2,0)
        self.FILE = QLabel(" ")
        grid.addWidget(self.FILE,1,1)
        self.PATH = QLabel(" ")
        grid.addWidget(self.PATH,2,1)
        #입력 변수 생성
        self.result = QLabel("Default")
        self.oracle = QRadioButton("oracle")
        self.mariadb = QRadioButton("mariadb")
        self.FILE_BUTTON = QPushButton("테이블정의서 선택...")
        self.FILE_BUTTON.clicked.connect(self.FILE_SELECT)
        self.SEARCH_BUTTON = QPushButton("찾아보기...")
        self.SEARCH_BUTTON.clicked.connect(self.PATH_SELECT)
        #입력칸 배치
        typehbox = QHBoxLayout()
        typehbox.addWidget(self.oracle,0)
        typehbox.addWidget(self.mariadb,1)
        grid.addLayout(typehbox,0,1)
        grid.addWidget(self.FILE_BUTTON,1,2)
        grid.addWidget(self.SEARCH_BUTTON,2,2)

        #DB선택 라디오버튼
        self.oracle.toggled.connect(self.SELEFT_DBTYPE)
        self.mariadb.toggled.connect(self.SELEFT_DBTYPE)
        #생성,취소버튼
        CreateButton = QPushButton("생성")
        CancleButton = QPushButton("취소")
        CreateButton.clicked.connect(self.CreateTable)
        CancleButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(CreateButton)
        hbox.addWidget(CancleButton)


        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.result)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        
        self.setGeometry(400,400,500,150)
        self.setWindowTitle('JSON Maker')
        self.show()
    
        #결과저장폴더선택
    def PATH_SELECT(self):
        dirName = QFileDialog.getExistingDirectory(self,self.tr("Save Directory"),"./",QFileDialog.ShowDirsOnly)
        self.dirName = dirName#.replace('''/''','''\\''')
        self.PATH.setText(dirName)
        
        return dirName

        #테이블정의서선택
    def FILE_SELECT(self):
        fileName = QFileDialog.getOpenFileName(self,self.tr("Open File"),"C:/","File(*.csv)")
        self.fileName = fileName
        self.FILE.setText(fileName[0])
        return fileName
        
        #종료 함수
    def close(self):
        sys.exit()

    def oracle(self):
        f=open(self.fileName,'r',encoding='utf-8')
        rdr=csv.reader(f)
        list=[]
        for line in rdr:
            list.append(line)
        f.close

        table_list=[]
        #oracle
        for i in list:
            table_list.append(i[0])
        table_set=set(table_list)
        query_list=[]
        for j in table_set:
            text=[]
            pk_cnt = 0
            text.append("CREATE TABLE QUADMAX_BASE."+j+"(")
            for i in range(0,len(list)):
                if list[i][0]==j:
                    text.append(list[i][2]+" "+list[i][5]+"(")
                    if list[i][5] == 'NUMBER':
                        text.append(list[i][7]+","+list[i][8])
                    else:
                        text.append(list[i][6])
                    text.append(") ")
                    if list[i][10]=='N':
                        text.append("NOT NULL ")
                    if list[i][9]=='PK':
                        pk_cnt += 1
                    text.append(",")
                    comment=list[i][1]
            if pk_cnt != 0 :
                text.append("PRIMARY KEY (")
                for i in range(0,len(list)):
                    if list[i][0]==j and list[i][9]=="PK"  :
                        text.append(list[i][2])
                        text.append(",")
                text.pop(-1)
            text.append(") );")
            comment_text=[]
            comment_text.append("COMMENT ON TABLE "+j+" IS '"+comment+"';")
            for i in range(0,len(list)):
                if list[i][0]==j:
                    comment_text.append("COMMENT ON COLUMN "+j+"."+list[i][2]+" IS '"+list[i][3]+"';")
            query=''
            for k in text:
                query+=k
            for m in comment_text:
                query+=m
            query_list.append(query)
            
            with open(self.dirName + """\\{}.txt""".format(j),'w',encoding="UTF-8") as outfile:
                    f.write(query)

        return self.result.setText(str(len(query_list))+ '개의 CREATE 파일이 생성 되었습니다')

        #mariadb 테이블 생성문


    def SELEFT_DBTYPE(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.DB_TYPE = radioBtn.text()

    def CreateTable(self):
        f=open(self.fileName[0],'r',encoding='utf-8')
        rdr=csv.reader(f)
        list=[]
        for line in rdr:
            list.append(line)
        f.close
        if self.DB_TYPE == 'oracle':
            table_list=[]
            #oracle
            for i in list:
                table_list.append(i[0])
            table_set=set(table_list)
            query_list=[]
            for j in table_set:
                text=[]
                pk_cnt = 0
                text.append("CREATE TABLE QUADMAX_BASE."+j+"(")
                for i in range(0,len(list)):
                    if list[i][0]==j:
                        text.append(list[i][2]+" "+list[i][5]+"(")
                        if list[i][5] == 'NUMBER':
                            text.append(list[i][7]+","+list[i][8])
                        else:
                            text.append(list[i][6])
                        text.append(") ")
                        if list[i][10]=='N':
                            text.append("NOT NULL ")
                        if list[i][9]=='PK':
                            pk_cnt += 1
                        text.append(",")
                        comment=list[i][1]
                if pk_cnt != 0 :
                    text.append("PRIMARY KEY (")
                    for i in range(0,len(list)):
                        if list[i][0]==j and list[i][9]=="PK"  :
                            text.append(list[i][2])
                            text.append(",")
                    text.pop(-1)
                text.append(") );")
                comment_text=[]
                comment_text.append("COMMENT ON TABLE "+j+" IS '"+comment+"';")
                for i in range(0,len(list)):
                    if list[i][0]==j:
                        comment_text.append("COMMENT ON COLUMN "+j+"."+list[i][2]+" IS '"+list[i][3]+"';")
                query=''
                for k in text:
                    query+=k
                for m in comment_text:
                    query+=m
                query_list.append(query)
                
                with open(self.dirName + """/{}.txt""".format(j),'w',encoding="UTF-8") as f:
                        f.write(query)
            all_create=''
            for k in query_list:
                all_create+=k
            with open(self.dirName + """/{}.txt""".format('ALL'),'w',encoding="UTF-8") as f:
                f.write(all_create)
            return self.result.setText(str(len(query_list)+1)+ '개의 CREATE 파일이 생성 되었습니다')
            
        if self.DB_TYPE == 'mariadb':
                table_list=[]
                #mariadb
                for i in list:
                    table_list.append(i[0])
                table_set=set(table_list)
                query_list=[]
                for j in table_set:
                    text=[]
                    pk_cnt = 0
                    text.append("CREATE TABLE QUADMAX_BASE."+j+"(")
                    for i in range(0,len(list)):
                        if list[i][0]==j:
                            text.append(list[i][2]+" ")
                            if list[i][5] == 'NUMBER':
                                if list[i][8] != "0":
                                    text.append("DECIMAL("+list[i][7]+","+list[i][8]+")")
                                elif list[i][7]=="5":
                                    text.append("SMALLINT("+list[i][7]+")")
                                elif list[i][7]=="10":
                                    text.append("INT("+list[i][7]+")")
                                elif list[i][7]=="19":
                                    text.append("BIGINT("+list[i][7]+")")
                            elif list[i][5] == 'VARCHAR2':
                                text.append("VARCHAR("+list[i][6]+")")
                            elif list[i][5] == 'CLOB':
                                text.append("TEXT")
                            elif list[i][5] == 'DATE':
                                text.append("VARCHAR(14)")
                            else :
                                text.append(list[i][5]+"("+list[i][6]+")")
                            if list[i][10]=='N':
                                text.append(" NOT NULL ")
                            if list[i][9]=='PK':
                                pk_cnt += 1
                            if list[i][1]=='':
                                text.append(",")
                            else:
                                text.append(" COMMENT '"+list[i][3]+"',")
                            comment=list[i][1]
                    if pk_cnt != 0 :
                        text.append("PRIMARY KEY (")
                        for i in range(0,len(list)):
                            if list[i][0]==j and list[i][9]=="PK"  :
                                text.append(list[i][2])
                                text.append(",")
                        text.pop(-1)
                    text.append(")) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='"+comment+"';")
                    query=''
                    for k in text:
                        query+=k
                    query_list.append(query)
                    with open(self.dirName + """/{}.txt""".format(j),'w',encoding="UTF-8") as f:
                            f.write(query)
                all_create=''
                for k in query_list:
                    all_create+=k
                with open(self.dirName + """/{}.txt""".format('ALL'),'w',encoding="UTF-8") as f:
                    f.write(all_create)

                return self.result.setText(str(len(query_list)+1)+ '개의 CREATE 파일이 생성 되었습니다')


    def tglStat(self,state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def keyPressEvent(self, e) :
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Exam()
    sys.exit(app.exec_())
