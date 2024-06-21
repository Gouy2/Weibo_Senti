import requests
import time
import gradio as gr

# 目标URL
base_url = "https://weibo.com/ajax/statuses/buildComments"

params = {
    # 'is_reload': '1',
    # 'id': '5044745389214394',  # 替换为实际微博ID
    # 'is_show_bulletin': '2',
    # 'is_mix': '0',
    # 'count': '20',  # 每次请求获取的评论数量
    # 'uid': '6168007956',  # 替换为实际用户ID
    # 'fetch_level': '0',
    # 'locale': 'zh-CN',
    'max_id': '0'  # 初始max_id为0
}

# 发送GET请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': 'XSRF-TOKEN=WnVzx2fpdqBF48spPlDHHRWs; SUB=_2A25Ld7mpDeRhGeNN6lIU-SfPzDuIHXVoDLNhrDV8PUNbmtAGLRDQkW9NSc49BSSaRZwesa-jQhI-vxucNiJvWTLc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5lDbLBfIcKTL_rTWxKTNT.5NHD95Qfe027SK.4e0MNWs4DqcjsKgvuqgU4; ALF=02_1721456378; WBPSESS=88rt2yfP_O6BJVfydi3SDdvU6uEYhdWruOkvLehnMlt6jqIuJ3OrEODFmP8voDKkKPusHklO7-4h_vbJRQs_JqkFaqOMgvIBqx6RvBoIsDPkm23pTLWU_gHg_5saXJ9Ktmn3UafqNoOgnWqvcsTZ-Q==' 
}

proxies = {
    "http": None,
    "https": None,
}



# comments_num = 1000
# epochs = comments_num // 20
# print(f"开始爬取评论，共{comments_num}条评论！")
# print(f"共需请求{epochs}次")


# 爬取评论的函数
def run_spider(url, referer, cookie, num_comments):
    comments = []
    epochs = num_comments // 20

    headers['Referer'] = referer
    headers['Cookie'] = cookie

    for i in range(epochs):
        response = requests.get(url, headers=headers,params=params, proxies=proxies)

        if response.status_code == 200:
            json_data = response.json()
            comments_data = json_data.get('data', [])

            if not comments_data:
                break

            for comment in comments_data:
                text_raw = comment.get('text_raw', '')
                comments.append(text_raw)

            max_id = json_data.get('max_id', '0')
            if max_id == '0' or not max_id:
                break

            params['max_id'] = max_id
            time.sleep(2)
        else:
            print(f"Failed to retrieve the data. Status code: {response.status_code}")
            break

    return comments[:num_comments]  # 返回指定数量的评论

def gr_interface(url, referer, cookie):
    # 调用爬虫函数获取评论
    comments = run_spider(url, referer, cookie, num_comments=500)  # 设置默认爬取评论数量为100

    # 将每条评论格式化为一行输出
    formatted_comments = "\n".join(comments)

    return formatted_comments

# 设置 Gradio 界面
iface = gr.Interface(
    fn=gr_interface,
    inputs=[
        gr.Textbox(label="输入URL"),
        gr.Textbox(label="输入Referer"),
        gr.Textbox(label="输入Cookie")
    ],
    outputs=gr.Textbox(label="爬取的所有句子", type="text"),
    title="评论爬取与显示",
    description="输入URL和Referer以爬取评论并显示。"
)

iface.launch()