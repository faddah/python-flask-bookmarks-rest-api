"""Utility script to generate and print a UUID v4."""
import uuid

if __name__ == "__main__":
    uuid_value = uuid.uuid4()  # pylint: disable=invalid-name
    uuid_string = str(uuid_value)  # pylint: disable=invalid-name
    print(uuid_string)