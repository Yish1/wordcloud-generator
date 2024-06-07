<div align="center">
	<a><img src="https://s2.loli.net/2024/06/07/VKlp2amoNB35FiJ.png" width="180" height="180" alt="wordcloud-generator"></a>
</div>
<div align="center">

# Wordcloud-Generator
_一个通过读取输入的网址的内容 或自定义的文本 生成词云的小工具_  
_A small tool that generates a word cloud by reading the content of a given URL or custom text._

</div>
## 特色
- [x] 自定义字体
- [x] 自定义图形
- [x] 自定义文字
- [x] 多语言支持
- [x] 网站抓取
- [ ] msn和百度系的网页暂时无法抓取，请使用自定义文本模式

## 使用方式
1.安装依赖库
```shell
pip install -i requirement.txt
```
2.开袋即食

## 打包
```shell
nuitka --standalone --lto=no --clang --msvc=latest --disable-ccache --windows-uac-admin --windows-disable-console --enable-plugin=pyqt5,upx --upx-binary=E:\ctest\o\upx\upx.exe --output-dir=o --windows-icon-from-ico=wc.ico demo.py
```
其中--clang --msvc=latest需要安装vs studio，可替换为--mingw64
upx为可选项 --upx-binary=E:\ctest\o\upx\upx.exe(替换成实际地址)
upx压缩可以大幅减少打包体积

打包完后需要将py目录下的pyqt5里的qt-plugins替换打包目录里的，因为upx压完这个后似乎损坏了
wordcloud目录下也缺少了一个文件，打包完要自行放入

首次打包建议取消--windows-disable-console以便查看报错
