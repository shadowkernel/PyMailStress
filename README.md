PyMailStress用户手册

# 快速入门

获取源代码：
git clone https://github.com/shadowkernel/PyMailStress

添加需要进行压力测试的邮箱的用户名和密码（以GMAIL服务器为例）：修改 userdb.txt
user1, pass1
user2, pass2

对GMAIL服务器进行压力测试：
./PyMailStress.py -c gmail-tls.conf -u userdb.txt  -m smtp2-imap-1hr.conf
其中，
gmail-tls.conf表示使用gmail的邮件服务器（TLS认证），
userdb.txt为测试用的用户名密码文件，
smtp2-imap-1hr.conf为压力测试模型（2线程的SMTP， 测试1小时）。

查看log：
cat gmail-2users.log

# 使用方法
./PyMailStress.py -h
