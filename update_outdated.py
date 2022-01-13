#!/usr/bin/env python3
"""update all outdated packages in current environment"""

import subprocess as sbp
import sys
from typing import List

# default values
pip_pkg_name = "pip"
python_exe_file = "python"

if "linux" == sys.platform:
    pip_pkg_name = "pip3"
    python_exe_file = "python3"


def exist_in_list_of_dict(package_name: str, source: List[dict], key_name="name") -> int:
    """
        Возвращает индекс содержимого списка словарей, если содержимое словаря
        по ключу key_name содержит package_name
    """
    for itm in source:
        if package_name == itm[key_name]:
            return source.index(itm)
    # not found (-1)
    return -1


def get_outdated_packages() -> List[dict]:
    """
    return list of dict outdated packages
    """
    str_cmd = f"{pip_pkg_name} list -o --format=json"
    return eval(str(sbp.run(str_cmd, shell=True, stdout=sbp.PIPE).stdout, encoding="utf-8"))


def update_package(cmd: str) -> sbp.CompletedProcess:
    return sbp.run(cmd, shell=True)  # !!!


if "__main__" == __name__:
    # get list with all outdated packages
    pkgs = get_outdated_packages()
    print(f"{len(pkgs)} outdated packages awaiting...")

    index = exist_in_list_of_dict(pip_pkg_name, pkgs)
    if index >= 0:
        pkgs.pop(index)  # строку с pip на первое место в списке для обновления в первую очередь
        s = f"{python_exe_file} -m {pip_pkg_name} install --upgrade {pip_pkg_name}"
        update_package(s)

    cnt, mx = 0, len(pkgs)

    while pkgs:
        pkg = pkgs.pop()
        pkg_name = pkg["name"]
        s = f"{pip_pkg_name} install --upgrade {pkg_name}"
        # updating
        completed_process = update_package(s)  # !!!

        if 0 == completed_process.returncode:
            cnt += 1
            print(f"{pkg_name} package updated. Total {int(100 * cnt / mx)} % updated.")
