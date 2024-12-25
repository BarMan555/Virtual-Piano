import platform
import subprocess
import loguru

def get_drive_serial():
    """Получение серийного номера диска"""
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output("wmic diskdrive get serialnumber", shell=True)
            return output.decode().split("\n")[1].strip()
        except Exception as e:
            loguru.logger.error(f"Ошибка получения серийного номера: {e}")
    elif platform.system() == "Linux":
        try:
            output = subprocess.check_output("lsblk -o SERIAL", shell=True)
            return output.decode().split("\n")[1].strip()
        except Exception as e:
            loguru.logger.error(f"Ошибка получения серийного номера: {e}")
    return None

if __name__ == "__main__":
    serial_number = get_drive_serial()
    print(serial_number)