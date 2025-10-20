import pdfplumber
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

def extract_nccu_admissions(pdf_path):
    all_rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    all_rows.append(row)
    df = pd.DataFrame(all_rows)
    # 假定pdf表格第1行是欄名
    df.columns = df.iloc[0]            # 第一行設為欄名
    df = df[1:].reset_index(drop=True)
    print(df.columns.tolist())
    print(df.head(10))


    # 映射你的標準欄位，根據 PDF 實際欄名調整
    result = pd.DataFrame({
        'university': 'National Chengchi University',
        'department': df['系 所 別'].str.strip(),
        'programname': '',                              # 若有學程/學位欄則填入
        'deadlinedate': '',                             # 無則空或視來源補
        'docdeadlinedate': '',
        'quota': df['招生名額'].astype(str).str.replace('名', '').str.strip(),
        'docsrequired': '',
        'eng required': '',
        'info': ''
    })
    return result

def write_to_google_sheet(df, spreadsheet_id):
    scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1
    set_with_dataframe(sheet, df)
    print('已成功儲存到 Google Sheet!')

if __name__ == '__main__':
    pdf_path = '115Shuo-Bo-Zhen-Shi-Jian-Zhang.pdf'
    spreadsheet_id = "1hX7PF4wanBXFgmqH2w2vVQrI5bvWs-YrpVZNYNPkvcw"   # 填入你的 Google Sheet ID
    admissions_df = extract_nccu_admissions(pdf_path)
    print(admissions_df.head())
    write_to_google_sheet(admissions_df, spreadsheet_id)

