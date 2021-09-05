# PyProtobufBot

<p align="center">
  <img src="https://pypbbot.kale1d0.space/assets/logo_large.png" width="200">
</p>
<div align="center">
Pypbbot：一个高效、跨平台、可扩展的<a href="https://github.com/PHIKN1GHT/pypbbot">开源</a> Python QQ 机器人服务端框架（基于 <a href="https://github.com/ProtobufBot/onebot_idl">
  ProtobufBot</a> 协议）。<br/>
<a href="https://pypbbot.kale1d0.space/"><b>文档主页</b></a><br/>
注意，本项目仍处于<b>早期开发阶段</b>，暂不适合用于生产环境。
</div>

当前版本：0.4a6

# 如何使用

首先，运行 `pip install --upgrade pypbbot` 以安装本项目或更新至最新版本。

## 普通用户

在工作目录内（一般是`plugins`文件夹所在的目录）执行`pypbbot`即可启动插件服务器。

```cmd
使用方法: pypbbot [选项]

选项列表:
  --host TEXT             服务器地址  [默认值: localhost]
  --port INTEGER          服务器端口  [默认值: 8080]
  --plugin_path TEXT      插件文件夹  [默认值: plugins]
  --reload / --no-reload  是否启用热重载（插件更新时立刻重启服务，建议仅调试时启用）  [默认值: no-reload]
```

## 插件开发者

### 类驱动模式

如果仅需要编写一些简单的逻辑，可直接导入该库，按照文档内容编写机器人程序后直接运行即可。

样例程序源代码： [simple_class_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/pypbbot_examples/simple_class_driver.py)

（可在项目根目录下使用 `python -m pypbbot_examples.simple_class_driver` 执行）

### 插件驱动模式

插件开发时建议启动热重载。其余选项同普通用户，见上。

`pypbbot --reload`

# 里程碑

- [x] 类驱动器
- [x] 测试组件
- [x] 插件化
- [x] 事务处理
- [x] 命令行工具：服务启动
- [ ] 命令行工具：插件安装
