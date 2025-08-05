import os

def get_file_extensions_in_current_directory(current_dir):
    """
    Scans the current directory, finds all unique file extensions,
    and returns them as a list.
    """
    # current_dir = os.getcwd()  # 获取当前工作目录
    extension_set = set()  # 使用集合来自动处理重复项

    # 遍历当前目录下的所有条目（文件和文件夹）
    # print(os.listdir(current_dir))
    for item in os.listdir(current_dir):
        # 构建完整路径
        item_path = os.path.join(current_dir, item)
        print(item_path)
        # 检查当前条目是否是文件
        if os.path.isfile(item_path):
            # 分割文件名和后缀名
            _, file_extension = os.path.splitext(item)
            
            # 如果后缀名存在（不为空），则添加到集合中
            if file_extension:
                extension_set.add(file_extension)
        elif os.path.isdir(item_path):
            # 如果是文件夹，则递归调用此函数
            # 并将返回的后缀名集合更新到当前集合中
            extension_set.update(get_file_extensions_in_current_directory(item_path))

    # 将集合转换为列表并返回
    return list(extension_set)

if __name__ == "__main__":
    extensions = get_file_extensions_in_current_directory('/home/tyrfly/labtask')
    print("当前目录下的所有文件后缀名列表：")
    print(extensions)