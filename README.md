# 主机信息获取-需求描述

## 项目描述

本项目旨在打造一个计算机终端保密检查工具,提供一种方式，可以很方便的展示出当前系统的全面信息

类似管家类软件，获取系统软硬件信息，usb插拔记录、文件访问记录、硬盘、系统日志 等等

本项目是一个GUI软件的功能子集,这些数据将在GUI软件中的列表呈现。

**商业原因限制，仅开放windows端部分接口。**

## 环境描述

- 开发语言 python >= 3.6
- 操作系统 windows/linux/macos
- 支持系统版本
    - windows 7/8/10
    - linux 为 国产操作系统uos20 、银河麒麟V10（x86、mips64）

## 一、文件检查

### 1. 文件访问记录

- 数据示例 
```json
[
  {
    "username":"albert",
    "access_time": "2020-10-22 08:12",
    "file_path": "D:\entertainment\music\I miss you.mp3",
    "is_exists": false
  }
  ...
]
```

### 2. 已删除文件记录
> 读取已删除到回收站里的文件信息
```json
[
    {
        "filepath":"C:\Users\god\pop.mp3",
        "create_time": "2020-07-06 16:46:00",
        "modify_time": "2020-07-29 17:21:22"
    }
    ...
]
```

## 二、痕迹检查

### 1. USB存储设备插拔记录 
- 数据示例 
```json
[
    {
        "device_name": "KingSoft USB 2.0",
      	"serilas": "241300000293",
        "manufacture": "Samsung",
        "description": "USB 2.0 Flash Driveß",
        "last_plugin_time": "2020-10-22 08:10"
    }
    ...
]
```
### 2. 手机插拔痕迹
```json
[
    {
        "device_name": "KingSoft USB 2.0",
        "manufacture": "Samsung",
        "storage": "16 GB",
        "last_plugin_time": "2020-10-22 08:10"
    }
    ...
]
```

### 3. 外接设备检查
> 枚举所有通过USB接口连接过此电脑的外设，不局限于鼠标、键盘、打印机等
```json
[
    {
        "name": "打印机",
        "manufacture": "惠普",
        "description": ""
    },
    {
        "name": "物理光驱",
        "manufacture": "标准 CD-ROM 驱动器",
        "description": "NECVMWar Vmware SATA CD01 ATA Device"
    }
    ...
]
```

## 三、系统检查

### 1.杀毒防护软件
> 检查是否安装主流杀软

```json
{
    "name": "360杀毒",
    "version": "20.1.2.3",
    "install_path": "C:\Program Files\360",
}
```

### 2. 已安装软件

> 列举本地已安装的所有软件

```json
[
    {
        "name": "Google Chrome",
        "version": "86.0.4240.111",
        "install_date": "2020-10-23",
        "publisher": "Google LLC",
        "install_path": "C:\Program Files\Google\Chrome\Application"
    }
    ...
]
```

### 3. 服务信息

> 列举电脑上安装的所有服务

```json
[
    {
        "name":"AeLookupSvc",
        "display_name":"Application Experience",
        "start_type": "auto",
        "process_id": 857,
        "is_signed": true,
        "is_system_service": true,
        "file_path": "C:\Program Files\Service\AeLookupSvc.exe",
        "status": "running" [stopped]
    }
]
```

### 4. 网络状态信息

> 展示当前网络情况

```json
[
    {
        "protocol": "tcp",
        "local_port": 8082,
        "process_name": "360se.exe",
        "local_ip": "127.0.0.1",
        "remote_ip": "0", # 本地监听程序远程ip默认为0
        "remote_port": 0, # 本地监听程序远程端口默认为空
        "status": "listen" # ["listen", "established", "timeout"]
        "program_path": "C:\users\albert\appdata\roaming\360se6\application\360se.exe",
        "pid": 1256
    }
    ...
]
```

### 5. 系统日志

> 读取系统日志

```json
[
    {
        "log_type": "系统日志", 
        "time": "2020-10-24 09:46:38",
        "event": 7036,
        "log_source": "Service Control Manager", [COM+, Desktop Window Manager, ESENT, EventLog, EventSystem ...]
        "description": "Multimedia Class Scheduler 正在运行", 
        "computer_name": "Albert-PC",
        "log_kind": "error" #[ Unknown, error, warning, info]
    },
    {
        "log_type": "应用程序日志",
        "time": "2020-10-07 18:10:52",
        "event": 903,
        "log_source": "Software Protection Platform",
        "description": "Multimedia Class Scheduler 正在运行", 
        "computer_name": "Albert-PC",
        "log_kind": "info" 
    },
    ...
]
```

### 6. 开关机日志

```json
[
    {
        "time": "2020-10-07 17:48:32",
        "event": "power on",
        "user": "Albert"
    }
    ...
]
```

### 7. 共享设置信息

> 读取系统共享目录设置

```json
[
    {
        "name": "C$",
        "path": "C:\\",
        "description": "默认共享",
        "connections_count": 0,
    }
    ...
]
```

### 8. 策略检查

> 检查系统策略是否满足要求

1. 是否配置了开机自动登录

### 9. 用户组信息

> 显示本机所有用户情况

```json
[
    {
        "group_name": "administrators",
        "description": "管理员对计算机/域有不受限制的完全访问权",
        "members":["Adminisstrator", "Albert"]  
    },
    {
        "group_name":"users",
        "description": "放置用户进行有意或无意的系统范围的修改, 但是可以运行大部分应用程序",
        "members": ["INTERACTIVE", "Authenticated Users"]
    },
    {
        "group_name":"usiis_iusrsers",
        "description": "internet 信息服务使用的内置组",
        "members": ["IIUSR"]  
    }
    ...
]
```


### 10. 硬件信息

> 显示本机所有硬件信息

```json
[
    {
        "kind": "IDE ATA/ATAPI 控制器", 
        "info": ""
    },
    {
        "kind": "CPU 处理器", 
        "info": "Inter(R) Core(TM) i7-5770K CPU @ 3.5GHz"
    },
    {
        "kind": "内存",
        "info": "1023 M"
    }
    ...
]
```


### 11. 系统驱动

> 显示本机安装的所有驱动

```json
[
    {
        "name": "1394ohci",
        "install_time":"2009-07-14",
        "description": "1394 OHCI Compliant Host Controller"     
    }
    ...
]

```
