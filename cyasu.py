import streamlit as st
import folium
from streamlit_folium import st_folium
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pandas as pd

import streamlit as st

# カスタムCSSを適用
st.image("kensakup_top.png", use_column_width=True)
st.image("kensakup_topmain.png", use_column_width=True)
st.image("to-kousikip.png", use_column_width=True)
st.image("kensakup_to-map.png", use_column_width=True)
st.markdown("""
    <style>
        /* 背景色を白、テキスト色を黒に設定 */
        body {
            background-color: #ffffff !important;  /* 背景: 白 */
            color: #000000 !important;            /* テキスト: 黒 */
        }
        .stApp {
            background-color: #ffffff !important; /* 全体の背景: 白 */
            color: #000000 !important;           /* テキスト: 黒 */
        }

        /* ヘッダーや見出しのスタイルを明確化 */
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;  /* 見出しの文字色を黒 */
        }

        /* テキストやラベルのスタイル */
        p, label {
            color: #000000 !important;  /* 残りのテキストも黒 */
        }

        /* フォームやテキスト入力フィールドのスタイル */
        input {
            background-color: #f9f9f9 !important; /* フォーム背景: 薄いグレー */
            color: #000000 !important;           /* 入力文字: 黒 */
            border: 1px solid #cccccc !important; /* フォームの枠線: 薄いグレー */
            padding: 10px;                        /* フォームの余白 */
            border-radius: 5px;                   /* フォームの角を丸く */
        }

        /* セレクトボックスのスタイル */
        select {
            background-color: #f9f9f9 !important; /* 背景: 薄いグレー */
            color: #000000 !important;           /* 選択肢: 黒 */
            border: 1px solid #cccccc !important; /* 枠線: 薄いグレー */
            padding: 10px;
            border-radius: 5px;
        }

        /* ボタンのスタイル */
        button {
            background-color: #007BFF !important; /* ボタン背景: 青 */
            color: #ffffff !important;           /* ボタン文字: 白 */
            border: none !important;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3 !important; /* ホバー時の背景: 濃い青 */
        }

/* カスタムボタンのスタイル */
[data-baseweb="radio"] > div {
    display: flex;
    justify-content: center; /* 中央揃え */
    gap: 10px; /* ボタン間の間隔 */
    margin: 20px 0; /* 上下の余白 */
}

[data-baseweb="radio"] > div > label {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 30px; /* ボタンを丸く */
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase; /* 大文字化 */
    transition: all 0.3s ease-in-out;
    border: 2px solid transparent; /* 初期の境界線なし */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 軽い影 */
}

[data-baseweb="radio"] > div > label:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* ホバー時の影 */
}

[data-baseweb="radio"] > div > label[data-selected="true"] {
    background: linear-gradient(90deg, #4facfe, #00f2fe); /* グラデーション背景 */
    color: white;
    border: 2px solid #00f2fe;
}

[data-baseweb="radio"] > div > label[data-selected="false"] {
    background: #f2f2f2; /* 非選択時の背景 */
    color: #a6a6a6; /* 非選択時の文字色 */
    border: 2px solid #cccccc;
}

[data-baseweb="radio"] > div > label[data-selected="false"]:hover {
    background: #e6e6e6; /* ホバー時の非選択背景 */
    color: #808080; /* ホバー時の文字色 */
}  
    </style>
    """, unsafe_allow_html=True)
# 加盟店データを外部ファイルからインポート
from 加盟店_data import 加盟店_data

# OpenCage APIの設定
api_key = "d63325663fe34549885cd31798e50eb2"
geocoder = OpenCageGeocode(api_key)

st.write("郵便番号もしくは住所を入力して、10km圏内の加盟店を検索します。")

# 検索モード選択
search_mode = st.radio(
    "検索方法を選択してください：",
    ("住所で検索", "最寄り駅で検索"),
    key="search_mode",  # ラジオボタンの選択肢を管理するキー
)

# ラジオボタンのカスタムCSSスタイルを適用
st.markdown("""
    <style>
        .stRadio > label {
            display: inline-block;
            padding: 12px 24px;
            margin: 10px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            border: 2px solid transparent;
            text-align: center;
        }
        .stRadio input[type="radio"] {
            display: none;  /* ラジオボタン自体は非表示 */
        }
        .stRadio input[type="radio"]:checked + label {
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            color: #ffffff;
            border: 2px solid #00f2fe;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stRadio input[type="radio"]:not(:checked) + label {
            background: #f2f2f2;
            color: #a6a6a6;
            border: 2px solid #cccccc;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stRadio input[type="radio"]:not(:checked) + label:hover {
            background: #e6e6e6;
            color: #808080;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
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

    selected_brand = st.radio("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

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
                m.fit_bounds(bounds)
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
            selected_brand = st.radio("検索エリアの取り扱い銘柄一覧", sorted(all_brands))

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
                        m.fit_bounds(bounds)
                else:
                    st.write(f"「{selected_brand}」を取り扱う店舗はありません。")

        else:
            st.warning("該当する駅が見つかりませんでした。")

# 地図のレンダリング
st_folium(m, width=700, height=500)
