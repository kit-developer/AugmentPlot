from tools.analyse_preset.plot import common as pl_common


module_info = {
    "1_meter": {
        "func": pl_common.last_value_meter,
        "require": ["square"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame_max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
            "datas_max_dim": (2,)
        },
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {}
        },
        "projection": "polar"
    },
    "1_meter_diff": {
        "func": pl_common.last_differential_meter,
        "require": ["square"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame_max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
            "datas_max_dim": (1,)
        },
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}
        },
        "projection": "polar"
    },
    "v_meter": {
        "func": pl_common.last_differential_meter,
        "require": ["vertical"],
        "iterable": {       # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame_max_num": (-1, 1),    # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
            "datas_max_dim": (1, )
        },
        "extent": (1, 1),       # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}
        },
        "projection": "polar"
    },
    "h_meter": {
        "func": pl_common.last_differential_meter,
        "require": ["horizontal"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame_max_num": (1, -1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
            "datas_max_dim": (1,)
        },
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}
        },
        "projection": "polar"
    },
    "x_color_bar": {
        "func": pl_common.color_differential2,
        "require": ["horizontal", "fit_main_w"],
        "iterable": {       # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame_max_num": (1, 1),    # (height, width) 上限がない場合は-1
            "datas_max_dim": (2, ),
        },
        "extent": (1, -1),       # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": ["xlim"],
            "values": {}
        },
        "projection": None
    }
}

# vertical      : 縦に大きい必要があるか
# horizontal    : 横に大きい必要があるか
# fit_main_w    : メインエリアと同じ幅で、位置も揃える必要があるか
# fit_main_h    : メインエリアと同じ高さで、位置も揃える必要があるか
# main_upper    : メインエリアの上側である必要があるか
# main_bottom   : メインエリアの下側である必要があるか
# main_left     : メインエリアの左側である必要があるか
# main_right    : メインエリアの右側である必要があるか
