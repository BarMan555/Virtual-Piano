import hashlib
import json
import loguru
from getDriveSerial import get_drive_serial


def validate_license(license_file="license.json"):
    """Проверяет лицензию на основе серийного номера носителя"""
    try:
        with open(license_file, "r") as file:
            license_data = json.load(file)
        current_serial = get_drive_serial()
        if hashlib.sha256(current_serial.encode()).hexdigest() == license_data["drive_serial"]:
            loguru.logger.success("Лицензия действительна")
            return True
        else:
            loguru.logger.error("Лицензия недействительна")
            return False
    except FileNotFoundError:
        loguru.logger.warning("Файл лицензии не найден")
    except Exception as e:
        loguru.logger.error(f"Ошибка проверки лицензии: {e}")
    return False
