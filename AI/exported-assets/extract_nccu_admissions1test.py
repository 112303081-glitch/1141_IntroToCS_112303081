import re, pdfplumber, pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

# ========== 1. 從政大招生簡章擷取文字 ==========

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(p.extract_text() for p in pdf.pages if p.extract_text())
    return text

# ========== 2. 正則抽取系所資訊 ==========

def preprocess_line(line):
    line = line.replace('\u3000', ' ')  # 全形空格轉半形空格
    line = re.sub(r'\s+', ' ', line)    # 多空白合併為一個
    return line.strip()

def parse_departments(text):
    lines = [preprocess_line(l) for l in text.splitlines() if l.strip()]
    data = []

    for i, line in enumerate(lines):
        # 簡化判斷條件，只看是否含有系、所字與代碼字
        if (re.search(r'系|所', line) and '代碼' in line):
            code_match = re.search(r"代碼\s*(\d{4,5})", line)
            dept_match = re.search(r"(系所別|學系|研究所|學程)?\s*([\u4e00-\u9fa5A-Za-z（）()]+)", line)
            quota_match = re.search(r"名額[：: ]?(\d+)", line)
            code = code_match.group(1) if code_match else ''
            dept = dept_match.group(2).replace(" ", "") if dept_match else ''
            quota = quota_match.group(1) if quota_match else ''
            data.append({
                '代碼': code,
                '系所名稱': dept,
                '名額': quota,
                '英檢': '',
                '截止日期': '',
                '網址': ''
            })

    return pd.DataFrame(data)

# ========== 3. 寫入 Google Sheet ==========

def write_to_google_sheet(df):
    #scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    scope =["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    # 加入以下列印你可訪問的試算表清單：
    client = gspread.authorize(creds)
    files = client.list_spreadsheet_files()
    print("可訪問的試算表：")
    for f in files:
        print(f['name'], f['id'])

    spreadsheet_id = "1hX7PF4wanBXFgmqH2w2vVQrI5bvWs-YrpVZNYNPkvcw"  # 從 Google Sheets 網址複製
    sheet = client.open_by_key(spreadsheet_id).sheet1
    set_with_dataframe(sheet, df)
    print('已成功儲存到 Google Sheet!')

# ========== 主程式 ==========
if __name__ == '__main__':
    pdf_path = '115Shuo-Bo-Zhen-Shi-Jian-Zhang.pdf'  # 政大招生簡章 PDF 檔名
    text = extract_text(pdf_path)

    # 印顯示前 30 行方便檢視格式
    for i, line in enumerate(text.splitlines()):
        if i >= 30:
            break
        print(repr(line))

    df = parse_departments(text)
    print(df.head())
    write_to_google_sheet(df)
