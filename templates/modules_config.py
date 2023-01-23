from tools.analyse_preset.plot import common as pl_common


module_priority = [
    "1_rader",
    "1_frequency",
    "1_meter",
    "1_meter_diff",
    "frequency",
    "x_color_bar",
    "v_meter",
    "h_meter",
]

module_info = {

    "1_meter": {
        "func": pl_common.last_value_meter,
        "require": ["square"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (3,),
                "priority": None}},
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {}},
        "projection": "polar"
    },

    "1_rader": {
        "func": pl_common.last_value_rader,
        "require": ["square"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (8, 3),
                "min_dim": (3, -1),
                "priority": None}},
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {}},
        "projection": "polar"
    },

    "1_meter_diff": {
        "func": pl_common.last_differential_meter,
        "require": ["square"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (1,),
                "priority": None}},
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}},
        "projection": "polar"
    },

    "v_meter": {
        "func": pl_common.last_differential_meter,
        "require": ["vertical"],
        "iterable": {       # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (-1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (1,),
                "priority": None}},
        "extent": (1, 1),       # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}},
        "projection": "polar"
    },

    "h_meter": {
        "func": pl_common.last_differential_meter,
        "require": ["horizontal"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, -1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (1,),
                "priority": None}},
        "extent": (1, 1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {"dims": 2}},
        "projection": "polar"
    },

    "x_color_bar": {
        "func": pl_common.color_differential,
        "require": ["horizontal", "fit_main_w"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (-1,),
                "priority": None}},
        "extent": (1, -1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": ["xlim"],
            "values": {"dims": 2}},
        "projection": None
    },

    "frequency": {
        "func": pl_common.frequency,
        "require": ["horizontal"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (-1,),
                "priority": None}},
        "extent": (1, -1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {
                "sampling_num": 100,
                "complement_way": "cubic",
                "dt(sec)": 1,
            }},
        "projection": None
    },

    "1_frequency": {
        "func": pl_common.frequency,
        "require": ["horizontal"],
        "iterable": {  # 複数次元データを処理できるか（axes → グラフ複数枠で対応可、data → １つのグラフ内で対応可）
            "frame": {
                "max_num": (1, 1),  # (height, width) 上限がない場合は-1(使用するサブエリアに依存)
                "priority": None},
            "datas": {
                "max_dim": (1,),
                "priority": None}},
        "extent": (1, -1),  # 1区画あたりを広げられるか
        "arg_values": {
            "main_item": [],
            "values": {
                "sampling_num": 100,
                "complement_way": "cubic",
                "dt(sec)": 0.1,
                "bar_chart": True,
            }},
        "projection": None
    },
}


# サブエリアに求める要求内容
# vertical      : 縦に大きい必要があるか
# horizontal    : 横に大きい必要があるか
# fit_main_w    : メインエリアと同じ幅で、位置も揃える必要があるか
# fit_main_h    : メインエリアと同じ高さで、位置も揃える必要があるか
# main_upper    : メインエリアの上側である必要があるか
# main_bottom   : メインエリアの下側である必要があるか
# main_left     : メインエリアの左側である必要があるか
# main_right    : メインエリアの右側である必要があるか


# 照合数値の優先順位
# 追加する場合はmain_axes_map.pyのmain_axes_mapと、paring_data.pyの_check_num_mapにも追加
# same_attr_construction        : g_attributeに対してl_attributeの構成がまったく同じなgroupの数
# include_attr_construction     : g_attributeに対して同じl_attributeが含まれているようなgroupの数
# attr_tree_r                   : l_attributeが同じg_attributeに何個含まれているかという数
# labels_num                    : 各groupに含まれるlabelの数
# labels_num_same_attr          : 各groupに含まれるl_attribute毎のlabelの数       (_check_num_mapへ未追加のため反映なし)
# attr_num                      : 各groupに含まれるg_attributeの数と、各labelに含まれるl_attributeの数
