import importlib
import inspect
import json
import os
import pkgutil
from pathlib import Path

from definitions import RESULTS_PATH, SITES_PATH
from sites.script import Script


def run_script(script: Script):

    """ Runs a Script Instance, extracting/parsing values & exporting to a JSON pdf_file
    :param script: Script Instance
    """

    print(f"Initializing Script: {script.name}\n")

    tag_func_map = {Script.REV_TAG: script.parse_revenue, Script.NET_INCOME_TAG: script.parse_net_income,
                    Script.CASH_TAG: script.parse_cash_flow, Script.EPS_TAG: script.parse_EPS}

    try:
        script.get_report()
        print("Acquiring Report")
    except Exception as e:
        print(f"Exception occurred when acquiring report for {script.name} : {e}")
        return

    for tag, func in tag_func_map.items():
        try:
            func()
            print(f"Extracted {script.values[tag]} for {tag}")
        except Exception as e:
            print(f"Exception occurred when parsing {tag} : {e}")

    output_path = "".join([RESULTS_PATH, '/', script.name, '.json'])

    with open(output_path, 'w') as fp:
        json.dump({'values': script.values, 'paragraphs': '', 'forward guidance': ''}, fp)

    print(f"\nExecution complete for {script.name}\nOutput written to: {output_path}\n")
    script.cleanup()


def get_script_class_from_path(package_name) -> []:
    """ Returns a Child of Script, given a package name. Searches /sites/ directory
    :param package_name: Package name
    :return: Script Subclass
    """
    for (_, name, _) in pkgutil.iter_modules([Path(SITES_PATH + f'{package_name}/' + '__init__.py').parent]):
        imported_module = importlib.import_module('.' + name, package=f'sites.{package_name}')
        attrs = list(filter(lambda x: not x.startswith('__'),
                            dir(imported_module)))

        for attr in attrs:
            n_type = getattr(imported_module, attr)
            if inspect.isclass(n_type) and issubclass(n_type, Script) and n_type != Script:
                return n_type


def get_site_package_names():
    """ Searches /sites/ directory for site names
    :return: List containing package names
    """
    path_package = []

    for root, dirs, files in os.walk(SITES_PATH, topdown=False):
        for name in dirs:
            if '__' not in name:
                path_package.append(os.path.join(root, name).split("/")[-1])

    return path_package


def run_all_scripts():
    """
        Dynamically and instantiates Script instances located in the /sites/ directory, sequentially running each.
    """
    print("Executing ALL scripts... \n\n")

    for i in get_site_package_names():
        script_class = get_script_class_from_path(i)
        run_script(script_class())


if __name__ == '__main__':
    run_all_scripts()


