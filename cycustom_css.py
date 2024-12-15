 custom_css = """
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
    gap: 3px; /* ボタン間の間隔 */
    margin: 5px 0; /* 上下の余白 */
}

[data-baseweb="radio"] > div > label {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 10px; /* ボタンを丸く */
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
/* スマホ表示のセレクトボックスのスタイルのみ変更 */
select {
  -webkit-appearance: none; /* iOS Safari, Chrome for iOS 対応 */
  -moz-appearance: none;   /* Firefox 対応 */
  appearance: none;        /* その他のブラウザ対応 */
  background-color: #ffffff; /* 白背景 */
  color: #000000;            /* 黒文字 */
  border: 1px solid #cccccc; /* 枠線の色 */
  border-radius: 4px;        /* 角を丸くする */
  padding: 10px;             /* 内側の余白を追加 */
}

/* セレクトボックスのホバー効果 */
select:hover {
  border-color: #888888; /* ホバー時の枠線色 */
}

/* セレクトボックスのフォーカス効果 */
select:focus {
  outline: none;              /* デフォルトのアウトラインを消す */
  border-color: #555555;     /* フォーカス時の枠線色 */
}

/* カスタムのドロップダウンアイコン */
select::after {
  content: '\25BC';          /* ▼の記号を表示 */
  position: absolute;
  right: 10px;
  pointer-events: none;      /* クリックを無効化 */
}
 /* カスタムリンクボタンのスタイル */
        .stLinkButton {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            background-color: #ffffff; /* 背景色: 白 */
            color: #000000; /* テキスト色: 黒 */
            border: 2px solid #ff0000; /* 枠線色: 赤 */
            border-radius: 5px; /* 角を丸く */
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .stLinkButton:hover {
            background-color: #ffcccc; /* ホバー時の背景色: 薄い赤 */
            color: #ff0000; /* ホバー時のテキスト色: 赤 */
        }
    """
