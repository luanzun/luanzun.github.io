更新软件列表
    apt-get update

更新软件

    apt-get upgrade

更新系统版本

    apt-get dist-upgrade

更新backsports源

    apt-get -t wheezy-backports upgrade

安装`aptitude`

    apt-get install aptitude

查找最新内核

    aptitude search linux-image

安装内核

    apt-get -t wheezy-backports install linux-image-3.2.0-4-amd64

查看系统中已安装的内核

    dpkg --get-selections |grep linux-image

卸载内核

    apt-get remove linux-image-3.16.0-0.bpo.4-amd64

