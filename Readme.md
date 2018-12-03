# Nginx + uWSGI + Django
## 三个组件之间的关系
web browser <-> Nginx <-> socket <-> uwsgi <-> wsgi <-> Django
## uWSGI, WSGI, uwsgi
1. WSGI  
WSGI相当于是Web服务器和Python应用程序之间的桥梁。那么这个桥梁是如何工作的呢？首先，我们明确桥梁的作用，WSGI存在的目的有两个：  
- 让Web服务器知道如何调用Python应用程序，并且把用户的请求告诉应用程序。  
- 让Python应用程序知道用户的具体请求是什么，以及如何返回结果给Web服务器。
2. uWSGI
与WSGI一样是一种通信协议，是uWSGI服务器的独占协议，用于定义传输信息的类型(type of information)，每一个uwsgi packet前4byte为传输信息类型的描述，与WSGI协议是两种东西，据说该协议是fcgi协议的10倍快。
3. uwsgi  
是一个web服务器，实现了WSGI协议、uwsgi协议、http协议等。
## 网站地址
网站分为两个版本：
- [xikong.site](http://xikong.site) 是稳定版  
- [dev](http://xikong.site/dev) 是测试版，每当开发新的功能时，在该站点部署
## 工程目录
- 在生产环境中的位置 `/home/xikong/mysite/`
- 在github中的位置 [mysite](https://github.com/AprilKK/mysite,"helloDjango")
```
./
├── Readme.md
├── helloDjango
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── admin.py
│   ├── admin.pyc
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── models.pyc
│   ├── templates
│   │   └── home.html
│   ├── tests.py
│   ├── views.py
│   └── views.pyc
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── media
│   │   └── media.png
│   ├── settings.py
│   ├── settings.pyc
│   ├── static
│   ├── urls.py
│   ├── urls.pyc
│   ├── wsgi.py
│   └── wsgi.pyc
├── mysite_nginx.conf
├── mysite_uwsgi.ini
├── test.py
├── uwsgi.log
└── uwsgi_params
```
### 配置文件
- `mysite_nginx.conf` 是Nginx的配置文件，需要将这个文件链接到`/etc/nginx/sites-enbaled`, 这样nginx就可以看到这个配置文件了
```
sudo ln -s /home/xikong/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/
```
- `uwsgi_params` 这个文件在 `mysite_nginx.conf` 中引用，目的是nginx和uwsgi server 进行链接
- `mysite_uwsgi.ini` 是uwsgi server 的配置文件， 单次运行，可以用下面的命令
```
uwsgi --ini mysite_uwsgi.ini
```
## 配置Nginx
### 安装
``` 
sudo apt-get install nginx
sudo /etc/init.d/nginx start    # start nginx
```
### 配置静态文件
在运行nginx之前，你必须收集所有的Django静态文件到静态文件夹里。首先，必须编辑mysite/settings.py，添加:
```
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```
然后运行
```
python manage.py collectstatic
```
### Nginx 控制命令
- 重启 `sudo /etc/init.d/nginx restart`
- 重新加载配置文件 `sudo nginx -s reload`

## uWSGI 
### Emperor Model
uWSGI可以运行在’emperor’模式。在这种模式下，它会监控uWSGI配置文件目录，然后为每个它找到的配置文件生成实例 (‘vassals’)。每当修改了一个配置文件，emperor将会自动重启 vassal.

```
# create a directory for the vassals
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /path/to/your/mysite/mysite_uwsgi.ini /etc/uwsgi/vassals/
# run the emperor
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
```
然后使用下面的命令来运行uWSGI server
```
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
```
### 系统启动自动运行
在`/etc/init/`目录中添加配置文件`uwsgi.conf`:
```
# Emperor uWSGI script

description "uWSGI Emperor"
start on runlevel [2345]
stop on runlevel [06]

respawn
exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
```
## Django
### 代码仓库
- 在生产环境中的位置 `/home/xikong/mysite/`
- 在github中的位置 [mysite](https://github.com/AprilKK/mysite,"helloDjango")
### 代码逻辑
- helloDjango 是项目的主要代码，里面的`views.py` 是定义view的地方
- templates 文件夹是放置template的位置，这个位置要在`mysite/settings.py`中指出，告诉django去哪里寻找template