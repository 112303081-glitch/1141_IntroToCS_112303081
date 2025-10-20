import pdfplumber
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

def extract_tables(pdf_path):
    all_rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    all_rows.append(row)
    # 轉成 DataFrame，欄位可稍後清洗
    df = pd.DataFrame(all_rows)
    return df

def clean_dataframe(df):
    # 根據簡章格式，清理標題行和空行
    # 範例：第一欄有「代碼」字可判斷為標題行，可丟掉
    df = df.dropna(how='all')  # 去除全空行
    df.columns = df.iloc[0]    # 將第一列當作標題
    df = df[1:]               # 去除表頭列
    df = df.reset_index(drop=True)
    # 你也可以做欄位重命名、去除多餘空白等預處理
    return df

def write_to_google_sheet(df, spreadsheet_id):
    scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1
    set_with_dataframe(sheet, df)
    print('已成功儲存到 Google Sheet!')

if __name__ == '__main__':
    pdf_path = '115Shuo-Bo-Zhen-Shi-Jian-Zhang.pdf'
    df_raw = extract_tables(pdf_path)
    df_cleaned = clean_dataframe(df_raw)
    print(df_cleaned.head())
    spreadsheet_id = "1hX7PF4wanBXFgmqH2w2vVQrI5bvWs-YrpVZNYNPkvcw"
    write_to_google_sheet(df_cleaned, spreadsheet_id)

