# -*- coding: UTF-8 -*-
import os
import sys
from typing import List, Tuple
import av
import pilk

DEBUG = False


# noinspection PyUnresolvedReferences
def to_pcm(in_path: str) -> Tuple[str, int]:
    """任意媒体文件转pcm"""
    out_path = os.path.splitext(in_path)[0] + '.pcm'
    with av.open(in_path) as in_container:
        in_stream = in_container.streams.audio[0]
        sample_rate = in_stream.codec_context.sample_rate
        if sample_rate not in [8000, 12000, 16000, 24000, 32000, 44100, 48000]:
            sample_rate = 24000
        with av.open(out_path, 'w', 's16le') as out_container:
            out_stream = out_container.add_stream(
                'pcm_s16le',
                rate=sample_rate,
                layout='mono'
            )
            try:
                for frame in in_container.decode(in_stream):
                    frame.pts = None
                    for packet in out_stream.encode(frame):
                        out_container.mux(packet)
            except:
                pass
    return out_path, sample_rate


def convert_to_silk(media_path: str, output_path) -> str:
    """任意媒体文件转为 silk, 返回silk路径"""
    pcm_path, sample_rate = to_pcm(media_path)
    silk_path = os.path.splitext(pcm_path)[0] + '.silk'
    pilk.encode(pcm_path, output_path, pcm_rate=sample_rate, tencent=True)
    if not DEBUG:
        os.remove(pcm_path)
    return silk_path


def get_parent_directory_name(file_path):
    # 使用 os.path.dirname 获取文件所在目录，然后使用 os.path.basename 获取文件夹名
    parent_directory_name = os.path.basename(os.path.dirname(file_path))

    return parent_directory_name



def traverse_directory(path):
    # 列出当前目录下的所有文件和文件夹
    items = os.listdir(path)
    if not os.path.isdir("silk"):
        os.mkdir("silk")
    for item in items:
        try:
            # 获取文件或文件夹的完整路径
            item_path = os.path.join(path, item)

            if os.path.isfile(item_path):
                # 如果是文件，则打印文件路径
                print("File:", item_path)
                parent_directory = get_parent_directory_name(item_path)
                if not os.path.isdir("silk//" + parent_directory):
                    os.mkdir("silk//" + parent_directory)
                print(parent_directory)
                file_name = item_path.split("\\")[-1]
                file_name = file_name.split(".")[0] + ".silk"
                output_path = "silk//" + parent_directory + "//" + file_name
                convert_to_silk(item_path, output_path)
            elif os.path.isdir(item_path):
                # 如果是文件夹，则递归遍历
                print("Directory:", item_path)
                traverse_directory(item_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    path = input("请输入你的需要转silk的文件目录：")
    traverse_directory(path)
