from native_os import NativeOS


def get_all_methods():
    # https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has/20100900
    instance = NativeOS().instance()
    return [method_name for method_name in dir(instance) if callable(getattr(instance, method_name)) and not method_name.startswith('__')]


def run_methods(selected_methods: list):
    obj_methods = get_all_methods()
    if selected_methods is None:
        selected_methods = obj_methods
    total_count = len(selected_methods)
    implement_methods = []
    failed_methods = []
    for method_name in selected_methods:
        assert (method_name in obj_methods)
        func = getattr(NativeOS().instance(), method_name)
        try:
            generator = func()
            for i in generator:
                print(i)
            implement_methods.append(method_name)
        except Exception as ex:
            print(f'failed call {method_name}', ex)
            failed_methods.append(method_name)
    print("-----------------FAILED----------------")
    for i in failed_methods:
        print(i)
    implement_count = len(implement_methods)
    print("-------------------OK------------------")
    for i in implement_methods:
        print(i)
    print(f"{implement_count} of {total_count} has implemented {implement_count * 100 / total_count}%")


if __name__ == '__main__':
    run_methods(None)
