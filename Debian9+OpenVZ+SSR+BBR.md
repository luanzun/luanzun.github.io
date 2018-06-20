OpenVZ 平台安装 Google BBR

    wget https://raw.githubusercontent.com/kuoruan/shell-scripts/master/ovz-bbr/ovz-bbr-installer.sh
    chmod +x ovz-bbr-installer.sh
    ./ovz-bbr-installer.sh

需要注意的是，在有 `firewalld` 的服务器上安装的时候，firewalld 会干扰 iptables 的规则，造成网络不通（现在具体原因未知，谁有解决方案可以提示一下）。所以在装有 firewalld 的服务器上需要先退出 `firewalld`：

    systemctl disable firewalld
    systemctl stop firewalld

如需卸载，请使用：

    ./ovz-bbr-installer.sh uninstall

### 错误说明

有些机器一切正常，但是加速失败。从网友的反馈来看，可能需要将 SS 的监听地址从 vps IP 改到 127.0.0.1 或者 0.0.0.0，具体未测试，加速失败的朋友可以试一试.

### 多端口加速

安装的时候只配置了一个加速端口，但是你可以配置多端口加速，配置方法非常简单。 修改文件

    # vi /usr/local/haproxy-lkl/etc/port-rules

在文件里添加需要加速的端口，每行一条，可以配置单个端口或者端口范围，以 # 开头的行将被忽略。 例如：8800 或者 8800-8810 配置完成之后，只需要重启 haproxy-lkl 即可。

注： 最初版本的实现是需要再开一个新端口，后来经人提醒，我又看了一下 HAproxy 的配置说明，可以直接代理后端端口，不必再开新端口。请注意，使用该方法后，如果 HAproxy 进程异常退出，会造成无法连接原有端口。所以，请确保在退出 HAproxy 时是通过命令正常退出的，在退出时会自动清理原有的防火墙规则。

使用 systemctl 或者 service 命令来启动、停止和重启 HAporxy-lkl：


    systemctl {start|stop|restart} haproxy-lkl

    service haproxy-lkl {start|stop|restart}

`/usr/local/haproxy-lkl/etc/haproxy.cfg` 这个文件是通过 `port-rules` 自动生成的，每次启动都会重新生成，所以直接修改它的配置没用。 如果想要自定义配置，请修改启动文件：

    /usr/local/haproxy-lkl/sbin/haproxy-lkl

检查一下：

    # ldd --version
    ldd (GNU libc) 2.15
    Copyright (C) 2012 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.

已经升级到 glibc 2.15 了。

### 判断 bbr 是否正常启动

可以尝试 ping 10.0.0.2，如果能通，说明 bbr 已经启动。

然后检查 iptables 规则

    iptables -t nat -nL
    Chain PREROUTING (policy ACCEPT)
    target     prot opt source               destination
    LKL_IN     all  --  0.0.0.0/0            0.0.0.0/0
    
    Chain POSTROUTING (policy ACCEPT)
    target     prot opt source               destination
    
    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination
    
    Chain LKL_IN (1 references)
    target     prot opt source               destination
    DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:8989 to:10.0.0.2

## 查看实时流量
查看实时占用带宽需要安装软件，并登录ssh通过命令方式查看。 安装vnstat命令如下：

    wget downinfo.myhostadmin.net/vnstat-1.10.tar.gz
    tar xzvf vnstat-1.10.tar.gz
    cd vnstat-1.10
    make && make install

用 `ifconfig` 命令查看网卡名称。一般情况下Xen、KVM的VPS都是`eth0` 有多个IP可能还有`eth1`等，OpenVZ的是`venet0`.

### vnstat基本使用命令

    vnstat -i eth0 -l #实时流量情况
    vnstat -i eth0 -h #按小时查询流量情况
    vnstat -i eth0 -d #按天数查询流量情况
    vnstat -i eth0 -m #按月数查询流量情况
    vnstat -i eth0 -w #按周数查询流量情况
    vnstat -i eth0 -t #查询TOP10流量情况

更多命令帮助信息可以 vnstat --help 进行查看。