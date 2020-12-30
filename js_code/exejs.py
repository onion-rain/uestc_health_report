import execjs

def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

def compile_js(file_name):
    return execjs.compile(js_from_file(file_name))
