import json
import os
import shutil
import subprocess
import zipfile

import requests


# 读取配置文件
def read_config():
    with open('./upload_config.json', 'r') as f:
        try:
            return json.loads(f.read())
        except Exception as e:
            print('配置文件有问题！')
            raise e


# 打包编译代码
def pack_source(build_shell):
    if build_shell is None:
        print('打包脚本为空')
    else:
        print('打包中...')
        subprocess.call(build_shell, shell=True)


# 压缩文件夹为zip
def zip_dir(startdir, file_news):
    # 判断文件夹是否存在
    if not os.path.isdir(startdir):
        print('上传的文件夹不存在或者不是文件夹')
        return

    zip = zipfile.ZipFile(file_news, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(startdir):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(startdir, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    print('压缩成功，文件名：%s' % file_news)


# 删除压缩包
def delete_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
        print('删除%s成功' % file_name)


# 删除文件夹
def delete_dirs(dirs):
    print('删除打包文件夹...')
    # 递归删除文件夹
    if os.path.isdir(dirs):
        shutil.rmtree(dirs)
        print('删除%s成功' % dirs)
    else:
        print('删除打包文件夹失败...')


def upload(other_post_data, upload_url, file_path):
    if not os.path.isfile(file_path) or not file_path.endswith('.zip'):
        print('没有%s，或者后缀不为.zip' % file_path)
        return

    if not upload_url:
        print('没有指定上传链接')
        return

    files = {'file': open(file_path, 'rb')}

    r = requests.post(upload_url, files=files, data=other_post_data)
    print('返回数据：%s' % r.json())


if __name__ == '__main__':
    config = read_config()
    # print(config)
    # 获取配置文件信息

    # 文件外其他上传的参数
    other_post_data = config['otherPostData']
    # 上传接口
    upload_url = config['uploadUrl']
    # 上传的文件夹
    upload_path = config['uploadPath']
    # 压缩后的名字
    zip_name = config['zipName'] + '.zip'
    # 打包命令
    build_shell = config['buildShell']

    # 删除文件夹
    delete_dirs(upload_path)

    # 打包
    pack_source(build_shell)

    # 压缩文件夹
    zip_dir(upload_path, zip_name)

    # 上传文件
    upload(other_post_data, upload_url, zip_name)

    # 删除压缩文件
    delete_file(zip_name)

    # 暂停
    os.system("pause")
