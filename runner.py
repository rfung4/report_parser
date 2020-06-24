import inspect
import json

from sites.script import Script
from util.driver_manager import DriverWrapper


def run_script(script: Script, driver=DriverWrapper(), single=True):
    """ Runs a Script Instance, extracting/parsing values & exporting to a JSON pdf_file
    :param single: Execution of a single script (boolean)
    :param script: Script Instance
    :param driver: WebDriver Wrapper, Instansiates
    """
    print(f"Initializing Script: {script.name}\n")

    script.set_driver(driver)
    script_path = inspect.getfile(script.__class__)
    tag_func_map = {Script.REV_TAG: script.parse_revenue, Script.NET_INCOME_TAG: script.parse_net_income,
                    Script.CASH_TAG: script.parse_cash_flow, Script.EPS_TAG: script.parse_EPS}

    try:
        script.get_report()
        print("Acquiring Report")
    except RecursionError as e:
        print(f"Exception occurred when acquiring report for {script.name} : {e}")
        return

    for tag, func in tag_func_map.items():
        try:
            func()
            print(f"Extracted {script.values[tag]} for {tag}")
        except RecursionError as e: # EXC
            print(f"Exception occurred when parsing {tag} : {e}")

    output_path = script_path.rsplit("/", 1)[0] + f'/{script.name}.json'

    with open(output_path, 'w') as fp:
        json.dump(script.values, fp)

    print(f"\nExecution complete for {script.name}\nOutput written to: {output_path}\n")

    if single:
        driver.quit_driver()

    script.cleanup()


def run_all_scripts():
    driver = DriverWrapper()
    scripts = []

    for script in scripts:
        run_script(script, driver, False)

    driver.quit_driver()
