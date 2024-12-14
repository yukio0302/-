import streamlit as st
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pandas as pd

# 加盟店データをCSVから読み込む
def load_data():
    try:
        return pd.read_csv("加盟店_data.csv")
    except Exception as e:
        st.error(f"加盟店データの読み込み中にエラーが発生しました: {e}")
        return pd.DataFrame()

加盟店_data = load_data()

# OpenCage APIの設定
api_key = "d63325663fe34549885cd31798e50eb2"
geocoder = OpenCageGeocode(api_key)

st.image("kensakup_top.png", use_column_width=True)
st.image("kensakup_topmain.png", use_column_width=True)
st.image("to-kousikip.png", use_column_width=True)
st.image("kensakup_to-map.png", use_column_width=True)

st.write("郵便番号もしくは住所を入力して、10km圏内の加盟店を検索します。")

# 検索モード選択
search_mode = st.radio(
    "検索方法を選択してください：",
    ("住所で検索", "最寄り駅で検索"),
    key="search_mode",
)

# デフォルトの地図
m = folium.Map(location=[35.681236, 139.767125], zoom_start=5, tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png", attr='国土地理院')

if search_mode == "住所で検索":
    postal_code_input = st.text_input("郵便番号を入力してください（例: 123-4567）:")
    address_input = st.text_input("住所（番地・号を除く）を入力してください:")

    if postal_code_input or address_input:
        query = postal_code_input if postal_code_input else address_input
        results = geocoder.geocode(query=query, countrycode='JP', limit=1)

        if results:
            search_lat = results[0]['geometry']['lat']
            search_lon = results[0]['geometry']['lng']
            
            m = folium.Map(location=[search_lat, search_lon], zoom_start=15, tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png", attr='国土地理院')
            folium.Marker([search_lat, search_lon], popup=f"検索地点", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

            加盟店_data["distance"] = 加盟店_data.apply(
                lambda row: geodesic((search_lat, search_lon), (row['lat'], row['lon'])).km, axis=1
            )

            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

            if not nearby_stores.empty:
                bounds = []
                for _, store in nearby_stores.iterrows():
                    brand_html = "".join(
                        f'<span style="background-color: red; color: white; padding: 2px 4px; margin: 2px; display: inline-block;">{brand}</span>'
                        for brand in eval(store["銘柄"])
                    )
                    popup_content = f"""
                    <b>{store['name']}</b><br>
                    <a href="{store['url']}" target="_blank">加盟店詳細はこちら</a><br>
                    銘柄: {brand_html}<br>
                    距離: {store['distance']:.2f} km
                    """
                    folium.Marker(
                        [store["lat"], store["lon"]],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    bounds.append((store["lat"], store["lon"]))

                if bounds:
                    m.fit_bounds(bounds)

if search_mode == "最寄り駅で検索":
    prefecture_input = st.text_input("都道府県を入力してください（省略可）:")
    station_name = st.text_input("最寄り駅名を入力してください（「駅」は省略可能です）:")

    if station_name:
        search_query = station_name if "駅" in station_name else station_name + "駅"
        if prefecture_input:
            search_query = f"{prefecture_input} {search_query}"

        results = geocoder.geocode(query=search_query, countrycode="JP", limit=1)

        if results:
            search_lat = results[0]['geometry']['lat']
            search_lon = results[0]['geometry']['lng']
            
            m = folium.Map(location=[search_lat, search_lon], zoom_start=15, tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png", attr='国土地理院')
            folium.Marker([search_lat, search_lon], popup=f"{station_name}駅", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

            加盟店_data["distance"] = 加盟店_data.apply(
                lambda row: geodesic((search_lat, search_lon), (row['lat'], row['lon'])).km, axis=1
            )

            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

            if not nearby_stores.empty:
                bounds = []
                for _, store in nearby_stores.iterrows():
                    brand_html = "".join(
                        f'<span style="background-color: red; color: white; padding: 2px 4px; margin: 2px; display: inline-block;">{brand}</span>'
                        for brand in eval(store["銘柄"])
                    )
                    popup_content = f"""
                    <b>{store['name']}</b><br>
                    <a href="{store['url']}" target="_blank">加盟店詳細はこちら</a><br>
                    銘柄: {brand_html}<br>
                    距離: {store['distance']:.2f} km
                    """
                    folium.Marker(
                        [store["lat"], store["lon"]],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color="blue"),
                    ).add_to(m)
                    bounds.append((store["lat"], store["lon"]))

                if bounds:
                    m.fit_bounds(bounds)

st_folium(m, width=700, height=500)
