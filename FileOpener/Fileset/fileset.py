import xlwings as xl
import pandas as pd
## 1. 퀀티와이즈에서 받은 엑셀 파일 내 모듈에 매크로 함수를 작성한 다음 매크로 확장자로 저장
## 2. 퀀티와이즈에 접속되어있는지 확인 후 해당 파이선을 돌림(cmd / python fileset.py)
## 3. 변수: 일자는 yyyymmdd 형식으로 입력
## 3. 변수: 일자는 yyyymmdd 형식으로 입력

## 현재 날짜까지: CPD [20181220]

## 해당 파이선 파일을 다른 곳에서 돌릴 수 있도록

### Sheet에 대한 Update 해줘야 함 -> Sheet에 대한 Macro 작성 완료

## 변수: Sheet명 / 바꿀 컬럼 / Date

"""
파일 업뎃 시 Date 변수 뿐만 아니라

다른 것도 고려

Cross-Sectional Data / Time Series Data

파일 타입에 따라(코드, 산업분류등)에 따라 조금씩 달라지겠구냥
"""


class Fileset:

    """
    매크로지정 (해당 엑셀파일 모듈 내)
    Public Sub Refresh_NewButton()
        '시트명.버튼위치.Hyperlinks(1).Follow
        Sheets(시트명).Range("A1").Hyperlinks(1).Follow
    End Sub
    """    

    def mkt_date_selector(st_date, ed_date):

        ## 12월 1일부터 3월 1일까지
        ## 3월 1일보다 작은 것

        date_as = pd.date_range(st_date, ed_date)

        return date_as[date_as < ed_date][0], date_as[date_as < ed_date][-1]

    ## 파일경로 / ## 파일명

    def __init__(self, file, path="Data"):

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

