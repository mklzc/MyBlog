本项目是基于 django 编写的博客。

[示例网站](https://blog.asyncerror.top)

## Features

1. 支持 Markdown 和 Latex 渲染
2. 支持评论，用户注册，文章管理等基本功能

## 部署指南（Mysql + Waitress + Caddy）

### 项目依赖

本项目的 requirements.txt 由 `pip freeze > requirements.txt` 命令生成，并不完全准确。

```
pip install -r requirements.txt
```

### 数据库配置

在服务器上创建一个叫 Mysql 数据库，然后在项目的根目录下创建 `.env` 文件

```text
DEBUG=on

SECRET_KEY=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USER=
```

其中 `GITHUB_CLIENT_ID` 和 `GITHUB_CLIENT_SECRET` 为实现 Github 第三方登录所需内容。

在 https://github.com/settings/developers 生成你的 Oauth App 即可获得以上的值。

### Caddy + Waitress

`Caddyfile` 参考

其中 `path/to/static` 是项目的 `app/static` 目录在服务器中的绝对路径

`path/to/media` 是项目的 `app/media` 目录在服务器中的绝对路径

```
domain.com {
    reverse_proxy localhost:8000
    handle_path /static/* {
        root * path/to/static
        file_server
    }
    handle_path /media/* {
        root * path/to/media
        file_server
    }
}
```

然后运行 
```
caddy run
python run.py
```

### 注册服务

Windows 下可以使用 nssm 注册 caddy 和 run.py 为服务，Linux 使用 systemctl 即可。

## TODO

1. &#x2705; 文章分类 2024-12-10
2. &#x2705; 支持文章搜索 2024-12-12
3. &#x2705; GitHub第三方登录
4. &#9744; 文章标签