import streamlit as st
import pandas as pd
import json

tab1, tab2= st.tabs(['Tab A' , 'Tab B'])


def validate_json(data):
  # JSON 형식 검증
  for item in data:
    if not all(key in item for key in ["key", "doc_count", "catalog_count"]) or \
            not isinstance(item["catalog_count"], dict) or \
            "value" not in item["catalog_count"]:
      return False
  return True

with tab1:
  #tab A 를 누르면 표시될 내용
  uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])

  # 파일이 업로드되었는지 확인
  if uploaded_file is not None:
    try:
      # 파일 읽기
      data = json.load(uploaded_file)

      # JSON 형식 검증
      if not validate_json(data):
        st.error("Input only brand catalog json file")
      else:
        # 데이터 파싱
        parsed_data = []
        for item in data:
          total_count = item["doc_count"]
          catalog_count = item["catalog_count"]["value"]
          matching_rate = (catalog_count / total_count) * 100 if total_count != 0 else 0

          parsed_data.append({
            "brand": item["key"],
            "total count": total_count,
            "catalog count": catalog_count,
            "matching rate": matching_rate  # 매칭 비율 추가
          })

        # 데이터프레임 생성
        df = pd.DataFrame(parsed_data)

        # 정렬 옵션 선택
        sort_option = st.selectbox(
          "정렬 기준을 선택하세요",
          ("brand", "total count", "matching rate")
        )

        # 선택한 정렬 기준으로 데이터 정렬
        if sort_option == "brand":
          df = df.sort_values(by="brand")
        elif sort_option == "total count":
          df = df.sort_values(by="total count", ascending=False)
        elif sort_option == "matching rate":
          df = df.sort_values(by=["matching rate", "total count"], ascending=[False, False])

        # 매칭 비율을 퍼센트 형식으로 표시
        df["matching rate"] = df["matching rate"].apply(lambda x: f"{x:.2f}%")

        # 테이블 표시 (스크롤 없이 전체 표시)
        st.table(df)
    except json.JSONDecodeError:
      st.error("Input only brand catalog json file")

  else:
    st.write("Please upload a JSON file.")

with tab2:
  st.write('TBD')