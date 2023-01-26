import base64
import datetime
import re
import os
import logging

from typing import Dict, Tuple

log = logging.getLogger(__name__)


class BaseClass:
    """Base class for Administrator and Volunteer classes."""
    def __init__(
        self, surname:str, is_administrator:bool, name:str=None, birth_date:str=None, email:str=None,
        phone_number:str=None, address:str=None, photo:str=None
        ):
        self.validate_name(name)
        self.surname = surname
        self.name = name
        self.validate_birth_date(birth_date)
        self.validate_email(email)
        self.validate_phone_number(phone_number)
        self.created_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.address = address
        self.validate_photo(photo)
        self.validate_is_administrator(is_administrator)

    def validate_name(self, name:str):
        if name is not None and not re.match("^[a-zA-Z]+$", name):
            raise ValueError("Name should contain only alphabetic characters.")

    def validate_birth_date(self, birth_date:str):
        if birth_date is not None and not re.match("^[1-9][0-9]*$", birth_date):
            self.birth_date = '2000'
            log.warning("Birth Date should be a positive number. Assigned value is 2000")
        else:
            self.birth_date = birth_date

    def validate_email(self, email:str):
        if email is not None and '@' not in email:
            self.email = email + '@gmail.com'
            log.warning("Email address should contain '@' character. Assigned suffix @gmail.com")
        else:
            self.email = email

    def validate_phone_number(self, phone_number:str):
        if phone_number is not None:
            if len (phone_number) < 5:
                raise ValueError("Phone number should contain at least 7 digits.")
            else:
                phone_number = re.sub(r'[^0-9]', '', phone_number)
                self.phone_number = phone_number
                if not re.match("^[0-9]+$", self.phone_number):
                    log.warning("Warning: Phone number should contain only digits. Extra characters removed.")

    def validate_is_administrator(self, is_administrator:bool):
        if isinstance(is_administrator, bool):
            self.is_administrator = is_administrator
        else:
            log.error("A is_administrator should be a boolean value.")
            self.is_administrator = False

    def validate_photo(self, photo:str):
        if photo is not None:
            if not photo.endswith('.jpg'):
                raise ValueError("Photo should be only in jpg format.")
            if not os.path.exists(photo):
                raise FileNotFoundError("File not found in the path: {}".format(photo))
            try:
                with open(photo, "rb") as image_file:
                    self.photo = base64.b64encode(image_file.read()).decode()
            except:
                log.error("Unable to convert photo to base64, photo set to None.")
                self.photo = None

    def get_full_name(self) -> str:
        output = " ".join([self.name or "", self.surname, self.email or ""])
        return output.strip()

    def save_photo_to_specific_directory(self, path:str):
        if self.photo:
            image = base64.b64decode(self.photo)
            with open(path + "/foto.jpg", "wb") as f:
                f.write(image)


class Administrator(BaseClass):
    """Administrator class."""
    def __init__(self, surname:str, is_administrator:bool, name:str=None, birth_date:str=None, email:str=None,
        phone_number:str=None, address:str=None, photo:str=None):
        super().__init__(surname, is_administrator, name, birth_date, email, phone_number,
        address, photo)

    def add_photo_to_volunteer(self, volunteer, photo):
        volunteer.validate_photo(photo)
        volunteer.photo = photo


class Volunteer(BaseClass):
    """Volunteer class."""
    def __init__(self, surname:str, is_administrator:bool, name:str=None, birth_date:str=None, email:str=None,
        phone_number:str=None, address:str=None, photo:str=None, garbage_data=None):
        super().__init__(surname, is_administrator, name, birth_date, email, phone_number,
        address, photo)
        self.garbage_data = garbage_data or []

    def add_photo_to_volunteer(self, photo:str):
        self.validate_photo(photo)

    def print_garbage_data(self):
        for data in self.garbage_data:
            print(data)

    def print_garbage_data_for_specific_date(self, date:str):
        for data in self.garbage_data:
            if data['date'] == date:
                print(data)

    def calculate_weigt_and_volume_for_specific_day(self, date:str) :
        weight = 0
        volume = 0
        for data in self.garbage_data:
            if data['date'] == date:
                weight += data['weight']
                volume += data['volume']
        return weight, volume

    def calculate_weigt_and_volume_for_all_days(self) -> Tuple[int, int]:
        weight: int = 0
        volume: int = 0
        weight_by_type: Dict[str, int] = {}
        volume_by_type: Dict[str, int] = {}
        for data in self.garbage_data:
            weight += data['weight']
            volume += data['volume']
            if data['type'] not in weight_by_type:
                weight_by_type[data['type']] = 0
                volume_by_type[data['type']] = 0
            weight_by_type[data['type']] += data['weight']
            volume_by_type[data['type']] += data['volume']
        print("Weight by type:", weight_by_type)
        print("Volume by type:", volume_by_type)
        return weight, volume


# init an administrator object (required parameters only)
admin = Administrator("Kostyukov", True, name="Vlad")
print(admin.name, admin.surname, admin.is_administrator)

# init an administrator object (with not mandatory parameters also)
admin = Administrator("Kostyukov", True, name="Vlad", birth_date="1995")
print(admin.name, admin.surname, admin.birth_date)

##################################################################################
# init a volunteer object (required parameters only)
volunteer = Volunteer("Kostyukov", False, name="Oliver")
print(volunteer.name, volunteer.surname, volunteer.is_administrator)

# init a volunteer object (with not mandatory parameters also)
volunteer = Volunteer("Kostyukov", False, name="Oliver", birth_date="2018")
print(volunteer.name, volunteer.surname, volunteer.birth_date)

###############################################################################
# administrator adding a photo to a volunteer
photo_path = "photo.jpg"
admin.add_photo_to_volunteer(volunteer, photo_path)


# volunteer adding a photo to himself
photo_path = "photo.jpg"
volunteer.add_photo_to_volunteer(photo_path)

# save photo to specific directory
volunteer.save_photo_to_specific_directory("photo")

##############################################################################
# garbage data for a volunteer init
garbage_data = [
    {'date': '2022-01-26', 'type': 'paper', 'weight': 100, 'volume': 40},
    {'date': '2022-01-27', 'type': 'plastic', 'weight': 25, 'volume': 8},
    {'date': '2022-01-25', 'type': 'glass', 'weight': 315, 'volume': 99},
    {'date': '2022-01-25', 'type': 'paper', 'weight': 100, 'volume': 40},
    ]

volunteer.garbage_data = garbage_data
# print garbage data for volunteer
volunteer.print_garbage_data()

# print garbage data for specific date
volunteer.print_garbage_data_for_specific_date('2022-01-25')

# calculate weight and volume for specific date
print(volunteer.calculate_weigt_and_volume_for_specific_day('2022-01-25'))

# calculate weight and volume for all days
print(volunteer.calculate_weigt_and_volume_for_all_days())
