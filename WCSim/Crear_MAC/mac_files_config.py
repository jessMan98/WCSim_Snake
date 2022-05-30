"""
Script to generate new .mac files combining different parameters from a
config.json file.

New .mac files will be created with the nomenclature:
wcs_<specification>_<particle_name>_<iteration_number>_<energy>_MeV.mac

Example of usage:

- Run 200 iterations for each particle combination. Copy resulting files in
C:\\test directory
python3 mac_files_config.py -i 200 -d "C:\\test directory"
"""

import json
import os
import re
import shutil
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

WORKDIR = os.getcwd()  # Current working directory (where script is run)
RESULTS_PATH = os.path.join(WORKDIR, 'resulting_mac_files')
BASE_MAC_FILE = os.path.join(WORKDIR, 'base.mac')
CONFIG_JSON = os.path.join(WORKDIR, 'config.json')


def main():
    """Generate new .mac files."""
    try:
        args = _parse_args(sys.argv[1:])
        config = _get_config(args.config_json)
        base_mac = _verify_base_mac_file(args.base_mac)
        _set_results_path()
        destination_path = _verify_destination_path(args.destination_path)
        for _, particle in config.items():
            _generate_particle_mac(
                particle, args.iterations, args.add_zeros,
                args.iteration_digits, destination_path, base_mac
            )
    except KeyboardInterrupt:
        print('Stopped due user interruption.\n')
    except Exception as error:
        _print_error(f'An error occurred: {error}\n')


def _parse_args(args):
    """Parse input arguments and return input values."""
    parser = ArgumentParser(
        formatter_class=lambda prog: RawTextHelpFormatter(
            prog, max_help_position=7
        ),
        description=('Script to generate new .mac files combining different '
                     'parameters from a config.json file.')
    )
    parser.add_argument(
        '--add_zeros', action='store_true',
        help='Add zeros to the left side of the iteration number.'
    )
    parser.add_argument(
        '--base_mac', default=BASE_MAC_FILE,
        help='Absolute path of the base .mac file.'
    )
    parser.add_argument(
        '--config_json', default=CONFIG_JSON,
        help='Absolute path of the configuration JSON file.'
    )
    parser.add_argument(
        '-d', '--destination_path', default='',
        help=('Absolute path of destination location. Generated files will be '
              'copied to this location.')
    )
    parser.add_argument(
        '-i', '--iterations', default=1, type=int,
        help='Number of files creation iterations (copies).'
    )
    parser.add_argument(
        '--iteration_digits', default=4, type=int,
        help=('Number of iteration digits. Applicable only if --add_zeros is '
              'specified.')
    )
    return parser.parse_args(args)


def _get_config(config_file):
    """Return an object with the dumped configuration JSON file."""
    if not os.path.isfile(config_file):
        _print_error(f'Configuration file "{config_file}" does not exist.')
    with open(config_file) as json_file:
        return json.load(json_file)


def _set_results_path():
    """Set the results path.

    If the results path does not exist, it will be created.
    If the results path exists, it will be emptied.
    """
    if not os.path.isdir(RESULTS_PATH):
        print(f'Creating results path "{RESULTS_PATH}"...')
        os.mkdir(RESULTS_PATH)
    else:
        print(f'Removing files in results path "{RESULTS_PATH}"...')
        _empty_results_path()


def _verify_base_mac_file(base_mac_file):
    """Verify the base .mac file exists."""
    if not os.path.isfile(base_mac_file):
        _print_error(f'The base .mac file "{base_mac_file}" does not exist.')
    return base_mac_file


def _verify_destination_path(destination_path):
    """Verify the destination path exists."""
    if not destination_path:
        destination_path = RESULTS_PATH
    if not os.path.isdir(destination_path):
        _print_error(
            f'The destination path "{destination_path}" does not exist.'
        )
    print(f'Destination path is "{destination_path}".')
    return destination_path


def _empty_results_path():
    """Remove all the files in the results path."""
    for filename in os.listdir(RESULTS_PATH):
        file_path = os.path.join(RESULTS_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as error:
            print(f'Failed to delete {file_path}. Reason: {error}')


def _generate_particle_mac(particle, iterations, add_zeros, iteration_digits,
                           destination_path, base_mac):
    """Generate the .mac files with all the particle combinations."""
    specification_list = [  # Split elements and remove white spaces
        i.strip() for i in particle['specification'].split(',')
    ]
    particle_name = particle['name']
    energy_list = particle['energy']
    simulations = particle['simulations']
    creation_count = 0
    print(f'Generating the .mac files for particle "{particle_name}"...')

    for specification in specification_list:
        for energy_unit, energy_levels in energy_list.items():
            # Split the energy level list in config JSON (separated by commas)
            energy_levels = [
                i.strip() for i in energy_levels.split(',')
            ]
            for energy in energy_levels:
                new_files_number = _create_mac_files(
                    iterations, add_zeros, iteration_digits, destination_path,
                    base_mac, {
                        'specification': specification,
                        'particle_name': particle_name,
                        'energy': energy,
                        'energy_unit': energy_unit,
                        'simulations': simulations
                    }
                )
                creation_count += new_files_number
    print(f'{creation_count} files were created for "{particle_name}" '
          'particle.')


def _create_mac_files(iterations, add_zeros, iteration_digits,
                      destination_path, base_mac, metrics):
    """Create a .mac with metrics given, the given number of iterations."""
    _validate_integer_metrics({  # Check set metrics are integers
        'energy': metrics["energy"], 'simulations': metrics['simulations']
    })
    count = 0
    for run_number in range(iterations):
        if add_zeros:  # Add zeros to the left size of number
            run_number = _add_left_zeros(run_number, iteration_digits)
        mac_name = (  # Set the name for .mac (and .root) file
            f'wcs_{metrics["specification"]}_{metrics["particle_name"]}'
            f'__{run_number}_{metrics["energy"]}_{metrics["energy_unit"]}'
        )
        # Dictionary containing .mac placeholders (left) and their values
        # to be replaced (right)
        replacing_dict = {
            '@particle': metrics['particle_name'],
            '@energy_value': metrics['energy'],
            '@energy_unit': metrics['energy_unit'],
            '@output_name': mac_name,
            '@simulations': metrics['simulations']
        }
        # Set the new .mac file path
        new_mac_file = os.path.join(RESULTS_PATH, f'{mac_name}.mac')
        _replace_string_in_file(
            base_mac, new_mac_file, replacing_dict
        )
        _copy_new_mac_file(  # Copy new file in custom destination
            new_mac_file, f'{mac_name}.mac', destination_path
        )
        count += 1
    return count


def _validate_integer_metrics(metrics):
    """Validate elements of a list of metrics are integers."""
    for metric_name, metric_value in metrics.items():
        try:
            int(metric_value)
        except ValueError:
            _print_error(
                f'Metric "{metric_name}" must contain integers only. '
                f'Incorrect value: "{metric_value}".'
            )


def _add_left_zeros(number, iteration_digits):
    """Add zeros to the left side of the experiment run number.

    Zeros will be added according to missing spaces until iterations_digits are
    reached.
    """
    number = str(number)
    return f'{"0" * (iteration_digits - len(number))}{number}'


def _replace_string_in_file(source_file, new_file, repldict):
    """Find strings within a file and creates a new one with strings replaced.

    Keyword arguments:
    source_file -- Source file, with the string(s) to be replaced
    new_file -- File name that will have the content of the source file with
        the string(s) replaced.
    repldict -- Dictionary containing one or more strings to be replaced. The
        keys will be the matching strings and the values will be the replacing
        strings. I.e.
            repldict = {
                'old string1': 'new string1',
                'old string2': 'new string2', ...
            }
    """
    pfile_path = source_file
    def _replfunc(match):  # Replacing function
        return repldict[match.group(0)]
    regex = re.compile('|'.join(re.escape(i) for i in repldict))
    with open(pfile_path) as fin:
        with open(new_file, 'w') as fout:
            for line in fin:
                fout.write(regex.sub(_replfunc, line))


def _copy_new_mac_file(mac_file_path, mac_file_name, destination_path):
    """Copy the generated .mac file in the results path."""
    if destination_path != RESULTS_PATH:
        destination_file = os.path.join(destination_path, mac_file_name)
        shutil.copyfile(mac_file_path, destination_file)


def _print_error(msg):
    """Print the error message and exit program."""
    print(msg)
    sys.exit(1)


if __name__ == '__main__':
    main()
