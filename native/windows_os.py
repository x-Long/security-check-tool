import os
import sys
import win32com.client 
import datetime
import getpass
import winshell as ws
from typing import Iterable
from abstract_os import AbstractOS
from winreg import *
import datetime
import wmi

class WindowsNative(AbstractOS):
    def get_file_access_records(self) -> Iterable[dict]:

        direction = os.environ.get(
            "USERPROFILE")+'\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\'
        file_lists = os.listdir(direction)
        for i in range(len(file_lists)):
            record = {}
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(direction+file_lists[i])
                record["username"] = direction.split("\\")[2]
                record["access_time"] = str(datetime.datetime.utcfromtimestamp(
                    int(os.path.getatime(direction+file_lists[i]))))
                record["file_path"] = shortcut.Targetpath
                if os.path.exists(shortcut.Targetpath):
                    record["is_exists"] = True
                else:
                    record["is_exists"] = False

                yield record
            except:
                pass

    def get_deleted_files_records(self) -> Iterable[dict]:

        records=list(ws.recycle_bin())

        if len(records)==0:
            return "Empty Recycle Bin"
        for i in range(len(records)):
            record={}

            record["filepath"]=str(records[i].original_filename())
            try:
                record["create_time"]=str(records[i].getctime())[:-13]
                record["modify_time"]=str(records[i].getmtime())[:-13]
            except Exception:
                record["create_time"]=str(records[i].recycle_date())[:-6]
                record["modify_time"]=str(records[i].recycle_date())[:-6]

            yield record

    def get_usb_storage_device_using_records(self):

        timestamp = (datetime.datetime(1600, 1, 1) -
                    datetime.datetime(1970, 1, 1)).total_seconds()
        regRoot = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        subDir = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
        keyHandle = OpenKey(regRoot, subDir)
        count = QueryInfoKey(keyHandle)[0]

        for i in range(count):

            subKeyName = EnumKey(keyHandle, i)
            subDir_2 = r'%s\%s' % (subDir, subKeyName)
            keyHandle_2 = OpenKey(regRoot, subDir_2)
            num = QueryInfoKey(keyHandle_2)[0]
            for j in range(num):

                subKeyName_2 = EnumKey(keyHandle_2, j)
                result_path = r'%s\%s' % (subDir_2, subKeyName_2)
                keyHandle_3 = OpenKey(regRoot, result_path)
                numKey = QueryInfoKey(keyHandle_3)[1]
                for k in range(numKey):
                    record = {}
                    name, value, type_ = EnumValue(keyHandle_3, k)
                    if(('Service' in name) and ('disk' in value)):

                        device_name, type_ = QueryValueEx(
                            keyHandle_3, 'FriendlyName')
                        serilas = subKeyName_2
                        manufacture = device_name.split(" ")[0]
                        description, type_ = QueryValueEx(
                            keyHandle_3, 'DeviceDesc')
                        last_plugin_time = str(datetime.datetime.fromtimestamp(
                            int(QueryInfoKey(keyHandle_3)[2]*0.0000001+timestamp)))
                        record["device_name"] = device_name
                        record["serilas"] = serilas[:-2]
                        record["manufacture"] = manufacture
                        record["description"] = str(
                            description.split(";")[1:])[1:-1]
                        record["last_plugin_time"] = last_plugin_time

                        yield record
        CloseKey(keyHandle)
        CloseKey(regRoot)

    def get_cell_phone_records(self) -> Iterable[dict]:

        timestamp = (datetime.datetime(1600, 1, 1) -
                    datetime.datetime(1970, 1, 1)).total_seconds()
        regRoot = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        subDir = r"SYSTEM\CurrentControlSet\Enum\USB"
        keyHandle = OpenKey(regRoot, subDir)
        count = QueryInfoKey(keyHandle)[0]

        for i in range(count):
            subKeyName = EnumKey(keyHandle, i)
            subDir_2 = r'%s\%s' % (subDir, subKeyName)
            keyHandle_2 = OpenKey(regRoot, subDir_2)
            num = QueryInfoKey(keyHandle_2)[0]

            for j in range(num):

                subKeyName_2 = EnumKey(keyHandle_2, j)
                result_path = r'%s\%s' % (subDir_2, subKeyName_2)
                keyHandle_3 = OpenKey(regRoot, result_path)
                numKey = QueryInfoKey(keyHandle_3)[1]
                for k in range(numKey):
                    record = {}
                    name, value, type_ = EnumValue(keyHandle_3, k)
                    # print(name)
                    if(('Service' in name) and ('WUDF' in value)):
                        try:
                            device_name, type_ = QueryValueEx( keyHandle_3, 'FriendlyName')
                            manufacture, type_ = QueryValueEx(keyHandle_3, 'Mfg')
                            storage, type_ = QueryValueEx(keyHandle_3, 'Capabilities')
                            last_plugin_time = str(datetime.datetime.fromtimestamp(int(QueryInfoKey(keyHandle_3)[2]*0.0000001+timestamp)))
                            record["device_name"] = device_name
                            record["manufacture"] = manufacture
                            record["storage"] = str(storage)+"GB"
                            record["last_plugin_time"] = last_plugin_time

                            yield record
                        except:
                            pass

        CloseKey(keyHandle)
        CloseKey(regRoot)

    def get_all_usb_device_records(self) -> Iterable[dict]:

        regRoot = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        subDir = r"SYSTEM\CurrentControlSet\Enum\USB"
        keyHandle = OpenKey(regRoot, subDir)
        count = QueryInfoKey(keyHandle)[0]

        for i in range(count):
            subKeyName = EnumKey(keyHandle, i)
            subDir_2 = r'%s\%s' % (subDir, subKeyName)
            keyHandle_2 = OpenKey(regRoot, subDir_2)
            num = QueryInfoKey(keyHandle_2)[0]
            for j in range(num):
                record={}
                subKeyName_2 = EnumKey(keyHandle_2, j)
                result_path = r'%s\%s' % (subDir_2, subKeyName_2)
                keyHandle_3 = OpenKey(regRoot, result_path)
                numKey = QueryInfoKey(keyHandle_3)[1]
                name, value, type_ = EnumValue(keyHandle_3, 0)
                flag,type_ = QueryValueEx(keyHandle_3,'Service')
                if flag=='USBSTOR':
                    pass
                else:
                    try: 
                        name1,type_ = QueryValueEx(keyHandle_3,'FriendlyName')
                        manufacture,type_ = QueryValueEx(keyHandle_3,'Mfg')
                        description,type_ = QueryValueEx(keyHandle_3,'DeviceDesc') 
                    except:
                        name1,type_ = QueryValueEx(keyHandle_3,'DeviceDesc')
                        manufacture,type_ = QueryValueEx(keyHandle_3,'Mfg')
                        description,type_ = QueryValueEx(keyHandle_3,'DeviceDesc') 
                    record["name"]=name1.split(";")[-1].replace("(","").replace(")","")
                    record["manufacture"]=manufacture.split(";")[-1].replace("(","").replace(")","")
                    record["description"]=description.split(";")[-1].split(";")[-1].replace("(","").replace(")","")
                    record["V_P_ID"]=subKeyName.split(";")[-1]

                    yield record
        CloseKey(keyHandle)
        CloseKey(regRoot)

    def get_installed_anti_virus_software_records(self) -> Iterable[dict]:

        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']

        for i in sub_key:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                i, 0, winreg.KEY_ALL_ACCESS)
            for j in range(0, winreg.QueryInfoKey(key)[0]-1):

                softwareInfo = {}
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + '\\' + key_name
                    each_key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)

                    name, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                    version, REG_SZ = winreg.QueryValueEx(
                        each_key, 'DisplayVersion')

                    try:
                        install_path, REG_SZ = winreg.QueryValueEx(
                            each_key, 'InstallLocation')
                        if install_path == "":
                            raise WindowsError
                    except WindowsError:
                        try:
                            install_path, REG_SZ = winreg.QueryValueEx(
                                each_key, 'InstallSource')
                            if install_path == "":
                                raise WindowsError
                        except:
                            install_path, REG_SZ = winreg.QueryValueEx(
                                each_key, 'UninstallString')
                            install_path = os.path.dirname(install_path)

                    softwareInfo["name"] = name
                    softwareInfo["version"] = version
                    softwareInfo["install_path"] = install_path

                    # 主流杀软
                    try:
                        if install_path.index("360Safe"):   # 360安全
                            yield softwareInfo
                        elif install_path.index("Kaspersky"):    # 卡巴斯基
                            yield softwareInfo
                        elif install_path.index("Rising"):   # 瑞星
                            yield softwareInfo
                        elif install_path.index("KWatch"):   # 金山
                            yield softwareInfo
                    except:
                        pass

                except WindowsError:
                    pass

    def get_installed_software_records(self) -> Iterable[dict]:

        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
        for i in sub_key:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                i, 0, winreg.KEY_ALL_ACCESS)
            for j in range(0, winreg.QueryInfoKey(key)[0]-1):
                softwareInfo = {}
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + '\\' + key_name
                    each_key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)

                    name, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                    version, REG_SZ = winreg.QueryValueEx(
                        each_key, 'DisplayVersion')
                    Publisher, REG_SZ = winreg.QueryValueEx(each_key, 'Publisher')

                    # 只有通过windowsinstaller安装的软件才有 InstallDate 字段
                    try:
                        InstallDate, REG_SZ = winreg.QueryValueEx(
                            each_key, 'InstallDate')
                    except:
                        InstallDate = "unwriten"
                    try:
                        install_path, REG_SZ = winreg.QueryValueEx(
                            each_key, 'InstallLocation')
                        if install_path == "":
                            raise WindowsError
                    except WindowsError:
                        try:
                            install_path, REG_SZ = winreg.QueryValueEx(
                                each_key, 'InstallSource')
                            if install_path == "":
                                raise WindowsError
                        except:
                            install_path, REG_SZ = winreg.QueryValueEx(
                                each_key, 'UninstallString')
                            install_path = os.path.dirname(install_path)+"\\"
                    softwareInfo["name"] = name
                    softwareInfo["Publisher"] = Publisher
                    softwareInfo["version"] = version
                    softwareInfo["install_path"] = install_path
                    softwareInfo["InstallDate"] = InstallDate
                    yield softwareInfo

                except WindowsError:
                    pass

    def get_services_records(self) -> Iterable[dict]:

        c = wmi.WMI()
        for s in c.Win32_Service():
            is_system_service = 'true' if s.ServiceType == "Own Process" else 'false'
            yield {
                "name": s.Name,
                "display_name": s.DisplayName,
                "start_type": s.StartMode,
                "process_id": s.ProcessId,
                "file_path": s.PathName,
                "status": s.State,
                "is_system_service": is_system_service

            }

    def get_current_network_records(self) -> Iterable[dict]:
        pass

    def get_system_logs_records(self) -> Iterable[dict]:
        pass

    def get_power_of_records(self) -> Iterable[dict]:
        pass

    def get_sharing_settings_records(self) -> Iterable[dict]:
        pass

    def get_strategy_records(self) -> Iterable[dict]:
        pass

    def get_users_groups_records(self) -> Iterable[dict]:
        pass

    def get_hardware_records(self) -> Iterable[dict]:
        pass

    def get_system_drives_records(self) -> Iterable[dict]:
        pass

