import streamlit as st
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pandas as pd

# 加盟店データを準備する（ここでは仮のデータを指定）
加盟店_data = pd.DataFrame({
    "name": ["浅野日本酒店"],  # 店名
    "lat": [34.70286004882703],       # 緯度（大阪市北区の適当な座標）
    "lon": [135.50515146931434],      # 経度（大阪市北区の適当な座標）
    "url": ["TEL 06-6585-0963"]  # その他の情報（TELなど）
})

# OpenCage APIの設定
api_key = "d63325663fe34549885cd31798e50eb2"  # OpenCageで取得したAPIキーを設定
geocoder = OpenCageGeocode(api_key)

# Streamlitアプリの設定
st.title("日本各地の最寄り駅周辺の加盟店検索アプリ")
st.write("最寄り駅を入力して、10km圏内の加盟店を検索します。")

# 最寄り駅の入力フォーム
station_name = st.text_input("最寄り駅名を入力してください（「駅」は省略可能です）:")

# 駅名に「駅」を付加して検索
if station_name:
    search_query = station_name if "駅" in station_name else station_name + "駅"
    result = geocoder.geocode(query=search_query, countrycode='JP', limit=5)
    
    if result:
        # 候補が複数ある場合、リストを表示して選択
        if len(result) > 1:
            options = {f"{loc['formatted']}": loc for loc in result}
            selected_address = st.selectbox("もしかして以下の駅ですか？", list(options.keys()))
            selected_location = options[selected_address]
        else:
            selected_location = result[0]
        
        # 選択された駅の緯度・経度を取得
        search_lat = selected_location['geometry']['lat']
        search_lon = selected_location['geometry']['lng']
        m = folium.Map(location=[search_lat, search_lon], zoom_start=13)
        
        # 検索した駅の位置にマーカーを追加
        folium.Marker(
            [search_lat, search_lon],
            popup=f"{station_name}駅",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

        # 加盟店データから10km圏内の店舗をフィルタリング
        stores_in_range = 0
        for _, store in 加盟店_data.iterrows():
            store_location = (store["lat"], store["lon"])
            distance = geodesic((search_lat, search_lon), store_location).km
            if distance <= 10:
                stores_in_range += 1
                folium.Marker(
                    store_location,
                    popup=f"<a href='#{store['url']}' target='_blank'>{store['name']}</a>",
                    icon=folium.Icon(color="green")
                ).add_to(m)

        # 10km圏内に加盟店がない場合のメッセージ
        if stores_in_range == 0:
            st.write(f"{station_name}駅周辺10km以内に加盟店はありません。")
    else:
        st.error("指定した駅が見つかりませんでした。再度試してください。")
        # 駅が見つからなかった場合の初期地図
        m = folium.Map(location=[35.681236, 139.767125], zoom_start=5)  # 初期地図の中心（東京駅）
else:
    # 駅が入力されていない場合の初期地図
    m = folium.Map(location=[35.681236, 139.767125], zoom_start=5)  # 初期地図の中心（東京駅）

# 地図を表示
st_folium(m, width=700, height=500)
