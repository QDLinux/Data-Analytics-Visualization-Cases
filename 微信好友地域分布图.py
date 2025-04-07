import csv
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Map
import os # 引入 os 模块方便检查文件

# --- 常量定义 ---
# 将配置信息作为常量放在开头，方便修改
CSV_FILENAME = '我的微信好友信息.csv'
PROVINCE_COLUMN_INDEX = 3  # 省份信息在第4列（索引为3）
OUTPUT_HTML_FILENAME = '好友所在省份分布图.html'
MAP_TITLE = "微信好友省份分布图"
MAP_SUBTITLE = "数据来源：微信好友信息CSV文件"
SERIES_NAME = "好友数量"

# --- 函数定义 ---

def load_province_data(filename: str, column_index: int) -> list:
    """
    从CSV文件中加载指定列的省份数据。

    Args:
        filename (str): CSV文件的路径。
        column_index (int): 省份数据所在的列索引（从0开始）。

    Returns:
        list: 包含省份名称的列表。如果文件不存在或读取错误则返回空列表。
    """
    provinces = []
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"错误：文件 '{filename}' 不存在。")
        return provinces

    try:
        # 使用 'utf-8' 编码打开，如果你的文件是其他编码（如 'gbk'），请修改
        with open(filename, 'r', encoding='utf-8-sig') as csvfile: # 'utf-8-sig' 可以处理带BOM的UTF-8文件
            reader = csv.reader(csvfile)
            header = next(reader, None) # 读取并跳过表头
            if header:
                print(f"跳过表头: {header}") # 打印表头以供确认

            for row in reader:
                # 确保行中有足够的列
                if len(row) > column_index:
                    province = row[column_index].strip() # 去除首尾空格
                    # 只添加非空字符串
                    if province:
                        provinces.append(province)
                else:
                    # 可以选择打印警告信息
                    # print(f"警告：行 '{row}' 的列数不足 {column_index + 1}，已跳过。")
                    pass
    except FileNotFoundError: # 再次捕获以防万一 (虽然上面检查过)
         print(f"错误：文件 '{filename}' 未找到。")
    except UnicodeDecodeError:
        print(f"错误：无法使用 'utf-8-sig' 解码文件 '{filename}'。请检查文件编码。")
    except Exception as e:
        print(f"读取CSV文件时发生错误: {e}")

    return provinces

def create_province_map(province_list: list) -> Map:
    """
    根据省份列表生成 Pyecharts 地图。

    Args:
        province_list (list): 包含省份名称的列表。

    Returns:
        Map: Pyecharts Map 对象。
    """
    # 1. 统计省份频率
    # 不再需要过滤 'Province'，因为 load_province_data 中跳过了表头
    # 也不需要过滤空字符串，因为 load_province_data 中处理了
    province_counts = Counter(province_list)

    # 2. 准备 Pyecharts 需要的数据格式: [("省份", 数量), ...]
    # 重要：Pyecharts 通常能识别标准省份名称（如 "山东", "北京"），无需手动加 "省" 或 "市"
    data_pair = list(province_counts.items())

    if not data_pair:
        print("警告：没有有效的省份数据可供绘图。")
        # 返回一个空的Map对象或进行其他处理
        return Map().set_global_opts(title_opts=opts.TitleOpts(title="无有效数据"))

    # 3. 动态计算 visualMap 的最大值
    max_count = max(count for province, count in data_pair) if data_pair else 0

    # 4. 创建地图
    map_chart = (
        Map()
        .add(
            series_name=SERIES_NAME,
            data_pair=data_pair,
            maptype="china",  # 地图类型为中国
            is_map_symbol_show=False, # 通常省份地图不显示标记点
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=MAP_TITLE,
                subtitle=MAP_SUBTITLE,
                pos_left="center" # 标题居中
            ),
            # 设置视觉映射组件
            visualmap_opts=opts.VisualMapOpts(
                max_=max_count + 1, # 设置最大值，+1 避免最大值省份颜色过曝 (可选)
                is_piecewise=False, # 使用连续型视觉映射，如果想分段显示，设为True并配置pieces
                pos_left="10%",     # 调整位置避免遮挡
                pos_bottom="10%"
            ),
            # 设置提示框组件
            tooltip_opts=opts.TooltipOpts(
                trigger="item", # 数据项图形触发
                formatter="{b}: {c}" # 格式化显示：省份名: 数量
            ),
             # 通常一个系列的地图不需要图例，可以隐藏
            legend_opts=opts.LegendOpts(is_show=False)
        )
        # 系列配置项，这里设置省份名称标签不显示在地图上（鼠标悬浮时通过Tooltip显示）
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return map_chart

# --- 主程序入口 ---
if __name__ == "__main__":
    print("开始处理微信好友省份数据...")

    # 1. 加载数据
    province_data = load_province_data(CSV_FILENAME, PROVINCE_COLUMN_INDEX)

    # 2. 检查是否有数据
    if not province_data:
        print("未能加载到省份数据，程序退出。")
    else:
        print(f"成功加载 {len(province_data)} 条原始省份记录。")
        # 3. 创建地图可视化对象
        province_map = create_province_map(province_data)

        # 4. 渲染地图到 HTML 文件
        try:
            province_map.render(path=OUTPUT_HTML_FILENAME)
            print(f"地图已成功生成并保存到: {os.path.abspath(OUTPUT_HTML_FILENAME)}")
        except Exception as e:
            print(f"渲染HTML文件时出错: {e}")

    print("处理完成。")
