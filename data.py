#!/usr/bin/env python3

from faker import Faker

fake = Faker()

def get_registered_user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "job": fake.job(),
        "email": fake.email(),
        "dob": fake.date(),
        "created_at": fake.year()
    }

if __name__ == "__main__":
    print(get_registered_user())
