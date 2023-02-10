import sys 
from PyQt5.QtWidgets import QApplication,  QPushButton, QLabel,QGridLayout, QHBoxLayout,QVBoxLayout,QWidget,QRadioButton,QFileDialog
from PyQt5.QtCore import Qt
import pandas as pd

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

    #라디오버튼 선택값 변수화
    def SELEFT_DBTYPE(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.DB_TYPE = radioBtn.text()

    #DDL 생성함수
    def CreateTable(self):
        #CSV파일읽어오기
        df=pd.read_csv("C:/Users/easycore/Downloads/insert_define.csv",encoding='utf8')
        #오라클
        if self.DB_TYPE == 'oracle':
            table_list=[]
            for i in df.A_TABLE_NAME:
                table_list.append(i)
            table_set=set(table_list)
            query_list=[]
            for j in table_set:
                text=[]
                pk_cnt=0
                temp_df=df.loc[df['A_TABLE_NAME']==j]
                text.append("CREATE TABLE QUADMAX_BASE."+j+"(")
                for i in range(0,len(temp_df)):
                    text.append(temp_df.iloc[i]['A_COLUMN_NAME'])
                    text.append(" ")
                    text.append(temp_df.iloc[i]['A_DATA_TYPE']+"(")
                    if temp_df.iloc[i]['A_DATA_TYPE'] == 'NUMBER':
                        text.append(int(temp_df.iloc[i]['A_DATA_PRECISION']))
                        text.append(",")
                        text.append(int(temp_df.iloc[i]['A_DATA_SCALE']))
                    else:
                        text.append(temp_df.iloc[i]['A_DATA_LENGTH'])
                    text.append(") ")
                    if temp_df.iloc[i]['NULLABLE']=='N':
                        text.append("NOT NULL ")
                    if temp_df.iloc[i]['비고3(PK구분)']=='PK':
                        pk_cnt +=1
                        text.append(",")
                        comment=temp_df.iloc[i]['A_TABLE_COMMENTS']
                if pk_cnt != 0 :
                    text.append("PRIMARY KEY (")
                for i in range(0,len(temp_df)):
                    if temp_df.iloc[i]['A_TABLE_NAME']==j and temp_df.iloc[i]['비고3(PK구분)']=="PK":
                        text.append(temp_df.iloc[i]['A_COLUMN_NAME'])
                        text.append(",")
                text.pop(-1)
                text.append(") );")
                comment_text=[]
                comment_text.append("COMMENT ON TABLE "+j+"IS '"+comment+"';")
                for i in range(0,len(temp_df)):
                    if temp_df.iloc[i]['A_TABLE_NAME']==j:
                        comment_text.append("COMMENT ON COLUMN "+j+"."+temp_df.iloc[i]["A_COLUMN_NAME"]+" IS '")
                        comment_text.append(str(temp_df.iloc[i]["A_COLUMN_COMMENTS"])+"';")
                query=''
                for k in text:
                    query += str(k)
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
        #마리아디비
        if self.DB_TYPE == 'mariadb':
            table_list=[]
            for i in df.A_TABLE_NAME:
                table_list.append(i)
            table_set=set(table_list)
            query_list=[]
            for j in table_set:
                text=[]
                pk_cnt=0
                temp_df=df.loc[df['A_TABLE_NAME']==j]
                text.append("CREATE TABLE QUADMAX_BASE."+j+"(")
                for i in range(0,len(temp_df)):
                    text.append(temp_df.iloc[i]['A_COLUMN_NAME'])
                    text.append(" ")
                    if temp_df.iloc[i]['A_DATA_TYPE'] == 'NUMBER':
                        if temp_df.iloc[i]['A_DATA_SCALE']!= 0:
                            text.append("DECIMAL(")
                            text.append(int(temp_df.iloc[i]['A_DATA_PRECISION']))
                            text.append(",")
                            text.append(int(temp_df.iloc[i]['A_DATA_SCALE']))
                            text.append(") ")
                        elif temp_df.iloc[i]['A_DATA_PRECISION']== 5:
                            text.append("SMALLINT(")
                            text.append(int(temp_df.iloc[i]['A_DATA_PRECISION']))
                            text.append(") ")
                        elif temp_df.iloc[i]['A_DATA_PRECISION']== 10:
                            text.append("INT(")
                            text.append(int(temp_df.iloc[i]['A_DATA_PRECISION']))
                            text.append(") ")
                        elif temp_df.iloc[i]['A_DATA_PRECISION']== 19:
                            text.append("BIGINT(")
                            text.append(int(temp_df.iloc[i]['A_DATA_PRECISION']))
                            text.append(") ")
                    elif temp_df.iloc[i]['A_DATA_TYPE'] == 'VARCHAR2':
                        text.append("VARCHAR(")
                        text.append(temp_df.iloc[i]['A_DATA_LENGTH'])
                        text.append(") ")
                    elif temp_df.iloc[i]['A_DATA_TYPE'] == 'CLOB':
                        text.append("TEXT")
                    elif temp_df.iloc[i]['A_DATA_TYPE'] == 'DATE':
                        text.append("VARCHAR(14)")
                    else:
                        text.append(temp_df.iloc[i]['A_DATA_TYPE'])
                        text.append("(")
                        text.append(temp_df.iloc[i]["A_DATA_LENGTH"])
                        text.append(") ")
                    if temp_df.iloc[i]['NULLABLE']=='N':
                        text.append("NOT NULL ")
                    if temp_df.iloc[i]['비고3(PK구분)']=='PK':
                        pk_cnt +=1
                    if temp_df.iloc[i]['A_COLUMN_COMMENTS']=='':
                        text.append(",")
                    else:
                        text.append(" COMMENT '")
                        text.append(temp_df.iloc[i]['A_COLUMN_COMMENTS'])
                        text.append("',")
                    comment=temp_df.iloc[i]['A_TABLE_COMMENTS']
                if pk_cnt != 0 :
                    text.append("PRIMARY KEY (")
                for i in range(0,len(temp_df)):
                    if temp_df.iloc[i]['비고3(PK구분)']=="PK":
                        text.append(temp_df.iloc[i]['A_COLUMN_NAME'])
                        text.append(",")
                text.pop(-1)
                text.append(")) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='")
                text.append(comment)
                text.append("';")
                query=''
                for k in text:
                    query += str(k)
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
