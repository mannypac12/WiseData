import xlwings as xl

## 1. 퀀티와이즈에서 받은 엑셀 파일 내 모듈에 매크로 함수를 작성한 다음 매크로 확장자로 저장
## 2. 퀀티와이즈에 접속되어있는지 확인 후 해당 파이선을 돌림(cmd / python fileset.py)
## 3. 변수: 일자는 yyyymmdd 형식으로 입력
## 3. 변수: 일자는 yyyymmdd 형식으로 입력

## 현재 날짜까지: CPD [20181220]

## 해당 파이선 파일을 다른 곳에서 돌릴 수 있도록

### Sheet에 대한 Update 해줘야 함 -> Sheet에 대한 Macro 작성 완료

## 변수: Sheet명 / 바꿀 컬럼 / Date

class Fileset:

    """
    매크로지정 (해당 엑셀파일 모듈 내)
    Public Sub Refresh_NewButton()
        '시트명.버튼위치.Hyperlinks(1).Follow
        Sheets(시트명).Range("A1").Hyperlinks(1).Follow
    End Sub
    """    

    ## 파일경로 / ## 파일명
    def __init__(self, file, path="D:\WiseData\Data"):

        self.path=path
        self.file=file
        self.fullpath=f"""{path}\\{self.file}"""

    ## 파일 Open

    def file_open(self):
        
        wb=xl.Book(self.fullpath)
        return wb

    ## 변수 변경(날짜)

    def update(self, st_date, ed_date):

        wb = self.file_open()
        sheets = wb.sheets
        
        for sheet in sheets:
            sheets[sheet.name].range("B5").value = st_date
            sheets[sheet.name].range("B6").value = ed_date

        mac = wb.macro("Refresh_Button")
        mac()
        
        wb.save(self.fullpath)

a = Fileset("test.xlsm")
a.update(20170101, 20170110)


# class FileSet:



#     def __init__(self, path=f"""D:\WiseData\Data""", file_name="test.xlsm"):
        
#         self.path = path
#         self.file_name = file_name

#     def file_open(self, st_date, ed_date):
        
#         wb=xl.Book(f"{self.path}\\{self.file_name}")
#         # wb=xl.Book(f"{PATH}\\test.xlsm")
#         sht=wb.sheets['sheet1']
#         sht.range("B5").value = st_date
#         sht.range("B6").value = ed_date

#         mac = wb.macro("Refresh_NewButton")
#         mac()

#         wb.save(f"{self.path}\\{self.file_name}")
        
# a = FileSet()

# a.file_open(20150101,20180130)
# # PATH = f"""D:\WiseData\Data"""


# ## Start Date / End Date 는 추후에 만지는 걸로

# # print(sht.range("A1").value)