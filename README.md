# 配置文件管理

生成并管理yaml格式文件的配置文件管理器

## 基类

- BaseFileManager

基础的配置文件管理器类。

配备配置文件的读写功能，会对路径更改及文件名更改进行检测。

可通过get_cwdPath静态方法返回该文件的前两级目录作为根目录。

可进一步重写run函数以实现程序运行期间的文件管理功能。

- BaseManagerUI

配置文件管理器实例的用户交互容器类。

对配置文件管理器实例的输入指令进行检测，并在run函数中实现指令控制流的管理，最终传递对应指令至具体的配置文件管理器实例。

默认的指令集包括以下六项：读取、更新、新增、删除、重命名、清空。['READ', 'UPDATE', 'DELETE', 'RENAME', 'ADD', 'CLEAR']

使用时根据实际需求重写run函数以及对应_code_function函数。

## 使用样例

详见bin文件夹下的 template.py 以及 src\manager\ConfManager.py 文件。

构造conf实例，可读取conf实例的conf_dict属性获取当前根目录下settings.py的配置内容
