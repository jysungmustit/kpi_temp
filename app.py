import streamlit as st
import pandas as pd
import json
from io import BytesIO

from parser.brand_catalog_parser import BrandCatalogParser
from parser.seller_catalog_parser import SellerCatalogParser
from sorter import Sorter

tab1, tab2 = st.tabs(['브랜드별 카탈로그 현황', '판매자별 카탈로그 현황'])
sorter = Sorter(st)


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def set_download_button(st, key):
    st.download_button(
        label="Download data as Excel",
        data=excel_data,
        file_name='data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key=key
    )


with tab1:
    uploaded_file = st.file_uploader("Choose a JSON file", type=["json"], key="brand_file_uploader")

    # 파일이 업로드되었는지 확인
    if uploaded_file is not None:
        # 파일 읽기
        data = json.load(uploaded_file)
        # st.write("Uploaded JSON:", data)  # JSON 데이터 표시 (원본데이터 확인 용도)

        parser = BrandCatalogParser(data)
        parsed_data = parser.parse()

        # 데이터프레임 생성
        df = pd.DataFrame(parsed_data)
        df = sorter.set_brand_catalog_sort(df)

        df["matching rate"] = df["matching rate"].apply(lambda x: f"{x:.1f}%")

        # 엑셀 파일 다운로드 버튼
        excel_data = to_excel(df)
        set_download_button(st, "brand_download_button")

        # 테이블 표시 (스크롤 없이 전체 표시)
        st.table(df)

with tab2:
    uploaded_file = st.file_uploader("Choose a JSON file", type=["json"], key="seller_file_uploader")

    # 파일이 업로드되었는지 확인
    if uploaded_file is not None:
        # 파일 읽기
        data = json.load(uploaded_file)

        parser = SellerCatalogParser(data)
        parsed_data = parser.parse()

        # 데이터프레임 생성
        df = pd.DataFrame(parsed_data)
        df = sorter.set_seller_catalog_sort(df)

        df["matching rate"] = df["matching rate"].apply(lambda x: f"{x:.1f}%")

        # 엑셀 파일 다운로드 버튼
        excel_data = to_excel(df)
        set_download_button(st, "seller_download_button")

        # 테이블 표시 (스크롤 없이 전체 표시)
        st.table(df)
