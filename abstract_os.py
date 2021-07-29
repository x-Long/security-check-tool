from typing import Iterable


class AbstractOS:
    # 不要等获取完所有信息后返回list，而每获取到一条记录就使用 yield 返回它
    # 1.1 文件访问记录
    def get_file_access_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 1.2 已删除文件记录
    def get_deleted_files_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 2.1 USB存储设备插拔记录
    def get_usb_storage_device_using_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 2.2 手机插拔痕迹
    def get_cell_phone_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 2.3 外接设备检查
    def get_all_usb_device_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.1 检查是否安装主流杀软
    def get_installed_anti_virus_software_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.2 列举本地已安装的所有软件
    def get_installed_software_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.3 列举电脑上安装的所有服务
    def get_services_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.4 当前网络情况
    def get_current_network_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.5 系统日志
    def get_system_logs_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.6 获取开机历史记录
    def get_power_of_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.7 读取系统共享目录设置
    def get_sharing_settings_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.8 系统策略检查，目前只需要检查是否配置了开机自动登录
    def get_strategy_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.9 本机所有用户组情况
    def get_users_groups_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.10 本机所有硬件信息
    def get_hardware_records(self) -> Iterable[dict]:
        raise NotImplementedError()

    # 3.11 本机安装的所有驱动
    def get_system_drives_records(self) -> Iterable[dict]:
        raise NotImplementedError()

