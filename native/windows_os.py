import os
import sys
import winreg
import win32com.client
import datetime
import getpass
import winshell as ws
from typing import Iterable
from abstract_os import AbstractOS
from winreg import *
import datetime
import wmi
from win32com.client import GetObject
import time
import traceback
import win32evtlog
import winerror
import win32con



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
        print(count)

        for i in range(count):
            subKeyName = EnumKey(keyHandle, i)
            subDir_2 = r'%s\%s' % (subDir, subKeyName)
            keyHandle_2 = OpenKey(regRoot, subDir_2)
            num = QueryInfoKey(keyHandle_2)[0]
            for j in range(num):

                record = {}
                subKeyName_2 = EnumKey(keyHandle_2, j)
                result_path = r'%s\%s' % (subDir_2, subKeyName_2)
                keyHandle_3 = OpenKey(regRoot, result_path)
                try:
                    flag, type_ = QueryValueEx(keyHandle_3, 'Service')
                    if flag == 'USBSTOR':
                        pass
                    else:
                        try:
                            name1, type_ = QueryValueEx(keyHandle_3, 'FriendlyName')
                            manufacture, type_ = QueryValueEx(keyHandle_3, 'Mfg')
                            description, type_ = QueryValueEx(keyHandle_3, 'DeviceDesc')
                        except:
                            name1, type_ = QueryValueEx(keyHandle_3, 'DeviceDesc')
                            manufacture, type_ = QueryValueEx(keyHandle_3, 'Mfg')
                            description, type_ = QueryValueEx(keyHandle_3, 'DeviceDesc')
                        record["name"] = name1.split(";")[-1].replace("(", "").replace(")", "")
                        record["manufacture"] = manufacture.split(";")[-1].replace("(", "").replace(")", "")
                        record["description"] = description.split(";")[-1].split(";")[-1].replace("(", "").replace(")", "")
                        record["V_P_ID"] = subKeyName.split(";")[-1]
                        yield record
                except:
                    pass
        CloseKey(keyHandle)
        CloseKey(regRoot)

    def get_installed_anti_virus_software_records(self) -> Iterable[dict]:

        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']

        for i in sub_key:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,i, 0, winreg.KEY_READ)
            for j in range(0, winreg.QueryInfoKey(key)[0]-1):
                softwareInfo = {}
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + '\\' + key_name
                    each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
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

        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
        for i in sub_key:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i, 0, winreg.KEY_READ)
            for j in range(0, winreg.QueryInfoKey(key)[0]-1):
                softwareInfo = {}
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + '\\' + key_name
                    each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                    name, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                    version, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayVersion')
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
                            install_path, REG_SZ = winreg.QueryValueEx(each_key, 'UninstallString')
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

        wmi = GetObject('winmgmts:/root/cimv2')
        processes = wmi.ExecQuery('SELECT * FROM Win32_Service')

        for s in processes:
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

        temp = os.popen('netstat -ano').readlines()
        for li in temp[4:]:
            netstat = {}
            li = [i for i in li[:-1].split(" ") if i != '']
            netstat["protocol"] = li[0]
            netstat["local_ip"] = li[1][: li[1].rfind(':')]
            netstat["local_port"] = li[1][li[1].rfind(':')+1:]
            if "*" in li[2]:
                netstat["remote_ip"] = li[2]
                netstat["remote_port"] = ""
            else:
                netstat["remote_ip"] = li[1][: li[1].rfind(':')]
                netstat["remote_port"] = li[2][li[1].rfind(':')+1:]
            pid = int(li[-1])
            if pid == 0:
                netstat["program_path"] = ""
                netstat["status"] = "TIME_WAIT"
            else:
                netstat["program_path"] = psutil.Process(pid).exe()
                netstat["status"] = psutil.Process(pid).status()
            netstat["process_name"] = psutil.Process(pid).name()
            netstat["pid"] = pid

            yield netstat

    def get_system_logs_records(self) -> Iterable[dict]:

        server = "localhost"
        for logtype in ["System", "Application", "Security"]:

            hand = win32evtlog.OpenEventLog(server, logtype)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)

            evt_dict = {win32con.EVENTLOG_AUDIT_FAILURE: 'Unknown',
                        win32con.EVENTLOG_AUDIT_SUCCESS: 'Unknown',
                        win32con.EVENTLOG_INFORMATION_TYPE: 'info',
                        win32con.EVENTLOG_WARNING_TYPE: 'waring',
                        win32con.EVENTLOG_ERROR_TYPE: 'error'}
            try:
                events = 1
                while events:
                    events = win32evtlog.ReadEventLog(hand, flags, 0)

                    for ev_obj in events:
                        infoTemp = {}

                        if not ev_obj.EventType in evt_dict.keys():
                            evt_type = "unknown"
                        else:
                            evt_type = str(evt_dict[ev_obj.EventType])
                        infoTemp["log_type"] = logtype
                        infoTemp["time"] = ev_obj.TimeGenerated.Format()
                        infoTemp["event"] = str(
                            winerror.HRESULT_CODE(ev_obj.EventID))
                        infoTemp["log_source"] = str(ev_obj.SourceName)
                        try:
                            infoTemp["description"] = ",".join(
                                ev_obj.StringInserts[:1])
                        except:
                            infoTemp["description"] = str(
                                ev_obj.StringInserts)[1:-1]

                        infoTemp["computer_name"] = str(ev_obj.ComputerName)
                        infoTemp["log_kind"] = str(evt_type)

                        yield infoTemp

            except:
                print(traceback.print_exc(sys.exc_info()))

    def get_power_of_records(self) -> Iterable[dict]:
        server = "localhost"
        for logtype in ["System", "Application", "Security"]:
            hand = win32evtlog.OpenEventLog(server, logtype)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            try:
                events = 1
                while events:
                    events = win32evtlog.ReadEventLog(hand, flags, 0)
                    for ev_obj in events:
                        infoTemp = {}
                        if winerror.HRESULT_CODE(ev_obj.EventID) == 6005:
                            infoTemp["time"] = ev_obj.TimeGenerated.Format()
                            infoTemp["event"] = "power on"
                            infoTemp["user"] = str(ev_obj.ComputerName)
                        elif winerror.HRESULT_CODE(ev_obj.EventID) == 6006:
                            infoTemp["time"] = ev_obj.TimeGenerated.Format()
                            infoTemp["event"] = "power off"
                            infoTemp["user"] = str(ev_obj.ComputerName)
                        elif winerror.HRESULT_CODE(ev_obj.EventID) == 6008:
                            infoTemp["time"] = ev_obj.TimeGenerated.Format()
                            infoTemp["event"] = "power off"
                            infoTemp["user"] = str(ev_obj.ComputerName)
                        else:
                            continue

                        yield infoTemp

            except:
                print(traceback.print_exc(sys.exc_info()))

    def get_sharing_settings_records(self) -> Iterable[dict]:

        sign_list = os.popen('net share  ').readlines()
        sign = []
        for li in sign_list:
            li = [i for i in li[:-1].split(" ") if i != '']
            try:
                if li[0][-1] == "$":
                    sign.append(li[0])
            except:
                pass

        for sign_one in sign:
            temp = os.popen('net share '+sign_one).readlines()
            temp1 = []
            k = 0
            for li in temp:
                li = [i for i in li[:-1].split(" ") if i != '']
                if k == 0 or k == 1 or k == 2 or k == 4:
                    temp1.append(li)
                k = k+1

            yield {

                "name": temp1[0][1],
                "path": "" if len(temp1[1]) == 1 else temp1[1][1],
                "description": "".join(temp1[2][1:]),
                "connections_count": len(temp1[3])-1,
            }


    def get_strategy_records(self) -> Iterable[dict]:
        pass

    def get_users_groups_records(self) -> Iterable[dict]:
        pass

    def get_hardware_records(self) -> Iterable[dict]:
        pass

    def get_system_drives_records(self) -> Iterable[dict]:
        pass

