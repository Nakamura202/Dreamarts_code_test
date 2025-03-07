from collections import defaultdict

# 経路と距離を保存
g_max_path,g_max_dist=[],0

# 標準入力から無向グラフを作成する関数
def value_to_graph(data):
    # グラフの構築
    graph = defaultdict(list)
    for start, end, distance in data:
        graph[start].append((end, float(distance)))
        graph[end].append((start, float(distance)))  # 無向グラフとして扱う
    return graph  # グラフ


# 経路の探索
def find_longest_path(node, visited, path, total_distance,first_node,graph):
    global g_max_path,g_max_dist

    # 点，経路を記録
    visited.add(node)
    path.append(node)

    # 隣り合うノードのペアを作成
    path_pairs = set(zip(path, path[1:]))

    # 未訪問の経路を取得
    unvisited_paths = [
      (neighbor, distance) for neighbor, distance in graph[node]
      if (node, neighbor) not in path_pairs and (neighbor, node) not in path_pairs
    ]
    # 未訪問の点がない場合
    if (not any(neighbor not in visited for neighbor, _ in graph[node])):
        # 現在の点からの未訪問経路があった場合
        if unvisited_paths:
            # 未訪問経路の中で最長経路を選択
            neighbor,distance = max(unvisited_paths, key=lambda x: x[1])
            # 2進数表現のため，四捨五入
            total_distance=round(total_distance+distance,3)
            # 現在の最長経路より長い場合
            if g_max_dist < total_distance:
                g_max_dist,g_max_path=total_distance,path+[neighbor]
        # 現在の点からの未訪問経路がない場合
        else:
            g_max_dist,g_max_path=total_distance,path

    # 未訪問の点があった場合
    else:
        # 再帰的に次の経路を探索
        for neighbor, distance in graph[node]:
            # 未訪問の点があった場合
            if neighbor not in visited:
                find_longest_path(neighbor, visited.copy(), path.copy(), total_distance + distance,first_node,graph)
                # 現在の点からの経路があった場合
                if unvisited_paths:
                    for neighbor, distance in unvisited_paths:
                        # 経路の先の点の中で始点と同じ場合
                        if neighbor==first_node:
                            total_distance=round(total_distance+distance,3)
                        # 現在の最長経路より長い場合  
                        if g_max_dist < total_distance:
                            g_max_dist,g_max_path=total_distance,path+[neighbor]


def main():
    global g_max_path,g_max_dist
    
    # ユーザーに入力を求めるループ
    print("データを入力してください")
    print("空列を入力（Enter2回）と経路を探索します")
    data=[]
    while True:
        input_data = input("")
        #　空列を入力（Enter2回）
        if input_data=="":
            print("探索を開始")
            break
        
        # 文字列をカンマで分割して,空白を取り除き，リスト化
        values = [v.strip() for v in input_data.split(',')]
        # 入力が正しい形式であるかを確認し、間違っていた場合はスキップ
        try:
            # 1番目と2番目は文字列、3番目はfloatに変換
            data.append((values[0], values[1], float(values[2])))
        except (IndexError, ValueError) as e:
            # 想定していない入力（カンマの数が足りない、または浮動小数点数に変換できない場合）はスキップ
            print("不正な入力がありました。再度入力してください。")
            continue
 

    # 入力から無向グラフの作成
    graph = value_to_graph(data)

    # すべての始点で経路を探索する
    for start_node in graph:
        find_longest_path(start_node, set(), [], 0,start_node,graph)

    for node in g_max_path:
        print(node)

if __name__ == "__main__":
    main()
