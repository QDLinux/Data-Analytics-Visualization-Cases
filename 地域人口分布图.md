这是一个使用 Python 和 Pyecharts 库绘制中国各省人口分布地图的示例代码。我们这里将使用第七次全国人口普查（2020年）的部分数据作为示例。

**你需要先安装 Pyecharts 库：**

```bash
pip install pyecharts pandas
```

**Python 代码：**

```python
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
import os

# --- 数据定义 ---
# 数据来源：基于第七次全国人口普查数据 (约数，单位：万人)
# 注意：Pyecharts 需要标准的省份名称，不带 "省"、"市"、"自治区"、"特别行政区" 后缀，
# 但特殊名称如 "内蒙古", "黑龙江", "西藏", "新疆", "广西", "宁夏" 需要完整。
# 直辖市直接用城市名: "北京", "上海", "天津", "重庆"
population_data = {
    "广东": 12601, "山东": 10153, "河南": 9937, "江苏": 8475, "四川": 8367,
    "河北": 7461, "湖南": 6644, "浙江": 6457, "安徽": 6103, "湖北": 5775,
    "广西": 5013, "云南": 4721, "江西": 4519, "辽宁": 4259, "福建": 4154,
    "陕西": 3953, "黑龙江": 3185, "山西": 3492, "贵州": 3856, "重庆": 3205,
    "吉林": 2407, "甘肃": 2502, "内蒙古": 2405, "新疆": 2585, "上海": 2487,
    "台湾": 2360, # 台湾数据通常单独统计，这里加入作示例
    "北京": 2189, "天津": 1387, "海南": 1008, "香港": 747, # 香港数据通常单独统计
    "宁夏": 720, "青海": 593, "西藏": 365, "澳门": 68 # 澳门数据通常单独统计
}

# --- 函数定义 ---

def create_china_population_map(data: dict) -> Map:
    """
    根据省份人口数据创建 Pyecharts 中国地图。

    Args:
        data (dict): 包含省份名称和对应人口数量的字典。

    Returns:
        Map: 配置好的 Pyecharts Map 对象。
    """
    # 1. 将字典转换为 Pyecharts 需要的列表格式 [(省份, 人口), ...]
    data_pair = list(data.items())

    # 2. 找出最大人口数，用于设置 visualMap
    if not data_pair:
        max_population = 100 # 设定一个默认值以防数据为空
    else:
        # 从元组列表中提取所有人口数值
        populations = [item[1] for item in data_pair if isinstance(item[1], (int, float))]
        max_population = max(populations) if populations else 100

    print(f"数据中的最大人口数 (万): {max_population}")

    # 3. 创建地图实例
    map_chart = (
        Map(init_opts=opts.InitOpts(width="1000px", height="800px")) # 设置画布大小
        .add(
            series_name="人口数量 (万)", # 系列名称，会显示在 tooltip 中
            data_pair=data_pair,    # 数据对
            maptype="china",        # 地图类型为中国
            is_map_symbol_show=False, # 不显示地图上的标记点
            label_opts=opts.LabelOpts(is_show=False), # 地图上默认不显示省份名称标签，鼠标悬浮显示
        )
        .set_global_opts(
            # 标题配置
            title_opts=opts.TitleOpts(
                title="中国各省人口分布图 (第七次人口普查)",
                subtitle="数据来源：国家统计局 (单位：万人)",
                pos_left="center" # 标题居中
            ),
            # 视觉映射配置 (核心部分)
            visualmap_opts=opts.VisualMapOpts(
                min_=0,              # 视觉映射的最小值
                max_=max_population, # 视觉映射的最大值，使用动态计算的最大人口
                range_text=["高", "低"], # 两端文本
                is_calculable=True,  # 是否显示拖拽用的手柄（用于筛选范围）
                range_color=["#E0F3F8", "#FFFFBF", "#FFD700", "#FFA500", "#FF4500", "#DC143C"], # 自定义颜色范围（从浅到深）
                pos_left="10%",      # 视觉映射组件离容器左侧的距离
                pos_bottom="10%"     # 视觉映射组件离容器底部的距离
                # --- 或者使用分段式视觉映射 ---
                # is_piecewise=True,
                # pieces=[
                #     {"min": 10000, "label": ">1亿", "color": "#8A0808"},
                #     {"min": 5000, "max": 9999, "label": "5000万-1亿", "color": "#B40404"},
                #     {"min": 3000, "max": 4999, "label": "3000万-5000万", "color": "#DF0101"},
                #     {"min": 1000, "max": 2999, "label": "1000万-3000万", "color": "#F78181"},
                #     {"min": 500, "max": 999, "label": "500万-1000万", "color": "#F5A9A9"},
                #     {"max": 499, "label": "<500万", "color": "#F6CECE"},
                # ]
            ),
            # 提示框配置
            tooltip_opts=opts.TooltipOpts(
                trigger="item", # 数据项图形触发
                formatter="{b}: {c} 万人" # 格式化显示：省份: 人口 万人
            ),
            # 图例配置 (对于单系列地图通常不需要显示)
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return map_chart

# --- 主程序入口 ---
if __name__ == "__main__":
    print("开始生成中国人口地图...")

    # 1. 创建地图对象
    china_map = create_china_population_map(population_data)

    # 2. 渲染地图到 HTML 文件
    output_filename = "china_population_map.html"
    try:
        china_map.render(output_filename)
        print(f"地图已成功生成并保存到: {os.path.abspath(output_filename)}")
        # 可以在这里添加代码自动打开浏览器查看
        # import webbrowser
        # webbrowser.open(os.path.abspath(output_filename))
    except Exception as e:
        print(f"渲染地图时出错: {e}")

    print("处理完成。")
```

**代码解释：**

1.  **导入库：** 导入 `pandas` (虽然这里没直接用，但处理数据常用)，`pyecharts.options` (别名 `opts`) 用于配置，`pyecharts.charts.Map` 用于创建地图，`os` 用于获取文件绝对路径。
2.  **定义数据：** `population_data` 字典存储了省份名称（键）和对应的人口数量（值，单位：万人）。**特别注意省份名称必须符合 Pyecharts 的标准**。
3.  **`create_china_population_map` 函数：**
    *   接收人口数据字典。
    *   将字典转换为 Pyecharts `add` 方法所需的 `[(key, value), ...]` 格式的列表 `data_pair`。
    *   动态计算数据中的最大人口数 `max_population`，用于设置视觉映射 (`visualmap_opts`) 的上限，确保颜色范围能覆盖所有数据。
    *   创建 `Map` 对象，可以设置初始画布大小 (`InitOpts`)。
    *   调用 `.add()` 方法添加数据系列：
        *   `series_name`: 鼠标悬浮时提示框中显示的系列名称。
        *   `data_pair`: 绑定的数据。
        *   `maptype="china"`: 指定地图为中国地图。
        *   `is_map_symbol_show=False`: 不在省份上显示额外的标记点。
        *   `label_opts=opts.LabelOpts(is_show=False)`: 默认不在地图上显示省份名称，保持简洁，鼠标移上去看 tooltip。
    *   调用 `.set_global_opts()` 进行全局配置：
        *   `title_opts`: 设置地图的标题和副标题。
        *   `visualmap_opts`: 这是关键配置，用于将数值（人口）映射到颜色：
            *   `min_`, `max_`: 定义了数值范围。
            *   `range_text`: 在视觉映射条两端显示的文字。
            *   `is_calculable=True`: 允许用户拖动滑块筛选范围。
            *   `range_color`: 自定义颜色过渡（可选，Pyecharts 有默认颜色）。
            *   **注释掉的部分** 展示了如何使用 `is_piecewise=True` 和 `pieces` 来创建分段式的视觉映射，对于人口这种差异巨大的数据有时效果更好。你可以取消注释这部分，并注释掉连续型的配置来尝试。
        *   `tooltip_opts`: 配置鼠标悬浮在省份上时显示的提示框格式。`{b}` 代表省份名（来自 `data_pair` 的键），`{c}` 代表人口数（来自 `data_pair` 的值）。
        *   `legend_opts=opts.LegendOpts(is_show=False)`: 对于只有一个数据系列的地图，图例通常是多余的，可以隐藏。
    *   返回配置好的 `Map` 对象。
4.  **主程序块 (`if __name__ == "__main__":`)**
    *   调用 `create_china_population_map` 函数创建地图实例。
    *   调用地图实例的 `.render()` 方法，将地图输出为 HTML 文件（例如 `china_population_map.html`）。
    *   打印成功信息和文件路径。

运行这段代码后，会在你的 Python 脚本所在的目录下生成一个 `china_population_map.html` 文件。用浏览器打开这个文件，你就能看到一个交互式的中国人口分布地图了。你可以鼠标悬浮在各省份上查看具体人口数量，也可以拖动视觉映射组件的滑块来筛选不同人口范围的省份。
