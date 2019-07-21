import os
import sys
import shutil
import argparse
import logging

PROJECT_ROOT = 'P:'         # Where we look (P drive)
GOLIVE = True               # False means a dry run
FOLDER_LIST = []            # List of all folders in PROJECT_ROOT
logger = []


def buildPath(project_num, project_name):
    """
    Create the path to a file or project folder from project_num
    and project_name.
    """
    # Check that the project number doesn't exist already
    length = len(project_num)
    folder = [x for x in FOLDER_LIST if x[: length] == project_num]
    if (len(folder) == 1 and
            os.path.isdir(os.path.join(PROJECT_ROOT, folder[0]))):
        # The folder exists (it should not)
        logger.error(f'Project number {project_num} already exists.')
        return False
    else:  # We're ready to build the project folder path
        return os.path.join(PROJECT_ROOT, f'{project_num} {project_name}')


def createProject(project_num, project_name, project_type):
    """
    Create a new project.
    If GOLIVE is False, just run the logic and issue logging messages.
    """

    def copyFolders(source, dest):
        logger.info(f'Copying from {source} to {dest}')
        if GOLIVE:
            status = shutil.copytree(source, dest)
            logger.debug(f'Copy status was {status}')

    logger.info(
        f'Creating {project_type} project: {project_num} {project_name}')
    if GOLIVE:
        dest = buildPath(project_num, project_name)
    else:
        dest = "dry run"

    if dest:
        try:            # Copy template into the folder
            if project_type == 'CAD':
                copyFolders(CAD_SOURCE, dest)
            elif project_type == 'Revit':
                copyFolders(REVIT_SOURCE, dest)
            else:
                copyFolders(GENERIC_SOURCE, dest)
        except OSError as e:
            logger.error(f'copyFiles: {e}')
            return False
        return True
    else:         # We failed to create the path for some reason
        return False


def checkNewProject(project_num, project_name):
    """
    Check project number and name prior to creating a project.
    Project number was set when create mode was invoked.
    """
    tr_table = str.maketrans('', '', ',;:"\'\\`~!%^#&{}|<>?*/')
    clean_name = project_name.translate(tr_table)
    clean_name = clean_name.strip('_ .\t\n-')
    if clean_name != project_name:
        logger.error("Name cannot contain special characters")
        return False
    if len(clean_name) < 6:
        logger.error("Project name too short.")
        return False

    return True


def main():
    """
    Top level function processes arguments and runs the app.
    Args:
      -i: Show informational messages
      -d: Show debug messages (use only one of -i and -w)
      -t: Test run - don't actually create folders
      -w location: Change from default "P:" for PROJECT_ROOT
      <number>%<name>%<type>: project number, name and type.
    Final argument is a delimited string like this:
    'Project number%Project Name%Project Type'
    For example: '2019.133%SCFHP TI%R'
    Project type is 'Revit', 'CAD', or 'Generic'
    """
    global GOLIVE       # If False, it's a dry run only
    global PROJECT_ROOT
    global CAD_SOURCE
    global REVIT_SOURCE
    global GENERIC_SOURCE
    global FOLDER_LIST
    global logger

    logger = logging.getLogger('__name__')
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    logger.debug(sys.argv)
    parser = argparse.ArgumentParser(description='Create a project')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', action='store_true', help="Show INFO messages")
    group.add_argument('-d', action='store_true', help="Show DEBUG messages")
    parser.add_argument('-t', action='store_true', help='Test: dry run only')
    parser.add_argument('-r', help="Set root directory")
    parser.add_argument('project_data', nargs='+', help="<num>%,<name>%<type>")

    args = parser.parse_args(sys.argv[1:])
    logger.debug(args)
    if args.i:
        logger.info('Setting logging level to INFO')
        logger.setLevel(logging.INFO)
    elif args.d:
        logger.info('Setting logging level to DEBUG')
        logger.setLevel(logging.DEBUG)
    if args.t:
        GOLIVE = False
        logger.info('Dry run...')
    if args.r:
        PROJECT_ROOT = args.r
        logger.info(f'Setting PROJECT_ROOT to {args.r}')

    CAD_SOURCE = os.path.join(PROJECT_ROOT, 'Templates', 'CAD_Template')
    REVIT_SOURCE = os.path.join(PROJECT_ROOT, 'Templates', 'Revit_Template')
    GENERIC_SOURCE = os.path.join(PROJECT_ROOT,
                                  'Templates', 'Generic_Template')
    FOLDER_LIST = os.listdir(PROJECT_ROOT)
    project_info = ' '.join(args.project_data)  # The parser split at spaces
    logger.debug(f'Project info: {project_info}')
    project_info = project_info.split('%')   # Divide it into our 3 fields
    project_number, project_name, project_type = project_info
    assert project_type in ['Revit', 'CAD', 'Generic']

    if checkNewProject(project_number, project_name):  # Sanity checks
        success = createProject(project_number, project_name, project_type)
        if success:
            logger.info(f'Created project {project_number} {project_name}')
        else:
            logger.error('Project creation failed.')


if __name__ == '__main__':
    main()
