from faker import Faker


def generate_fake_user_data_dict():
    fake = Faker()
    new_user_data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    return new_user_data


def generate_random_phone_number():
    fake = Faker()
    return f"{fake.random_number(digits=10)}"
