��    1      �  C   ,      8  �   9  !      $   "     G     N     d     ~  !   �     �  (   �      �     
  #     �  D     
     /
  C   6
     z
  &   �
  �  �
  <   ?  &   |     �     �  *   �     �     	  �        �  3   �     �                '     .  E   D  +   �  1   �     �     �          	  '        G  3   f     �     �     �  *  �  �   �  #   �  #     
   '     2     M     g  :   w     �  '   �  &   �       �   "  �  �     f     x  D   }     �  4   �  �    C   !      K!     l!     u!  0   �!     �!     �!  �   �!     �"  ?   �"     �"     �"     #     #     $#  C   0#  5   t#  5   �#     �#     �#     �#     $  '   &$      N$  E   o$     �$     �$     �$                                            ,   (   -           0      
   +          #   .         "   )             /          &                  !                                 %   1         '                   *             $   	       


欢迎使用网页词云生成器！
在上方文本框中输入需要分析的网址
(需要输入http://或https://协议头)，

点击开始按钮，稍后即可在右栏中查看词云。


 使用自定义文字生成词云 使用自定义文本生成词云图 保存 保存api随机图片 保存url文本出错: %s 保存词云图 修改语言后重启程序生效 关于此工具 图片文件 (*.png *.jpg *.jpeg *.webp) 尝试在此页面使用%s编码 开始生成词云图 您选择了%s作为词云图形状

Tips: 尽可能选择分辨率较高且背景为白色的图片，所选图片分辨率即为词云图分辨率！

正常情况下，您应该可以在右栏看到选择的图片，如果没有正常显示，则图片无法读取，尝试更换图片！ 感谢您使用网页词云生成器！

这是一个作为Py课设的小工具，使用Pyqt5搭建ui，request、bs4和jieba分析网页内容，再使用wordcloud生成词云。

除此之外，还第一次尝试了多线程等性能优化方式，使用Qthread遇到了不少麻烦，比如无法结束线程，内存泄漏等，后面换用线程池(可以自动结束线程)解决了。

不过即便是这样一个小程序，也依旧还有许多的不足（比如MSN和百度系列的网站无法分析），也有许多尚未实现的想法。此工具将会开源，以及在沉梦小站中分享一些遇到的问题及解决方法。

作者：Yish_

版本：%s

注：此工具调用了沉梦小站的随机图api 找到字体%s, %s 提示 无法找到此字体的实际地址
请尝试更换其他字体！ 无法设置字体 暂不支持Windows7及以下系统！ 未行之路:
                                    在你消失的夜里穿行 
                                    微风送来最后一封信 
                                    通篇找寻沉默的音讯 
                                    谜底也许  不期而遇 
                                    
                                    悲欢离合是旅行的考卷 
                                    明月下想象另一轮明月 
                                    假如某刻你我再次相见 
                                    过往 能否重现 
                                    故事 再向前 
                                    
                                    我从未原地等待 
                                    追赶命运的节拍 
                                    夜幕深如海 而你照亮远方之外 
                                    无论海角天涯 你找到我出发
                                    前路无阻 就算一切崩塌 
                                    
                                    当白雪渐渐消融 
                                    当坚冰显现裂缝 
                                    而你是否已经扬帆启航 乘着风 
                                    无论海角天涯 我找到你出发
                                    我们从未迷路 
                                    我们终将重逢 来自沉梦小站的随机图API图片 (*.png *.jpg *.webp) 来自网页词云生成工具 (*.png) 标题:  此页面使用%s编码 没有在此页面获取到有效信息！ 生成词云图出错: %s 确定 网站SSL证书不存在或者失效，可能导致无法访问或者使您的设备遭受攻击。
若仍要继续访问，请去除链接'https'中的's'。 网站简介: 网页无法访问，请检查链接是否正确！ 网页词云生成器 网页词云生成器 %s 警告 设置 词云图生成完毕 词云图装载中...
(正在生成词云图，卡顿是正常现象) 词云图装载中...
正在分析文本... 词云图装载中...
正在尝试访问网站... 词云字体 词云形状 语言 请先选择字体！ 请输入可访问的网址！！！
%s 请输入有效内容！！！ 请选择一个用于生成词云图的字体！
%s 选择图片文件 选择语言 错误 Project-Id-Version: 英语
PO-Revision-Date: 2024-06-20 00:35+0800
Last-Translator: 
Language-Team: cmxz
Language: en_US
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
X-Generator: Poedit 3.4.4
X-Poedit-SourceCharset: UTF-8
 


Welcome to the Web Word Cloud Generator!
Enter the URL you want to analyze in the text box above (make sure to include 'http://' or 'https://' protocol),

Click the start button, and you will soon see the word cloud in the right column.


 Generate Wordcloud with Custom Text Generate Wordcloud with Custom Text Save image Save random image from api Error saving url text: %s Save word cloud Modify the language and restart the program to take effect About this tool Image files (*.png *.jpg *.jpeg *.webp) Trying to use %s encoding on this page Start Generating You have selected %s as the word cloud shape.

Tips: Choose a high-resolution image with a white background. The resolution of the selected image will be the resolution of the word cloud ! Thank you for using the Web Wordcloud Generator!

This is a small tool created as a Python course project. It uses PyQt5 for the UI, requests, BeautifulSoup (bs4), and Jieba for web content analysis, and generates word clouds with wordcloud.

Additionally, it was my first attempt at performance optimization with multithreading. Using QThread caused some issues like being unable to terminate threads and memory leaks, which were resolved by switching to a thread pool (which can automatically terminate threads).

However, even with this small program, there are still many shortcomings (such as the inability to analyze MSN and Baidu series websites) and many ideas that have yet to be implemented. This tool will be open-sourced, and I will share some encountered issues and solutions on Deep Dream  Blog.

Author: Yish_

Version: %s

Note: This tool uses the random image API from Deep Dream  Blog Find fonts %s, %s Tips Cannot find the actual address of this font
Please try another font! Unable to set fonts Windows 7 and below are not supported at this time ! 未行之路:
                        Traveling in the nights you've left me in.
                        Even nowhere I can find you out,
                        The answer is not far off now.
                        
                        This journey of ours has been bittersweet.
                        Close my eyes wondering what you would have dreamed.
                        If you were here standing next to me,
                        Would you know how I feel,
                        And see what I see?
                        
                        Know that I'll always try.
                        Finding your rhythm and rhyme.
                        Though the nights are long and dark, I‘ll see you shining bright.
                        And no matter where you are, you've come with me this far.
                        Showing the way when all else falls apart.
                        
                        When the snow all melts away,
                        And the ice finally breaks.
                        Have you taken off, are you already on your way?
                        No matter where you are, I've come with you this far.
                        I’m never really lost.
                        Our paths will surely cross. Random image API pictures from Deep Dream Blog (*.png *.jpg *.webp) From Wordcloud Generator (*.png) Title :  This page uses %s encoding No valid information was obtained on this page ! Error generating word cloud: %s OK A non-existent or invalid website SSL certificate may prevent access or expose your device to attack.
To continue access, please remove the 's' from the link 'https' Website Introduction : The page is inaccessible, please check if the link is correct ! Web Wordcloud Generator Web Wordcloud Generator %s Warning Setting Completed ! Word cloud is loading...
(Generating word cloud, lagging is normal) Word cloud is loading...
Trying to access the site... Word cloud is loading...
Trying to access the site... Wordcloud Font Wordcloud Shape Language Please select the font first! Please enter an accessible URL ! ! !
%s Please enter valid content ! ! ! Please select a font that will be used to generate the word cloud!
%s Selecting an image file Choose language Error 