import streamlit as st
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pandas as pd
import streamlit as st
# カスタムCSS読込
from cycustom_css import custom_css
from cycustom_radio_css import custom_css as radio_custom_css 

# JavaScriptとCSSで最下部右側のリンクを非表示にする
hide_streamlit_style = """
            <style>
            /* ヘッダーとフッターのスタイル */
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            <script>
                // ページがロードされた後に最下部のリンクを非表示にする
                window.onload = function() {
                    var footerLinks = document.querySelectorAll('.css-1m5hb7j, .css-1n76uvr');
                    footerLinks.forEach(function(link) {
                        link.style.display = 'none';
                    });
                };
            </script>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 画像読込
st.image("kensakup_top.png", use_column_width=True)
st.image("kensakup_topmain.png", use_column_width=True)
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
    key="search_mode",  # ラジオボタンの選択肢を管理するキー
)

# ここでカスタムラジオボタンのCSSを適用
st.markdown(f"""
    <style>
    {radio_custom_css }
    </style>
    """, unsafe_allow_html=True)

# デフォルトの地図
m = folium.Map(location=[35.681236, 139.767125], zoom_start=5, tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png", attr='国土地理院')

if search_mode == "住所で検索":
    postal_code_input = st.text_input("郵便番号を入力してください（例: 123-4567）:")
    address_input = st.text_input("住所（番地・号を除く）を入力してください:")

    # 検索処理
    if postal_code_input or address_input:
        if postal_code_input:
            # 郵便番号で検索
            query = postal_code_input
        else:
            # 住所で検索
            query = address_input

        results = geocoder.geocode(query=query, countrycode='JP', limit=1)

        if results:
            # 検索地点の座標を取得
            search_lat = results[0]['geometry']['lat']
            search_lon = results[0]['geometry']['lng']

            # 地図の初期化
            m = folium.Map(location=[search_lat, search_lon], zoom_start=15, tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png", attr='国土地理院')
            folium.Marker([search_lat, search_lon], popup=f"検索地点", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

            # 加盟店データとの距離計算
            加盟店_data["distance"] = 加盟店_data.apply(
                lambda row: geodesic((search_lat, search_lon), (row['lat'], row['lon'])).km, axis=1
            )
            # 10km以内の加盟店をフィルタリング
            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

  # 検索エリアの取り扱い銘柄一覧を表示
if 'nearby_stores' in locals() and not nearby_stores.empty:  # nearby_stores が定義されていて、空でない場合
    if "銘柄" in nearby_stores.columns:
        all_brands = set(
            brand for brands in nearby_stores["銘柄"]
            if brands and brands != [""]  # 空リストまたは取り扱い銘柄なしの処理
            for brand in brands
        )
    else:
        all_brands = set()
    all_brands.add("すべての銘柄")

    selected_brand = st.selectbox("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

    if selected_brand:
        if selected_brand == "すべての銘柄":
            filtered_stores = nearby_stores
        else:
            filtered_stores = nearby_stores[
                nearby_stores["銘柄"].apply(lambda brands: selected_brand in brands)
            ]

        if not filtered_stores.empty:
            bounds = []
            for _, store in filtered_stores.iterrows():
                brand_html = "".join(
                    f'<span style="background-color: red; color: white; padding: 2px 4px; margin: 2px; display: inline-block;">{brand}</span>'
                    for brand in store["銘柄"]
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
                # 検索地点の座標も bounds に追加
                bounds.append((search_lat, search_lon))  
                m.fit_bounds(bounds, padding=(30, 30))  # 適度な余白を設定
        else:
            st.write(f"「{selected_brand}」を取り扱う店舗はありません。")

# 最寄り駅で検索の分岐
if search_mode == "最寄り駅で検索":
    prefecture_input = st.text_input("都道府県を入力してください（省略可）:")
    station_name = st.text_input("最寄り駅名を入力してください（「駅」は省略可能です）:")

    if station_name:
        # 駅名の形式を確認
        search_query = station_name if "駅" in station_name else station_name + "駅"
        if prefecture_input:
            search_query = f"{prefecture_input} {search_query}"

        # 駅名で検索
        results = geocoder.geocode(query=search_query, countrycode="JP", limit=5)

        if results:
            if len(results) > 1:
                st.write("該当する駅が複数見つかりました。都道府県の入力もしくは候補から選択してください。")
                station_options = [
                    f"{result['components'].get('state', '')} {result['formatted']}" for result in results
                ]
                selected_station = st.selectbox("選択してください：", station_options)
                selected_result = results[station_options.index(selected_station)]
            else:
                selected_result = results[0]

            search_lat = selected_result["geometry"]["lat"]
            search_lon = selected_result["geometry"]["lng"]

            # 地図の初期化
            m = folium.Map(
                location=[search_lat, search_lon],
                zoom_start=15,
                tiles="https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",
                attr="国土地理院",
            )
            folium.Marker(
                [search_lat, search_lon],
                popup=f"{station_name}駅",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(m)

            # 加盟店データとの距離計算
            加盟店_data["distance"] = 加盟店_data.apply(
                lambda row: geodesic((search_lat, search_lon), (row["lat"], row["lon"])).km, axis=1
            )
            nearby_stores = 加盟店_data[加盟店_data["distance"] <= 10]

            # 検索エリアの取り扱い銘柄一覧を表示
            all_brands = set(
                brand for brands in nearby_stores["銘柄"]
                if brands and brands != [""]  # 空リストまたは取り扱い銘柄なしの処理
                for brand in brands
            )
            all_brands.add("すべての銘柄")
            selected_brand = st.selectbox("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

            if selected_brand:
                if selected_brand == "すべての銘柄":
                    filtered_stores = nearby_stores
                else:
                    filtered_stores = nearby_stores[
                        nearby_stores["銘柄"].apply(lambda brands: selected_brand in brands)
                    ]

                if not filtered_stores.empty:
                    bounds = []
                    for _, store in filtered_stores.iterrows():
                        brand_html = "".join(
                            f'<span style="background-color: red; color: white; padding: 2px 4px; margin: 2px; display: inline-block;">{brand}</span>'
                            for brand in store["銘柄"]
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
                        # 検索地点の座標も bounds に追加
                        bounds.append((search_lat, search_lon))  
                        m.fit_bounds(bounds, padding=(30, 30))  # 適度な余白を設定
                else:
                    st.write(f"「{selected_brand}」を取り扱う店舗はありません。")
        else:
            st.warning("該当する駅が見つかりませんでした。")
# 追加: 入力情報クリアボタンのロジック
st.markdown("""
    <style>
        .small-button a {
            font-size: 12px; /* 文字のサイズを小さく */
            padding: 5px 10px; /* 余白を小さく */
            margin: 5px 0; /* ボタン周囲の余白を調整 */
            text-decoration: none; /* アンダーラインを削除 */
            border: 1px solid #ccc; /* 枠線の追加 */
            border-radius: 5px; /* 角を丸める */
            background-color: #f0f0f0; /* ボタンの背景色 */
            color: #333; /* 文字色 */
            display: inline-block; /* インラインブロック表示 */
        }
        .small-button a:hover {
            background-color: #e0e0e0; /* ホバー時の色変更 */
        }
    </style>
    <div class="small-button">
        <a href="https://7drnd3kxvrjrcucyvutntu.streamlit.app/#c898a4f7?cache=clear" target="_self">
            入力情報をクリアする
        </a>
    </div>
""", unsafe_allow_html=True)      

# CSSでレスポンシブ対応（スマホで100%の幅、PCで700px）
st.markdown("""
    <style>
        .st-deck .css-1v3fvcr {
            width: 100% !important;
            height: 500px !important;  /* 画面サイズに応じて高さを設定 */
        }
        @media (max-width: 768px) {
            .st-deck .css-1v3fvcr {
                height: 400px !important;  /* スマホ用に高さ調整 */
            }
        }
    </style>
""", unsafe_allow_html=True)

# 地図を表示
st_folium(m, width="100%", height=500)
st.markdown("""
    <a href="https://www.meimonshu.jp/modules/xfsection/article.php?articleid=377" target="_blank" class="stLinkButton">
        立春朝搾り特設サイトはこちら
    </a>
    """, unsafe_allow_html=True)
