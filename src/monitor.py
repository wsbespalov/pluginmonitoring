import os
import re
import sys
import time
import subprocess
from datetime import datetime

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

from subprocess import Popen


def get_plugin_name(plugin):
    if isinstance(plugin, str):
        return plugin.split('/')[-1][:-3]
    
def load_plugins():
    plugin_dir = 'plugins'
    plugin_prefix = 'plg'

    listdir = os.listdir(os.path.join(os.path.dirname(__file__), plugin_dir))

    plugins = []
    plugins_names = []

    for plugin in listdir:
        if plugin_prefix in plugin:
            plugins.append(os.path.abspath(os.path.join(os.path.dirname(__file__), plugin_dir, plugin)))
            plugins_names.append(plugin)

    plugins.sort()

    return plugins, plugins_names

def run_one_plugin(plugin):
    print('[R] Try to run plugin: {}'.format(plugin))
    proc = '{0} {1}'.format(sys.executable, plugin)
    plugin_process = Popen(proc, shell=True, preexec_fn=os.setsid)
    plugin_pid = plugin_process.pid
    print('[R] Plugin: {} run with PID: {}'.format(plugin, plugin_pid))

def run_plugins():
    plugins, plugins_names = load_plugins()
    
    print('[+] Get {} files from plugin directory'.format(len(plugins_names)))
    
    plg_counter = 0
    for plg_index in range(0, len(plugins)):
        run_one_plugin(plugins[plg_index])
        plg_counter += 1
    
    print('[+] {} Plugins was run'.format(plg_counter))
    
    return plugins, plugins_names

def only_digits(s):
    return re.sub("\D\.\?", "", s)

def raise_plugin(plugin):
    run_one_plugin(plugin)

def monitor_plugins(plugins, plugins_names):
    while True:
        try:
            for plg_index in range(0, len(plugins)):
                plugin_name_to_watch = plugins_names[plg_index]
                cmd = "ps aux|grep '%s'|grep -v grep |awk '{print $2}'" % (plugin_name_to_watch)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
                out, err = p.communicate()
                if isinstance(out, bytes):
                    out = out.decode("utf-8").replace('\n', '')
                    out = only_digits(out)
                else:
                    out = None
                if err is None:
                    if out is not None and out != "":
                        print('[+] Process {} with PID {} is alive'.format(plugin_name_to_watch, out))
                    elif out is None or out == "":
                        print('[-] Process {} is not alive'.format(plugin_name_to_watch))
                        print('[r] Try raise the plugin: {}'.format(plugin_name_to_watch))
                        raise_plugin(plugins[plg_index])
                else:
                    print('[---] Process {} is not alive. Err: {}'.format(plugin_name_to_watch, err))
                    raise_plugin(plugins[plg_index])
            time.sleep(10)
        except KeyboardInterrupt:
            print('Keyboard interrupt...Exiting...')
            sys.exit(0)

def main():
    print("Started at: {}".format(now()))
    plugins, plugins_names = run_plugins()
    monitor_plugins(plugins, plugins_names)

if __name__ == '__main__':
    sys.exit(main())