
class Sorter:
    def __init__(self, st):
        self.st = st

    def set_brand_catalog_sort(self, df):
        # 정렬 옵션 선택
        sort_option = self.st.selectbox(
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
        return df

    def set_seller_catalog_sort(self, df):
        # 정렬 옵션 선택
        sort_option = self.st.selectbox(
            "정렬 기준을 선택하세요",
            ("seller", "total count", "matching rate")
        )

        # 선택한 정렬 기준으로 데이터 정렬
        if sort_option == "seller":
            df = df.sort_values(by="seller")
        elif sort_option == "total count":
            df = df.sort_values(by="total count", ascending=False)
        elif sort_option == "matching rate":
            df = df.sort_values(by=["matching rate", "total count"], ascending=[False, False])
        return df
