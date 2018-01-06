在udebian `apt-get upgrade`的时候，遇到：

  E: Could not get lock /var/cache/apt/archives/lock - open (11 Resource temporarily unavailable)
  E: Unable to lock the download directory

解决办法如下：

  sudo rm -rf /var/cache/apt/archives/lock
  sudo apt-get update

然后apt-get就恢复正常了。
