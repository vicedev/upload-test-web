## 介绍

用于打包上传网页到服务器，基于python3开发

## 使用 

##### upload_config.json：	

~~~
{
  "uploadUrl": "http://test/fileUpload", //上传地址
  "otherPostData": {	                 //除文件外其他的一些post参数
    "type": "post",
    "dataType": "json"
  },
  "uploadPath": "./dist",                //需要上传的文件夹路径
  "zipName": "uploadTest",               //压缩uploadPath后的文件名字，程序内部压缩为.zip文件
  "buildShell": "npm run build"          //打包命令
}
~~~

##### 使用

windows：

将upload.exe和upload_config.json拷贝到项目中，修改upload_config.json，双击upload.exe。

linux/mac：

将upload.py和upload_config.json拷贝到项目中，修改upload_config.json，执行python upload.py。

##### 源码修改生成可执行文件

~~~shell
pyinstaller -F -c upload.py
~~~

