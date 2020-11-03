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
                    if(('Service' in name) and ('WUDFRd' in value)):
                        device_name, type_ = QueryValueEx(
                            keyHandle_3, 'FriendlyName')
                        manufacture, type_ = QueryValueEx(keyHandle_3, 'Mfg')
                        storage, type_ = QueryValueEx(keyHandle_3, 'Capabilities')
                        serilas = subKeyName_2

                        last_plugin_time = str(datetime.datetime.fromtimestamp(
                            int(QueryInfoKey(keyHandle_3)[2]*0.0000001+timestamp)))
                        record["device_name"] = device_name
                        record["manufacture"] = manufacture
                        record["storage"] = str(storage)+"GB"
                        record["last_plugin_time"] = last_plugin_time

                        yield record

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
        pass

    def get_installed_software_records(self) -> Iterable[dict]:
        pass

    def get_services_records(self) -> Iterable[dict]:
        pass

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

