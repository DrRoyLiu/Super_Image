def show_progress_bar(iteration: int, total: int = 100, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 100, fill: str = '█', print_end: str = "\r"):
    """
    显示进度条

    Args:
        iteration (int): 当前进度. Defaults to 1.
        total (int): 总进度，默认100
        prefix (str, optional): 进度条前缀. Defaults to ''.
        suffix (str, optional): 进度条后缀. Defaults to ''.
        decimals (int, optional): 百分比保留的小数位数. Defaults to 1.
        length (int, optional): 进度条长度. Defaults to 100.
        fill (str, optional): 进度条填充字符. Defaults to '█.
    Returns:
        None
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()
