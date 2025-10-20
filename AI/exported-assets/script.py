import os, zipfile

# 建立專案資料夾
project_root = 'nccu_extractor'
os.makedirs(project_root, exist_ok=True)

# Python 腳本內容
script_content = '''import re, pdfplumber, pandas as pd
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
    pattern = re.compile(r'(\\d{4,5})\\s*(.+?)(?=\\d{4,5}\\s|$)', re.DOTALL)
    matches = pattern.findall(text)
    data = []
    for code, block in matches:
        dept = re.search(r'[\\u4e00-\\u9fa5A-Za-z\\s]+系所?', block)
        quota = re.search(r'名額[:： ]?(\\d+)', block)
        exams = re.findall(r'(TOEFL|IELTS|TOEIC|GRE|JLPT|TOPIK)', block)
        deadline = re.search(r'(\\d{3,4}[\\./－-]\\d{1,2}[\\./－-]\\d{1,2})', block)
        url = re.search(r'https?[:/\\.\\w-]+nccu\\.edu\\.tw', block)
        data.append({
            '代碼': code,
            '系所名稱': dept.group(0) if dept else '',
            '名額': quota.group(1) if quota else '',
            '英檢': ', '.join(set(exams)) if exams else '無',
            '截止日期': deadline.group(1) if deadline else '',
            '網址': url.group(0) if url else ''
        })
    return pd.DataFrame(data)

# ========== 3. 寫入 Google Sheet ==========

def write_to_google_sheet(df):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NCCU_Admission_Extracted").sheet1
    set_with_dataframe(sheet, df)
    print('已成功儲存到 Google Sheet!')

# ========== 主程式 ==========
if __name__ == '__main__':
    pdf_path = '115Shuo-Bo-Zhen-Shi-Jian-Zhang.pdf'  # 政大招生簡章 PDF 檔名
    text = extract_text(pdf_path)
    df = parse_departments(text)
    print(df.head())
    # write_to_google_sheet(df)  # 可選擇是否匯出 Google Sheet
'''

# 寫入檔案
with open(os.path.join(project_root, 'extract_nccu_admissions.py'), 'w', encoding='utf-8') as f:
    f.write(script_content)

# requirements.txt
reqs = '''pdfplumber
gspread
oauth2client
gspread-dataframe
pandas
'''
with open(os.path.join(project_root, 'requirements.txt'), 'w', encoding='utf-8') as f:
    f.write(reqs)

# 壓縮
zip_path = 'nccu_extractor.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(project_root):
        for file in files:
            path = os.path.join(root, file)
            zipf.write(path, os.path.relpath(path, project_root))

zip_path