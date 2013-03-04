# 介绍

这个脚本可以用来对邮件服务进行压力测试，支持的协议是SMTP与IMAP。模拟多
个用户同时登入服务器进行查询收件箱、收发邮件等操作，通过这种方式试图找
到邮件服务能够承受的最大负载。使用本脚本进行测试的人员通过编辑配置文件
的方式来调整对邮件服务器的压力，进而找到邮件服务器的极限服务能力。

该脚本使用的编程语言是python 2.7，需要在命令行环境下运行，也就是说要想运行
这个脚本，你需要使用Linux, Unix, Cygwin中的一种，并且你的操作系统需要
支持多线程工作（如果不确定，请使用Linux或Unix），需要安装 threading,
ConfigParser, smtplib, imaplib, email 这几个python的库，以支持脚本的顺
利运行。
- - - - - -

# 结构与工作原理

这个脚本的结构与原理很简单，整个脚本由配置文件mail.conf与mailtest.py,
send.py, fetch.py三个模块组成，其中mailtest.py是主模块，是整个脚本的入
口，用户在命令行下使用python执行该文件即可启动脚本对需要测试的邮件服务
器进行压力测试:
```
cd /path/to/the/script
python mailtest.py
```
send.py与fetch.py分别负责通过邮件服务器发送邮件与下载邮件。

当脚本启动之后，首先从配置文件mail.conf中获取脚本执行过程中需要的数据
与参数，随后通过操作系统的API函数`os.fork()`创建子进程，子进程负责发送
邮件，父进程负责下载邮件。

每个进程从配置文件中获取需要创建的线程数以及用户名与密码以及邮件服务器
的域名等信息，根据配置文件中的信息创建规定数量的线程，每个线程使用不同
的帐户登陆到邮件服务器进行收发邮件的操作。隔多长时间连接服务器进行操作、
每次登陆服务器收发多少邮件都可以通过编辑配置文件进行调整，所有工作完成
之后程序打印出本次测试的统计结果退出，一次测试结束。
- - - - - -

# 实现细节

本脚本需要被测试邮件服务器提供一组有规律的帐户，这些帐户必须全部使用同
样的密码，账户名须以数字结尾，比如test1, test2,  ... test100等,
每个线程使用一个帐户登陆服务器进行操作。下面以send.py模块为例讲一下脚
本的实现细节。

当send.py被调用时，程序首先从配置文件中获取所需信息并将其保存在全局变
量中，然后生成需要发送的邮件内容，同样保存在全局变量msg中，类SendMail
继承自类threading的子类Thread，该子类中的__init__与run两个函数是我们需
要覆盖的，前者进行初始化的工作，后者在创建SendMail对象之后，当调用对象
中的函数start时，会自动执行函数run，所以我们可以把需要执行的动作放在函
数run里面进而让脚本执行我们希望做的事情，在这个例子中，函数run根据从配
置文件中获取的线程数n，循环n次执行登陆服务器发送邮件的操作。

send.py模块主要使用了smtplib与threading这两个库，用于解析配置文件的库
ConfigParser与用于生成和解析邮件内容的库email的使用相当简单，smtplib与
threading的使用可以参考官方文档：

[threading — Higher-level threading interface][threading]

[smtplib — SMTP protocol client][smtplib]

[threading]: http://docs.python.org/2/library/threading.html#module-threading
[smtplib]: http://docs.python.org/2/library/smtplib.html

fetch.py模块的实现与send.py基本差不多，使用的库是imaplib，具体的使用方
法可以参考官方文档：

[imaplib — IMAP4 protocol client][imaplib]
[imaplib]: http://docs.python.org/2/library/imaplib.html
