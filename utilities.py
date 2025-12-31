
def check_for_keys(dictionary: dict[any, any], keys: any) -> None:
    list_of_keys: list[any]
    if not isinstance(keys, list):
        list_of_keys = [keys]
    else:
        list_of_keys = keys

    for key in list_of_keys:
        if key not in dictionary:
            raise KeyError(f"{key} is not in {dictionary}")

def get_if_available(dictionary: dict[any, any] | None, key: any) -> any:
    if isinstance(dictionary, dict) and key in dictionary:
        return dictionary[key]
    else:
        return None