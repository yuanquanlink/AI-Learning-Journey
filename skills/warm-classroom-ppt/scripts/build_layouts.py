"""Build editable 16:9 classroom layout examples with OfficeCLI."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def build(output):
    cli = shutil.which('officecli')
    if not cli:
        raise SystemExit('Install officecli before building the layout template.')
    if output.exists():
        raise SystemExit('Output already exists. Choose a new filename.')
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([cli, 'create', str(output)], check=True)
    layouts = [
        ('课程主题', [('课程目标', 2, 5, 14, 6), ('主题插图位置', 19, 3, 12, 12)]),
        ('作品说明', [('作品图片位置', 2, 4.5, 20, 11), ('成果说明与任务', 23, 4.5, 9, 11)]),
        ('观察与对话', [('人物或图片位置', 2, 5, 10, 10), ('一个主要问题', 14, 5, 17, 4), ('学生自己的回答', 16, 10, 15, 4)]),
        ('分镜与依据', [('第一格', 2, 4.5, 14, 5), ('第二格', 18, 4.5, 14, 5), ('第三格', 2, 10.5, 14, 5), ('第四格', 18, 10.5, 14, 5)]),
        ('字词与概念', [('字词一', 2, 5, 9, 9), ('字词二', 12.5, 5, 9, 9), ('字词三', 23, 5, 9, 9)]),
        ('操作步骤', [('选择材料', 2, 5, 9, 7), ('表达想法', 12.5, 6, 9, 7), ('判断修改', 23, 7, 9, 7)]),
        ('作品检查', [('文字与事实', 2, 5, 21, 3), ('图文对应', 2, 9, 21, 3), ('自己的选择', 2, 13, 21, 3)]),
        ('展示与复盘', [('作品位置', 2, 5, 18, 10), ('我做了什么', 22, 5, 10, 3), ('我修改了什么', 22, 9, 10, 3), ('为什么这样改', 22, 13, 10, 3)]),
    ]
    colors = ['A6DAF7', 'FFD369', 'B6E7A9', 'FF9A86', 'DCC8F5']
    commands = []
    for i, (title, blocks) in enumerate(layouts, 1):
        commands.append({'command': 'add', 'parent': '/', 'type': 'slide', 'props': {'layout': 'blank', 'background': 'FFF6E5'}})
        parts = [(title, 2, 1.2, 29, 2, None)] + [(text, x, y, w, h, colors[j % len(colors)]) for j, (text, x, y, w, h) in enumerate(blocks)]
        for j, (text, x, y, w, h, fill) in enumerate(parts):
            props = {'name': f'content-{i}-{j}', 'text': text, 'x': f'{x}cm', 'y': f'{y}cm', 'width': f'{w}cm', 'height': f'{h}cm', 'font': 'Microsoft YaHei', 'size': '30' if j == 0 else '23', 'color': '282522', 'bold': 'true' if j == 0 else 'false'}
            if fill:
                props.update({'preset': 'roundRect', 'fill': fill, 'line': '282522', 'valign': 'middle', 'align': 'center'})
            commands.append({'command': 'add', 'parent': f'/slide[{i}]', 'type': 'shape', 'props': props})
    subprocess.run([cli, 'batch', str(output)], input=json.dumps(commands, ensure_ascii=False), text=True, encoding='utf-8', check=True)
    subprocess.run([cli, 'save', str(output)], check=True)
    subprocess.run([cli, 'validate', str(output)], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    build(parser.parse_args().output)
