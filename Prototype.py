from pynput import keyboard
import pyperclip
import requests
import json

# 在这里定义你的快捷键
COMBINATION = {keyboard.Key.f9}  # F9
current_keys = set()  # 按下的键

# 读取剪贴板内容
to_translate = pyperclip.paste()

# 获取你的 OpenAI API key
api_key = ''  # 在两个单引号里写入你的API Key

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',  # 使用你的 OpenAI API key
}

# 新增一个全局变量作为标志
translate_activated = False

def translate_clipboard_content():
    global translate_activated

    # 显示提示信息
    print("开始翻译中...")

    # 获取剪贴板上的文本
    user_content = pyperclip.paste()

    data = {
        'model': 'gpt-3.5-turbo-0613',
        'messages': [
            {
                'role': 'system',
                'content': '请作为一个训练有素的翻译，帮我把给定的所有文本翻译成流畅的中文文本。'
            },
            {
                'role': 'user',
                'content': user_content  # 使用剪贴板上的文本
            }
        ]
    }

    # 在两个单引号里写入你的自定义目标URL
    response = requests.post('', headers=headers, data=json.dumps(data))

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()

        # 提取 assistant 发送的消息
        message = data['choices'][0]['message']['content']
        print(message)

        # 将翻译结果写入剪贴板
        pyperclip.copy(message)
    else:
        print("请求失败，状态码：", response.status_code)

    # 翻译完成后，重置标志变量
    translate_activated = False

def on_press(key):
    global translate_activated

    if key in COMBINATION and not translate_activated:
        translate_activated = True
        translate_clipboard_content()

def on_release(key):
    global translate_activated

    if key in COMBINATION:
        translate_activated = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

