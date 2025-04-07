# Data-Analytics-Visualization-Cases

设计一个使用AI工具（如豆包、Kimi Chat、DeepSeek等，这里以通用AI代码助手为例）完成数据分析可视化案例的流程。

**案例目标：** 分析一个（虚构的）在线零售商店的销售数据，了解销售趋势、畅销商品类别以及主要销售区域。

**使用工具：**

1.  **AI编程助手** (模拟豆包、DeepSeek、ChatGPT、Copilot等)：用于生成代码、解释代码、调试、提供分析思路。
2.  **Python**：作为主要的编程语言。
3.  **Pandas**：用于数据处理和分析。
4.  **Matplotlib / Seaborn**：用于数据可视化。
5.  **Jupyter Notebook / VS Code (with Python extension)**：作为交互式开发环境。

**数据集（虚构）：** `online_sales.csv`
包含以下列：
*   `InvoiceNo`: 发票号
*   `StockCode`: 产品代码
*   `Description`: 产品描述
*   `Quantity`: 数量
*   `InvoiceDate`: 发票日期 (格式: 'YYYY-MM-DD HH:MM:SS')
*   `UnitPrice`: 单价
*   `CustomerID`: 客户ID
*   `Country`: 国家
*   `Category`: 产品类别 (我们虚构添加，便于分析)

---

**分析步骤及AI应用：**

**第一步：环境设置与数据加载**

1.  **任务描述:** 需要加载CSV数据到Pandas DataFrame，并进行初步查看。
2.  **向AI提问 (示例):**
    *   "请给我Python代码，使用Pandas库加载名为 'online_sales.csv' 的文件到一个DataFrame，并显示前5行和数据的基本信息（列名、非空值、数据类型）。"
    *   "如何检查我的DataFrame中有多少缺失值？"
3.  **AI可能生成的代码 (示例):**

    ```python
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 设置图表样式 (AI 也可以建议)
    sns.set(style="whitegrid")

    # 加载数据
    try:
        df = pd.read_csv('online_sales.csv', encoding='utf-8') # AI可能建议尝试不同编码
        print("数据加载成功！")
        print("\n前5行数据:")
        print(df.head())
        print("\n数据基本信息:")
        print(df.info())
        print("\n各列缺失值数量:")
        print(df.isnull().sum())
    except FileNotFoundError:
        print("错误：'online_sales.csv' 文件未找到。请确保文件在正确的目录下。")
    except Exception as e:
        print(f"加载数据时出错: {e}")

    ```
4.  **结果:** 成功加载数据，了解数据结构、类型和缺失值情况。

**第二步：数据清洗与预处理**

1.  **任务描述:** 处理日期格式、处理负数数量（可能表示退货）、计算总价、处理缺失值。
2.  **向AI提问 (示例):**
    *   "我的 'InvoiceDate' 列是字符串格式，如何将其转换为Pandas的datetime对象？"
    *   "数据中有 'Quantity' 为负数的情况，可能代表退货，暂时先将这些行移除，请给出代码。" (或者：如何将负数Quantity标记为'Returned'?)
    *   "如何计算每行的总价 (Quantity * UnitPrice) 并添加为新列 'TotalPrice'？"
    *   "CustomerID列有缺失值，对于分析客户行为可能有用，暂时保留。但如果UnitPrice有少量缺失，如何用中位数填充？"
3.  **AI可能生成的代码 (示例):**

    ```python
    # 转换日期格式
    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        print("日期格式转换完成。")

    # 处理负数数量 (示例：移除)
    initial_rows = len(df)
    df = df[df['Quantity'] > 0]
    print(f"移除了 {initial_rows - len(df)} 行 Quantity <= 0 的数据。")

    # 计算总价
    if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        print("计算'TotalPrice'列完成。")

    # 处理 UnitPrice 缺失值 (示例：用中位数填充)
    if 'UnitPrice' in df.columns and df['UnitPrice'].isnull().any():
        median_price = df['UnitPrice'].median()
        df['UnitPrice'].fillna(median_price, inplace=True)
        print(f"使用中位数 {median_price} 填充了 UnitPrice 的缺失值。")

    # 再次查看数据信息
    print("\n处理后的数据信息:")
    print(df.info())
    print("\n处理后的前5行:")
    print(df.head())
    ```
4.  **结果:** 数据格式统一，异常值得到处理，计算了关键指标，为后续分析准备好干净的数据。

**第三步：探索性数据分析 (EDA) 与可视化**

**任务1：分析月度销售总额趋势**

1.  **向AI提问:** "我想分析月度销售总额的变化趋势。请写Python代码，从 'InvoiceDate' 提取月份，然后按月份分组计算 'TotalPrice' 的总和，并用Matplotlib或Seaborn绘制线图。"
2.  **AI可能生成的代码:**

    ```python
    if 'InvoiceDate' in df.columns and 'TotalPrice' in df.columns:
        # 提取月份 (确保日期已是datetime对象)
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M') # AI可能提供多种提取方式

        # 按月分组计算总销售额
        monthly_sales = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
        # 将 Period 对象转换为字符串或时间戳以便绘图
        monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str) # 或 .to_timestamp()

        print("\n月度销售总额:")
        print(monthly_sales)

        # 绘制线图
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=monthly_sales, x='YearMonth', y='TotalPrice', marker='o')
        plt.title('月度销售总额趋势')
        plt.xlabel('月份')
        plt.ylabel('总销售额')
        plt.xticks(rotation=45)
        plt.tight_layout() # AI可能建议添加，防止标签重叠
        plt.show()
    else:
        print("错误：缺少 'InvoiceDate' 或 'TotalPrice' 列，无法进行月度销售分析。")
    ```
3.  **结果:** 生成月度销售额的线图，可以直观看到销售额随时间的变化。

**任务2：分析畅销商品类别**

1.  **向AI提问:** "我想知道哪些产品类别最受欢迎。请按 'Category' 分组，计算每个类别的总销售额 'TotalPrice' 和总销量 'Quantity'，并用Seaborn绘制条形图显示销售额最高的前10个类别。"
2.  **AI可能生成的代码:**

    ```python
    if 'Category' in df.columns and 'TotalPrice' in df.columns and 'Quantity' in df.columns:
        # 按类别分组计算总销售额和总销量
        category_sales = df.groupby('Category').agg(
            TotalSales=('TotalPrice', 'sum'),
            TotalQuantity=('Quantity', 'sum')
        ).reset_index()

        # 按销售额排序并取前10
        top_10_categories = category_sales.sort_values(by='TotalSales', ascending=False).head(10)

        print("\n销售额最高的前10个产品类别:")
        print(top_10_categories)

        # 绘制条形图
        plt.figure(figsize=(12, 7))
        sns.barplot(data=top_10_categories, y='Category', x='TotalSales', palette='viridis')
        plt.title('销售额最高的前10产品类别')
        plt.xlabel('总销售额')
        plt.ylabel('产品类别')
        plt.tight_layout()
        plt.show()

        # (可选) 绘制销量前10的条形图 (可以再次提问AI)
        # top_10_quantity = category_sales.sort_values(by='TotalQuantity', ascending=False).head(10)
        # ... (类似绘图代码) ...

    else:
        print("错误：缺少 'Category', 'TotalPrice' 或 'Quantity' 列，无法进行类别分析。")
    ```
3.  **结果:** 生成条形图，清晰展示哪些产品类别贡献了主要的销售额。

**任务3：分析主要销售区域**

1.  **向AI提问:** "我想了解销售主要集中在哪些国家。请按 'Country' 分组，计算每个国家的总销售额 'TotalPrice'，并用条形图展示销售额最高的前10个国家。"
2.  **AI可能生成的代码:**

    ```python
    if 'Country' in df.columns and 'TotalPrice' in df.columns:
        # 按国家分组计算总销售额
        country_sales = df.groupby('Country')['TotalPrice'].sum().reset_index()

        # 排序并取前10 (通常需要排除主要的本国，看其他国家情况，或者直接看全部排名靠前的)
        top_10_countries = country_sales.sort_values(by='TotalPrice', ascending=False).head(10)

        print("\n销售额最高的前10个国家:")
        print(top_10_countries)

        # 绘制条形图
        plt.figure(figsize=(12, 7))
        sns.barplot(data=top_10_countries, y='Country', x='TotalPrice', palette='magma')
        plt.title('销售额最高的前10个国家')
        plt.xlabel('总销售额')
        plt.ylabel('国家')
        plt.tight_layout()
        plt.show()
    else:
        print("错误：缺少 'Country' 或 'TotalPrice' 列，无法进行国家销售分析。")

    ```
3.  **结果:** 生成条形图，识别出主要的销售来源国家。

**第四步：总结与报告**

1.  **任务描述:** 整理分析结果和可视化图表，撰写简要报告。
2.  **向AI提问 (辅助思考):**
    *   "根据以上分析（月度销售高峰在年底、某几个类别销售额突出、销售主要集中在本国和少数几个欧洲国家），请帮我总结一下主要的发现。"
    *   "如何更专业地描述这个销售额的月度波动性？"
    *   "基于这些发现，可以提出哪些业务建议？" (例如：针对高峰期备货、推广畅销品类、拓展潜力市场等)
3.  **AI的辅助:** AI可以帮助组织语言、提供常见的业务解读、或者根据图表特征给出描述性文字的建议。但最终的深入洞察和业务决策需要结合领域知识由人来完成。
4.  **结果:** 形成一份包含主要发现、可视化图表和初步建议的数据分析报告。

---

**AI工具在整个过程中的价值：**

*   **提高效率:** 快速生成基础和重复性的代码（加载、清洗、聚合、绘图）。
*   **降低门槛:** 即使对某些库或函数不太熟悉，也能通过自然语言提问获得可用代码。
*   **提供思路:** 可以询问AI“如何分析X和Y的关系？”或“有哪些常用的可视化方法来看分布？”等，获取分析灵感。
*   **学习与解释:** 可以让AI解释生成的代码、某个函数的用法或某个统计概念。
*   **调试辅助:** 当代码报错时，可以将错误信息和相关代码片段给AI，请求帮助定位和修复问题。

**注意事项：**

*   **理解代码:** 不能完全依赖AI，必须理解生成的代码，确保其逻辑正确且符合分析目标。
*   **验证结果:** AI生成的代码可能存在细微错误或不完全符合预期，需要运行和验证。
*   **数据敏感性:** 在处理真实、敏感数据时，要注意数据隐私和安全，谨慎向公开的AI模型提供具体数据内容。优先使用本地化或有安全保障的AI工具。
*   **迭代优化:** 初步分析后，可能需要根据结果调整分析角度或方法，这需要分析师的主动思考，AI可以辅助实现新的想法。
*   **领域知识:** AI缺乏深入的业务背景知识，最终的解读和决策需要结合实际业务情况。

这个案例展示了如何将AI工具融入数据分析和可视化的工作流中，使其成为一个强大的助手，加速从数据到洞察的过程。
