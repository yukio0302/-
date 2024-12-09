import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd

# 加盟店データ
加盟店_data = pd.DataFrame({
    "name": ["(株)兼中 田中商店", "ｸﾜﾊﾗ食糧(株)", "酒のいろは - (有)鈴木商店", "Sample Store 1", "Sample Store 2"],
    "lat": [43.0909579, 43.1150863, 43.1096344, 43.095, 43.105],
    "lon": [141.3425112, 141.3401039, 141.3432736, 141.350, 141.345],
    "url": ["http://example.com/1", "http://example.com/2", "http://example.com/3", "http://example.com/4", "http://example.com/5"],
    "銘柄": ["野村自慢", "野村自慢", "八海山", "久保田", "八海山"]  # 各加盟店の取り扱い銘柄
})

# Streamlitアプリのタイトル
st.title("📍 日本各地の最寄り駅周辺の加盟店検索アプリ")
st.write("最寄り駅を入力するか、**現在地を取得**して10km圏内の加盟店を検索します。")

# === 1. 現在地取得のボタンと機能 ===
st.write("### 📍 **現在地の自動取得**")
if st.button("📍 現在地を取得"):
    # 現在地取得用のJavaScriptコンポーネント
    location = components.html("""
        <script>
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const streamlitData = {latitude: lat, longitude: lon};
                    const message = JSON.stringify(streamlitData);
                    window.parent.postMessage(message, "*");
                },
                (error) => {
                    alert("位置情報が取得できませんでした。ブラウザの権限を確認してください。");
                }
            );
        </script>
    """, height=0)

# === 2. 最寄り駅の検索 ===
st.write("### 🚉 **最寄り駅からの検索**")
station_name = st.text_input("最寄り駅名を入力してください（「駅」は省略可能です）:")

# === 3. 現在地の情報を受け取る ===
# 位置情報がJavaScriptから受け取られるように設定
if 'latitude' not in st.session_state:
    st.session_state['latitude'] = None
if 'longitude' not in st.session_state:
    st.session_state['longitude'] = None

# クエリパラメータから現在地の緯度・経度を取得
query_params = st.experimental_get_query_params()
if 'latitude' in query_params and 'longitude' in query_params:
    try:
        st.session_state['latitude'] = float(query_params['latitude'][0])
        st.session_state['longitude'] = float(query_params['longitude'][0])
        st.success(f"現在地の緯度: {st.session_state['latitude']}, 経度: {st.session_state['longitude']}")
    except ValueError:
        st.error("緯度と経度の形式が正しくありません。")

# === 4. 地図の表示 (駅検索 or 現在地) ===
if st.session_state['latitude'] and st.session_state['longitude']:
    search_lat = st.session_state['latitude']
    search_lon = st.session_state['longitude']
    m = folium.Map(location=[search_lat, search_lon], zoom_start=13)
    folium.Marker(
        [search_lat, search_lon],
        popup="現在地",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
else:
    m = folium.Map(location=[35.681236, 139.767125], zoom_start=5)  # 東京駅を初期表示

# 10km以内の加盟店を表示
if st.session_state['latitude'] and st.session_state['longitude']:
    加盟店_data["distance"] = 加盟店_data.apply(
        lambda row: geodesic((search_lat, search_lon), (row['lat'], row['lon'])).km, axis=1
    )
    nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

    if not nearby_stores.empty:
        for _, store in nearby_stores.iterrows():
            popup_html = f"""
            <div style="width: 200px;">
                <strong>{store['name']}</strong><br>
                距離: {store['distance']:.2f} km<br>
                取り扱い銘柄： 
                <span style="background-color: red; color: white; padding: 3px; border-radius: 3px;">
                    {store['銘柄']}
                </span><br>
                <a href="{store['url']}" target="_blank" style="color: blue; text-decoration: underline;">リンクはこちら</a>
            </div>
            """
            popup = folium.Popup(popup_html, max_width=200)
            folium.Marker(
                [store["lat"], store["lon"]],
                popup=popup,
                icon=folium.Icon(color="green")
            ).add_to(m)
    else:
        st.write("10km以内に加盟店はありません。")

# 地図を表示
st_folium(m, width=800, height=500)
