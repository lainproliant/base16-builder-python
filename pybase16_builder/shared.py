import os
import yaml
from collections import namedtuple

CWD = os.path.realpath(os.getcwd())
job_options_fields =['base_output_dir', 'templates', 'lock', 'job_queue',
                     'verbose']
JobOptions = namedtuple('JobOptions', job_options_fields,
                        defaults=[None] * len(job_options_fields))
JobOptions._field_defaults = {x: 0 for x in JobOptions._fields}
ACodes = namedtuple('ACodes',
                    ['red', 'yellow', 'bold', 'end'])
acodes = ACodes(red='\033[31m', yellow='\033[33m',
                bold='\033[1m', end='\033[0m')


def rel_to_cwd(*args):
    """Get absolute real path of $path with $CWD as base."""
    return os.path.join(CWD, *args)


def get_yaml_dict(yaml_file):
    """Return a yaml_dict from reading yaml_file. If yaml_file is empty or
    doesn't exist, return an empty dict instead."""
    try:
        with open(yaml_file, 'r') as file_:
            yaml_dict = yaml.safe_load(file_.read()) or {}
        return yaml_dict
    except FileNotFoundError:
        return {}


def thread_print(lock, msg, verbose=True):
    """Safely print to stdout from thread."""
    lock.acquire()
    if verbose:
        print(msg)
    lock.release()


def verb_msg(msg, lvl=1):
    """Print a warning ($lvl=1) or an error ($lvl=2) message."""
    if lvl == 1:
        return '{0.yellow}{0.bold}Warning{0.end}:\n{1}'.format(acodes, msg)
    elif lvl == 2:
        return '{0.red}{0.bold}Error{0.end}:\n{1}'.format(acodes, msg)
