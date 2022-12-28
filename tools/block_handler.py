import numpy as np
import copy
import pprint

'''
check_skipには、連続した点座標が入る
battingには、バッティングが含まれているブロックの原点座標が入る
new_blockのbattingには、分割対象になっているブロックが持つbattingを、分割をさせるブロックと同じ別軸を含まないように引き継ぐ
'''


def block_handle(main_area, custom_area, debug_show=False):
    tmp = np.ones_like(main_area, dtype="int8")
    tmp = tmp - main_area
    sub_area = tmp - custom_area

    if debug_show:
        print(sub_area)

    block_possibility = possible_block(sub_area, priority=("square", "width", "height"))

    confirmed_block = block_choice(block_possibility, priority=("square", "width", "height"),
                                   show_progress=debug_show)

    return confirmed_block


def block_choice(block_possibility, priority=("square", "width", "height"), show_progress=False):
    block_possibility = block_possibility.items()

    confirmed_block = []

    while True:

        for k in priority[::-1]:
            block_possibility = sorted(block_possibility, key=lambda item: item[1][k], reverse=True)

        if show_progress:
            print("")
            pprint.pprint(block_possibility)

        pos = block_possibility[0][0]
        block = block_possibility[0][1]
        if block["square"] <= 0:
            break

        confirmed_block.append((pos, {k: v for k, v in block.items() if k != "batting" and k != "cross"}))
        block_possibility.pop(0)

        if len(block_possibility) <= 0:
            break

        for bat_pos in block["batting"]:

            # bat_posに一致する情報をblock_possibilityから抜き出す
            tmp = [bp[1] for bp in block_possibility if bp[0] == bat_pos]
            if len(tmp) > 0:
                bat_block = tmp[0]
                block_possibility = batting_resolve(block_possibility, pos, block, bat_pos, bat_block)

        for cr_pos in block["cross"]:
            # cr_posに一致するcross情報を持っているものをblock_possibilityから抜き出す
            tmp = [bp for bp in block_possibility if cr_pos in bp[1]['cross']]
            if len(tmp) > 0:
                remote_bat_pos = tmp[0][0]
                remote_bat_block = tmp[0][1]
                block_possibility = batting_resolve(block_possibility, pos, block, remote_bat_pos, remote_bat_block)

        # 確定させる範囲の点をすべてのcrossから削除する
        for i in range(pos[0], pos[0] + block["height"]):
            for j in range(pos[1], pos[1] + block["width"]):
                for bp in block_possibility:
                    if (i, j) in bp[1]["cross"]:
                        bp[1]["cross"] = [c for c in bp[1]["cross"] if c != (i, j)]

        if len(block_possibility) <= 0:
            break

    return confirmed_block


def batting_resolve(block_possibility, pos, block, bat_pos, bat_block):
    new_blocks = []

    # 幅に余剰がある場合
    sub_w = bat_block["width"] - block["width"]
    if sub_w > 0:

        # 左側が余る
        left_w = pos[1] - bat_pos[1]
        if left_w > 0:
            new_block = new_block_surplus(bat_pos, pos, bat_block, left_w, "width")
            new_blocks.append(new_block)

        # 右側が余る
        right_w = bat_pos[1] + bat_block["width"] - (pos[1] + block["width"])
        if right_w > 0:
            new_pos = (bat_pos[0], pos[1] + block["width"])
            new_block = new_block_surplus(new_pos, pos, bat_block, right_w, "width")
            new_blocks.append(new_block)

    # 高さに余剰がある場合
    sub_h = bat_block["height"] - block["height"]
    if sub_h > 0:

        # 上側が余る
        upper_h = pos[0] - bat_pos[0]
        if upper_h > 0:
            new_block = new_block_surplus(bat_pos, pos, bat_block, upper_h, "height")
            new_blocks.append(new_block)

        # 下側が余る
        lower_h = bat_pos[0] + bat_block["height"] - (pos[0] + block["height"])
        if lower_h > 0:
            new_pos = (pos[0] + block["height"], bat_pos[1])
            new_block = new_block_surplus(new_pos, pos, bat_block, lower_h, "height")
            new_blocks.append(new_block)

    block_possibility = [bp for bp in block_possibility if bp[0] != bat_pos]
    block_possibility.extend(new_blocks)

    seen = []
    block_possibility = [x for x in block_possibility if x not in seen and not seen.append(x)]

    return block_possibility


def new_block_surplus(new_pos, pos, bat_block, surplus, dire):
    if dire == "width":
        axis = 1
    elif dire == "height":
        axis = 0
    else:
        raise ValueError("dire must be width or height")

    w = bat_block["width"] if dire == "height" else surplus
    h = bat_block["height"] if dire == "width" else surplus
    new_block = (new_pos,
                 {
                     "width": w,
                     "height": h,
                     "square": w * h,
                     "batting": [bb for bb in bat_block["batting"] if bb[axis] != pos[axis]],
                     "cross": [bb for bb in bat_block["cross"] if bb[axis] != pos[axis]]
                 })

    return new_block


def possible_block(sub_area, priority=("square", "width", "height")):

    block_possibility = {}
    check_skip_r = {}
    check_skip_b = {}
    check_skip_confirm = {}
    for i, row in enumerate(sub_area):
        for j, val in enumerate(row):

            batting = []
            if (i, j) not in check_skip_r and (i, j) not in check_skip_confirm:

                # 右が連続しているかチェック
                block_num_r = check_continue(sub_area, i, j, check_skip_r, "right")

                # 右に連続しているかつ上の連続に影響され、check_skip_bに登録されてしまった場合は復活させる
                if block_num_r > 1 and (i, j) in check_skip_b:
                    batting = check_skip_b[(i, j)]
                    check_skip_b = {k: v for k, v in check_skip_b.items() if k != (i, j)}
            else:
                block_num_r = 0

            if (i, j) not in check_skip_b and (i, j) not in check_skip_confirm:

                # 下が連続しているかチェック
                block_num_b = check_continue(sub_area, i, j, check_skip_b, "below")

                # 下に連続しているかつ左の連続に影響され、check_skip_rに登録されてしまった場合は復活させる
                if block_num_b > 1 and (i, j) in check_skip_r:
                    batting = check_skip_r[(i, j)]
                    check_skip_r = {k: v for k, v in check_skip_r.items() if k != (i, j)}

                    block_num_r = check_continue(sub_area, i, j, check_skip_r, "right")
            else:
                block_num_b = 0

            # スキップしたもの同士の交点を検出
            cross = []
            if (i, j) in check_skip_r and (i, j) in check_skip_b:
                cross.extend(check_skip_r[(i, j)])
                cross.extend(check_skip_b[(i, j)])
                cross = list(set(cross))

            # 右も下も２つ以上連続している場合、サブエリアでない部分を考慮する
            if block_num_r > 1 and block_num_b > 1:
                block_num_dict = {}
                bnr = block_num_r
                r_last_continue = 0
                for b_i in range(0, block_num_b):
                    r_last = True
                    for r_j in range(0, bnr):
                        # サブエリアでない部分を発見
                        if sub_area[i+b_i][j+r_j] == 0:
                            block_num_dict[bnr] = b_i
                            bnr = r_j
                            r_last = False
                            r_last_continue = 0
                            break
                    # 横方向の走査が最後まで回ったら２段以上の可能性
                    if r_last:
                        r_last_continue += 1
                        block_num_dict[bnr] = r_last_continue

                block_num_dict[bnr] = block_num_b

                tmp = []
                for w, h in block_num_dict.items():
                    tmp.append({
                        "width": w,
                        "height": h,
                        "square": w * h,
                        "batting": batting,
                        "cross": []
                    })

                # 一番良いものだけ作成
                for k in priority[::-1]:
                    tmp = list(sorted(tmp, key=lambda item: item[k], reverse=True))
                block_possibility[(i, j)] = tmp[0]

                # 確定分はskipする
                for b_i in range(tmp[0]["height"]):
                    for r_j in range(tmp[0]["width"]):
                        check_skip_confirm = add_skip(check_skip_confirm, (i+b_i, j+r_j), (i, j))

                # 確定しなかった部分のskipを復活させる
                for b_i in range(i + tmp[0]["height"], i + block_num_b):
                    if (b_i, j) in check_skip_b:
                        check_skip_b.pop((b_i, j))
                for r_j in range(j + tmp[0]["width"], j + block_num_r):
                    if (i, r_j) in check_skip_r:
                        check_skip_r.pop((i, r_j))

            else:
                block_possibility[(i, j)] = {
                    "width": block_num_r if block_num_b != 0 else 0,
                    "height": block_num_b if block_num_r != 0 else 0,
                    "square": block_num_r * block_num_b,
                    "batting": batting,
                    "cross": []
                }

            for pos in batting:
                block_possibility[pos]["batting"].append((i, j))
            for pos in cross:
                block_possibility[pos]["cross"].append((i, j))

    return block_possibility


def check_continue(sub_area, i, j, check_skip, direction):
    shape = sub_area.shape
    ctn = True
    n = -1
    while ctn:
        n += 1
        if direction == "right":
            if shape[1] > j + n:
                ctn = sub_area[i][j+n] == 1
                if ctn and n > 0:
                    check_skip = add_skip(check_skip, (i, j+n), (i, j))
            else:
                ctn = False
        else:
            if shape[0] > i + n:
                ctn = sub_area[i+n][j] == 1
                if ctn and n > 0:
                    check_skip = add_skip(check_skip, (i+n, j), (i, j))
            else:
                ctn = False
    return n


def add_skip(check_skip, skip_pos, add_pos):
    if skip_pos not in check_skip:
        check_skip[skip_pos] = [add_pos]
    else:
        check_skip[skip_pos].append(add_pos)
    return check_skip


def test_preset():
    dataset = []
    main_area = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 1, 1, 0, 0]])
    myans = [((0, 3), {'height': 3, 'square': 6, 'width': 2}),
             ((0, 0), {'height': 2, 'square': 4, 'width': 2}),
             ((0, 2), {'height': 1, 'square': 1, 'width': 1}),
             ((2, 0), {'height': 1, 'square': 1, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 0],
                          [0, 1, 1, 1, 0]])
    myans = [((0, 0), {'height': 1, 'square': 5, 'width': 5}),
             ((1, 0), {'height': 1, 'square': 2, 'width': 2}),
             ((1, 4), {'height': 2, 'square': 2, 'width': 1}),
             ((2, 0), {'height': 1, 'square': 1, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0],
                          [0, 1, 1, 1, 0]])
    myans = [((0, 0), {'height': 2, 'square': 6, 'width': 3}),
             ((0, 4), {'height': 3, 'square': 3, 'width': 1}),
             ((2, 0), {'height': 1, 'square': 1, 'width': 1}),
             ((0, 3), {'height': 1, 'square': 1, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 0, 1, 1, 0],
                          [0, 0, 1, 1, 0],
                          [0, 0, 0, 0, 0]])
    myans = [((0, 0), {'height': 3, 'square': 6, 'width': 2}),
             ((2, 2), {'height': 1, 'square': 3, 'width': 3}),
             ((0, 4), {'height': 2, 'square': 2, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 0, 1, 1, 0],
                          [0, 0, 1, 1, 0],
                          [0, 0, 0, 0, 0]])
    myans = [((0, 0), {'height': 3, 'square': 6, 'width': 2}),
             ((2, 2), {'height': 1, 'square': 3, 'width': 3}),
             ((0, 4), {'height': 2, 'square': 2, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 1, 1, 0, 0],
                          [0, 1, 1, 0, 0],
                          [0, 0, 0, 0, 0]])
    myans = [((0, 3), {'height': 3, 'square': 6, 'width': 2}),
             ((2, 0), {'height': 1, 'square': 3, 'width': 3}),
             ((0, 0), {'height': 2, 'square': 2, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 1, 0, 0, 0],
                          [0, 1, 1, 0, 0],
                          [0, 0, 1, 0, 0]])
    myans = [((0, 3), {'height': 3, 'square': 6, 'width': 2}),
             ((0, 0), {'height': 3, 'square': 3, 'width': 1}),
             ((0, 2), {'height': 1, 'square': 1, 'width': 1}),
             ((2, 1), {'height': 1, 'square': 1, 'width': 1})]
    dataset.append((main_area, myans))

    main_area = np.array([[0, 0, 1, 1, 0],
                          [0, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0]])
    myans = [((2, 0), {'height': 1, 'square': 5, 'width': 5}),
             ((0, 0), {'height': 2, 'square': 2, 'width': 1}),
             ((0, 4), {'height': 2, 'square': 2, 'width': 1}),
             ((0, 1), {'height': 1, 'square': 1, 'width': 1})]
    dataset.append((main_area, myans))

    for i, d in enumerate(dataset):
        custom_area = np.array([[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])
        confirmed_block = block_handle(d[0], custom_area, debug_show=False)
        if len(confirmed_block) == len(d[1]) and all([cb in d[1] for cb in confirmed_block]):
            print("dataset", i, "OK")
        else:
            print("dataset", i, "Bad")
            print(d[0])
            print("confirmed_block")
            pprint.pprint(confirmed_block)
            print("answer")
            pprint.pprint(d[1])


def test_block_handle():
    main_area = np.array([[0, 0, 1, 0, 1],
                          [0, 1, 1, 0, 1],
                          [0, 0, 0, 0, 0]])
    custom_area = np.array([[0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0]])
    confirmed_block = block_handle(main_area, custom_area, debug_show=True)

    print("-------")
    print(main_area)
    print("-------")
    pprint.pprint(confirmed_block)


"""
完全版にする場合
175: if (i, j) not in check_skip_r and (i, j) not in check_skip_confirm:
187: if (i, j) not in check_skip_b and (i, j) not in check_skip_confirm:
下に変更
175: if (i, j) not in check_skip_r:
187: if (i, j) not in check_skip_b:
して、
block_possibilityのvalueをリスト（複数対応）にする

理由：
possible_blockの208以降の１座標にて複数のブロック選択肢が撮れる場合の流れで
243のように１つに決め打ちしてしまっていることが問題となっているから
"""


if __name__ == '__main__':
    test_block_handle()
    # test_preset()
