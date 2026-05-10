import pytest

@pytest.fixture(scope = "function")
def test_func_init_numbers():
    numbers = [1,2,3,4,5,6,7,8,9,10]
    return numbers

def test_func_filter_even_and_double(test_func_init_numbers):
    result=[
        x*2
        for x in test_func_init_numbers
        if x%2==0
    ]
    print(result)

@pytest.fixture(scope = "class", autouse = True)
def class_init_fixture():
    print("前置工作")
    numbers = [1,2,3,4,5,6,7,8,9,10]
    keys = ['name', 'age', 'city', 'job']
    values = ['张三', '18', '上海']
    yield (numbers, keys, values)
    print ("后置工作结束")

class TestClassPublic():
    def test_func_filter_even_and_double(self,class_init_fixture):
        numbers, keys, values = class_init_fixture
        result = [
            x*2
            for x in numbers
            if x%2 == 0
        ]
        print(result)
    def test_func_lists_to_dict(self,class_init_fixture):
        result = {}
        numbers, keys, values = class_init_fixture
        for i, key in enumerate(keys):
            result[key] = values[i] if i < len(values) else None
        print(result)
