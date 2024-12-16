import streamlit as st
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pandas as pd
# カスタムCSS読込
from cycustom_css import custom_css
from cycustom_radio_css import custom_css as radio_custom_css 

# 画像読込
st.image("kensakup_top.png", use_column_width=True)
st.image("kensakup_topmain.png", use_column_width=True)
st.markdown("""
    <a href="https://www.meimonshu.jp/modules/xfsection/article.php?articleid=377" target="_blank" class="stLinkButton">
        立春朝搾り特設サイトはこちら
    </a>
    """, unsafe_allow_html=True)
st.image("kensakup_to-map.png", use_column_width=True)

# ここでカスタムCSSを適用
st.markdown(f"""
    <style>
    {custom_css}
    </style>
    """, unsafe_allow_html=True)

# 加盟店データを外部ファイルからインポート
from 加盟店_data import 加盟店_data

# MAP情報OpenCage APIの設定
api_key = "d63325663fe34549885cd31798e50eb2"
geocoder = OpenCageGeocode(api_key)

st.write("郵便番号もしくは住所を入力して、10km圏内の加盟店を検索します。")
# 検索モード選択
search_mode = st.radio(
    "検索方法を選択してください：",
    ("住所で検索", "最寄り駅で検索"),
    key="search_mode",
)

# ここでカスタムラジオボタンのCSSを適用
st.markdown(f"""
    <style>
    {radio_custom_css}
    </style>
    """, unsafe_allow_html=True)

# ナビタイムAPIの情報
NAVITIME_CID = "n2302880"
NAVITIME_API_KEY = "Kakvwq38mAwTjiA80BAKzTQbvaDTgUUs"
NAVITIME_TILE_URL = f"https://{NAVITIME_CID}.api-service.navitime.biz/map/v1/{NAVITIME_API_KEY}/{{z}}/{{x}}/{{y}}.png"

# デフォルトの地図
m = folium.Map(location=[35.681236, 139.767125], zoom_start=5, tiles=NAVITIME_TILE_URL, attr='ナビタイムAPI')

if search_mode == "住所で検索":
    postal_code_input = st.text_input("郵便番号を入力してください（例: 123-4567）:")
    address_input = st.text_input("住所（番地・号を除く）を入力してください:")

    if postal_code_input or address_input:
        query = postal_code_input if postal_code_input else address_input
        results = geocoder.geocode(query=query, countrycode='JP', limit=1)

        if results:
            search_lat = results[0]['geometry']['lat']
            search_lon = results[0]['geometry']['lng']

            m = folium.Map(location=[search_lat, search_lon], zoom_start=15, tiles=NAVITIME_TILE_URL, attr='ナビタイムAPI')
            folium.Marker([search_lat, search_lon], popup=f"検索地点", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

            加盟店_data["distance"] = 加盟店_data.apply(
                lambda row: geodesic((search_lat, search_lon), (row['lat'], row['lon'])).km, axis=1
            )
            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

if 'nearby_stores' in locals() and not nearby_stores.empty:
    all_brands = set(
        brand for brands in nearby_stores["銘柄"]
        if brands and brands != [""]
        for brand in brands
    )
    all_brands.add("すべての銘柄")
    selected_brand = st.selectbox("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

    if selected_brand:
        filtered_stores = nearby_stores if selected_brand == "すべての銘柄" else nearby_stores[nearby_stores["銘柄"].apply(lambda brands: selected_brand in brands)]
        if not filtered_stores.empty:
            bounds = []
            for _, store in filtered_stores.iterrows():
                brand_html = "".join(
                    f'<span style="background-color: red; color: white; padding: 2px 4px; margin: 2px;">{brand}</span>'
                    for brand in store["銘柄"]
                )
                popup_content = f"""
                <b>{store['name']}</b><br>
                <a href="{store['url']}" target="_blank">加盟店詳細はこちら</a><br>
                銘柄: {brand_html}<br>
                距離: {store['distance']:.2f} km
                """
                folium.Marker([store["lat"], store["lon"]], popup=folium.Popup(popup_content, max_width=300), icon=folium.Icon(color="blue")).add_to(m)
                bounds.append((store["lat"], store["lon"]))
            if bounds:
                m.fit_bounds(bounds)

if search_mode == "最寄り駅で検索":
    prefecture_input = st.text_input("都道府県を入力してください（省略可）:")
    station_name = st.text_input("最寄り駅名を入力してください（「駅」は省略可能です）:")

    if station_name:
        search_query = f"{prefecture_input} {station_name}駅" if prefecture_input else f"{station_name}駅"
        results = geocoder.geocode(query=search_query, countrycode="JP", limit=5)

        if results:
            selected_result = results[0] if len(results) == 1 else st.selectbox("選択してください：", results)
            search_lat = selected_result["geometry"]["lat"]
            search_lon = selected_result["geometry"]["lng"]

            m = folium.Map(location=[search_lat, search_lon], zoom_start=15, tiles=NAVITIME_TILE_URL, attr='ナビタイムAPI')
            folium.Marker([search_lat, search_lon], popup=f"{station_name}駅", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

            加盟店_data["distance"] = 加盟店_data.apply(lambda row: geodesic((search_lat, search_lon), (row["lat"], row["lon"])).km, axis=1)
            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

            all_brands = set(brand for brands in nearby_stores["銘柄"] for brand in brands) if not nearby_stores.empty else set()
            all_brands.add("すべての銘柄")
            selected_brand = st.selectbox("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

            if selected_brand:
                filtered_stores = nearby_stores if selected_brand == "すべての銘柄" else nearby_stores[nearby_stores["銘柄"].apply(lambda brands: selected_brand in brands)]
                if not filtered_stores.empty:
                    for _, store in filtered_stores.iterrows():
                        brand_html = "".join(f'<span style="background-color: red;">{brand}</span>' for brand in store["銘柄"])
                        popup_content = f"<b>{store['name']}</b><br><a href='{store['url']}' target='_blank'>加盟店詳細</a><br>銘柄: {brand_html}<br>距離: {store['distance']:.2f} km"
                        folium.Marker([store["lat"], store["lon"]], popup=folium.Popup(popup_content, max_width=300), icon=folium.Icon(color="blue")).add_to(m)

st_folium(m, width=700, height=500)
