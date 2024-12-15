
custom_css = """
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
    """
