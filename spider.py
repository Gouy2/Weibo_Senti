import requests
import time

# 目标URL
base_url = "https://weibo.com/ajax/statuses/buildComments"

params = {
    'is_reload': '1',
    'id': '5044745389214394',  # 替换为实际微博ID
    'is_show_bulletin': '2',
    'is_mix': '0',
    'count': '20',  # 每次请求获取的评论数量
    'uid': '6168007956',  # 替换为实际用户ID
    'fetch_level': '0',
    'locale': 'zh-CN',
    'max_id': '0'  # 初始max_id为0
}

# 发送GET请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://weibo.com/6168007956/OiM1YCF5g',
    'Cookie': 'SINAGLOBAL=3031026914434.709.1718289909763; SUB=_2A25Lb3cmDeRhGeNN6lIU-SfPzDuIHXVoBfburDV8PUNbmtAGLRjTkW9NSc49BX1u9u1n0Q5LwvU-_wnW0l_gK-DQ; ALF=02_1720882294; UOR=,,link.csdn.net; _s_tentry=weibo.com; Apache=6490922095566.707.1718352260820; ULV=1718352260823:2:2:2:6490922095566.707.1718352260820:1718289909768; XSRF-TOKEN=gHMoEiq9IpyzcRV5YAZMprfP; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CihO79b2SpQKe41szsbJVYH-e-KkbZXxvaEBJmElKUNq4fwjXj7wvzhgsPye6hvZoJpIccxoxpKkTXN7wMPCNFkuswYfJHA2d3w5m91h6HZhPihoTnuqDcE7uyGQCiD2f3mCLc8ImRnnG60h5yuqXif76FcIBLWfHtW7QdVQAITupzoZ_qJIDs1d5DIINhgeQ==' 
}

proxies = {
    "http": None,
    "https": None,
}



comments_num = 1000
epochs = comments_num // 20
print(f"开始爬取评论，共{comments_num}条评论！")
print(f"共需请求{epochs}次")

with open('comments.txt', 'w', encoding='utf-8') as file:
    for i in range(epochs):
        # 发送GET请求
        response = requests.get(base_url, headers=headers, params=params, proxies=proxies)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON数据
            json_data = response.json()
            comments_data = json_data.get('data', [])
            
            if not comments_data:
                print("No more comments found.")
                break
            
            # 遍历每条评论
            for comment in comments_data:
                # 获取评论文本内容，并写入文件
                text_raw = comment.get('text_raw', '')
                file.write(text_raw + '\n')

                # print(f"已完成第{comments_data.index(comment)+1}条评论的爬取")
            
            if (i+1) % 5 == 0:
                print(f"已完成{(i+1)*20}条评论的爬取")
            # print(f"Fetched {len(comments_data)} comments.")
            
            # 获取下一个max_id
            max_id = json_data.get('max_id', '0')
            
            if max_id == '0' or not max_id:
                print("Reached the last page of comments.")
                break
            
            # 更新params的max_id
            params['max_id'] = max_id
            
            # 为了避免频繁请求导致被封禁IP，休眠一段时间
            
            time.sleep(2)
        else:
            print(f"Failed to retrieve the data. Status code: {response.status_code}")
            break

print("结束爬取评论！")