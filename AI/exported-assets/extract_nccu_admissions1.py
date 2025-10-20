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

def parse_departments(text):
#    pattern = re.compile(r'(\d{4,5})\s*(.+?)(?=\d{4,5}\s|$)', re.DOTALL)
#      matches = pattern.findall(text)
    data = []
    for line in text.splitlines():
        if "代碼" in line and ("系" in line or "研究所" in line):
        # 此處插入前面提供的多欄資料提取程式
            code_match = re.search(r"代碼\s*(\d{4,5})", line)
            code = code_match.group(1) if code_match else ''
            dept_match = re.search(r"(?:系所別|系\s*別|所\s*別|學系|研究所)\s*([\u4e00-\u9fa5A-Za-z（）()]+)", line)
            dept = dept_match.group(1).replace(" ", "") if dept_match else ''
            quota_match = re.search(r"名額[：: ]?(\d+)", line)
            quota = quota_match.group(1) if quota_match else ''
            data.append({'代碼': code, '系所名稱': dept, '名額': quota, '英檢': '', '截止日期': '', '網址': ''})
    return pd.DataFrame(data)
# 3. 最後整理成 DataFrame
#    df = pd.DataFrame(data)
#    print(df.head())
#return pd.DataFrame(data)

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
    df = parse_departments(text)
    print(df.head())
    write_to_google_sheet(df)  # 可選擇是否匯出 Google Sheet
