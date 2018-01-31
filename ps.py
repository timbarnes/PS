#
import os
import shutil
import datetime
import tkinter
from tkinter import ttk
import openpyxl

CURRENT_YEAR = datetime.datetime.now().year    # This year
PROJECT_ROOT = './Test'                        # Where we look (P drive)
CAD_SOURCE = os.path.join(PROJECT_ROOT, 'CAD_Template')
REVIT_SOURCE = os.path.join(PROJECT_ROOT, 'Revit_Template')
INFO_FILE = 'Project_Information.xlsx'

FOLDER_LIST = os.listdir(PROJECT_ROOT)    # List of all folders in PROJECT_ROOT


def popup(message):
    """
    Simple popup message box.
    """
    w = tkinter.Toplevel()
    m = tkinter.Message(w, text=message, width=400)
    m.grid(row=0, column=0, pady=20)
    e = ttk.Button(w, text="OK", command=w.destroy)
    e.grid(row=1, column=0, pady=20)


def error(message):
    """
    Print an error to a pop-up.
    """
    popup("Error: {}".format(message))


def buildPath(app, file=None):
    """
    Create the path to a file or project folder from app and optional fileName
    """
    if file:
        return os.path.join(PROJECT_ROOT,
                            "{} - {}".format(app.project_number.get(),
                                             app.project_name.get()),
                            file)
    else:
        return os.path.join(PROJECT_ROOT,
                            "{} - {}".format(app.project_number.get(),
                                             app.project_name.get()))


def getProjectNumber():
    """
    Get the number of the most recent project,
    and return the next number up as a 2 or 3 digit string..
    """
    pnum = str(datetime.datetime.now().year)
    fileList = [f for f in FOLDER_LIST if f[:4] == pnum]
    try:
        latestProject = sorted(fileList, reverse=True)[0]
        projectNumber = int(latestProject[5: 8])
        return "{:02}".format(projectNumber + 1)
    except IndexError:
        error("getProjectNumber: No projects found.")
        return '000'


def readProjectData(app):
    """
    Read project information from an Excel template file.
    """
    fileName = buildPath(app, INFO_FILE)
    try:
        print('Opening file: %s', fileName)
        pf = openpyxl.load_workbook(fileName)
        sheet = pf.active
        app.project_name.set(sheet['B4'].value)
        app.project_pm.set(sheet['B6'].value)
        app.project_type.set(sheet['B7'].value)
        app.project_addr.set(sheet['B9'].value)
        app.project_csz.set(sheet['B10'].value)
        app.billing_name.set(sheet['B12'].value)
        # app.billing_title.set(sheet['B13'].value)
        app.billing_addr.set(sheet['B17'].value)
        app.billing_csz.set(sheet['B18'].value)
    except FileNotFoundError:
        error("readProjectData: "
              "Project spreadsheet not found: {}".format(fileName))


def getProjectData(app):
    """
    Get information for a given project and instantiate in the GUI.
    Return False if there's no such project.
    """
    pnum = app.project_number.get()
    length = len(pnum)
    pfolder = [x for x in FOLDER_LIST if x[: length] == pnum]
    if (len(pfolder) == 1 and
            os.path.isdir(os.path.join(PROJECT_ROOT, pfolder[0]))):
            # We found the folder: return a tuple of fullname, number and name
        pname = pfolder[0][9:]
        while pname[0] in ['-', ' ']:
            pname = pname[1:]
        app.project_name.set(pname)
        readProjectData(app)
        return (pfolder[0], pnum, pname)
    else:
        error("getProjectData: No such project: {}".format(pnum))
        return False


def makeProjectFolder(app):
    """
    Create the project name and create the folder for it.
    Assumes data has been validated.
    """
    folderName = buildPath(app)
    try:
        os.mkdir(folderName)
        popup("Folder {} created".format(folderName))
    except FileExistsError:
        error("makeProjectFolder: Folder already exists")


def copyFiles(app, folder):
    """
    Copy files based on project type to the pre-created folder.
    """
    dest = buildPath(app)
    try:
        if app.mode == 'CAD':
            shutil.copytree(os.path.join(PROJECT_ROOT, CAD_SOURCE), dest)
        elif app.mode == 'Revit':
            shutil.copytree(os.path.join(PROJECT_ROOT, REVIT_SOURCE), dest)
        else:
            # 02 Folder only
            pass
    except OSError as e:
        error("copyFiles: {}".format(e))


def setMode(app, mode):
    """
    Sets the mode to 'create' or 'modify' based on button press.
    """
    app.mode = mode
    if mode == 'create':
        app.next_pnum = "{}.{}".format(CURRENT_YEAR, getProjectNumber())
        app.project_number.set(app.next_pnum)
        app.project_number.state = 'disabled'
        app.mode_label.set("// Mode: CREATE - Enter name, type, and PM. //")
    if app.mode == 'modify':
        app.mode_label.set("// Mode: UPDATE - Enter Project Number //")
        app.project_number.set('-.-')


def createProject(app):
    """
    Create a new project using pre-validated information.
    """
    if not app.mode == 'create':
        error('createProject: Mode not set to create')
        return
    print(("Creating Project '{} - {}'"
           "for {}.").format(app.project_number.get(),
                             app.project_name.get(),
                             app.project_pm.get()))
    new_folder = makeProjectFolder(app)
    copyFiles(app, new_folder)


def modifyProject(app):
    """
    Alter project information for an existing project.
    """
    # check basic data is in place
    # write updated information to the spreadsheet
    print("Modify project {}".format(app.project_number.get()))


def checkNewProject(app):
    """
    Check project name and PM data prior to creating a project.
    Project number was set when create mode was invoked.
    """
    app.project_name.set(app.project_name.get().strip(' \t\n-'))
    if len(app.project_name.get()) < 6:
        error("Project name too short.")
        return False
    app.project_pm.set(app.project_pm.get().strip(' \t\n-'))
    if len(app.project_pm.get()) < 3:
        error("Enter a valid project manager name")
        return False
    if not app.project_type.get() in ['Revit', 'CAD', 'Other']:
        error("Select a project type (CAD, Revit or Other)")
        return False
    app.mode_label.set("// Mode: CREATE - Ready to GO. //")
    return True


def write(app):
    """
    Writes to file system based on the current mode.
    """
    if app.mode == 'create':
        if checkNewProject(app):
            createProject(app)
    elif app.mode == 'load':
        modifyProject(app)
    else:
        error("Invalid mode: {}".format(app.mode))


class Application(ttk.Frame):
    """
    Build the application window and initialize a project
    """
    # Initialize an empty project
    mode = 'create'
    next_pnum = "{}.{}".format(CURRENT_YEAR, getProjectNumber())

    def __init__(self, master=None):
        # Create the main frame
        ttk.Frame.__init__(self, master)
        # Create the communicating variables
        self.mode_label = tkinter.StringVar()
        self.mode_label.set("// Select Mode: Create new or Load existing. //")
        self.pnum = getProjectNumber()
        self.project_number = tkinter.StringVar()
        self.project_number.set(self.next_pnum)
        self.project_name = tkinter.StringVar()
        self.project_type = tkinter.StringVar()
        self.project_type.set('Revit')
        self.project_pm = tkinter.StringVar()
        self.project_addr = tkinter.StringVar()
        self.project_csz = tkinter.StringVar()
        self.billing_name = tkinter.StringVar()
        self.billing_addr = tkinter.StringVar()
        self.billing_csz = tkinter.StringVar()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """
        Create all the elements of the UI and connect to variables.
        """
        # Action buttons along the top
        cr = 0  # current row
        self.label1 = ttk.Label(self, text="Actions:", justify='right')
        self.label1.grid(row=cr, column=0)
        self.createButton = ttk.Button(
            self, text='Create', width=12,
            command=lambda: setMode(self, 'create'))
        self.createButton.grid(column=1, row=cr)

        self.updateButton = ttk.Button(
            self, text='Load', width=12,
            command=lambda: setMode(self, 'load'))
        self.updateButton.grid(column=2, row=cr)

        self.checkButton = ttk.Button(
            self, text='Write', width=12,
            command=lambda: write(self))
        self.checkButton.grid(column=3, row=cr)

        # Project number and name
        cr += 1
        self.basicsLabel = ttk.Label(self, padding=20,
                                     textvariable=self.mode_label)
        self.basicsLabel.grid(row=cr, columnspan=4)
        cr += 1
        self.label1 = ttk.Label(self, text="Project Number:", justify='right')
        self.label1.grid(row=cr, column=0)
        self.projectNumberEntry = ttk.Entry(self,
                                            textvariable=self.project_number)
        self.projectNumberEntry.grid(row=cr, column=1)
        self.label2 = ttk.Label(self, text="Project Name:", justify='right')
        self.label2.grid(row=cr, column=2)
        self.projectNameEntry = ttk.Entry(self, textvariable=self.project_name)
        self.projectNameEntry.grid(row=cr, column=3)

        # Project type (CAD or Revit or Other) and Project Manager
        cr += 1
        self.label3 = ttk.Label(self, text="Project Type:", justify='right')
        self.label3.grid(row=cr, column=0)
        self.projectTypeFrame = ttk.Frame(self, borderwidth=1)
        self.projectTypeFrame.grid(row=cr, column=1)
        self.cadRadio = ttk.Radiobutton(
            self.projectTypeFrame,
            text='CAD', value='CAD', variable=self.project_type)
        self.cadRadio.grid(row=0, column=1)
        self.revitRadio = ttk.Radiobutton(
            self.projectTypeFrame,
            text='Revit', value='Revit', variable=self.project_type)
        self.revitRadio.grid(row=0, column=2)
        self.otherRadio = ttk.Radiobutton(
            self.projectTypeFrame,
            text='Other', value='Other', variable=self.project_type)
        self.otherRadio.grid(row=0, column=3)

        self.label4 = ttk.Label(self, text="Project Manager:", justify='right')
        self.label4.grid(row=cr, column=2)
        self.projectManagerEntry = ttk.Entry(self,
                                             textvariable=self.project_pm)
        self.projectManagerEntry.grid(row=cr, column=3)

        # Project Address
        cr += 1
        self.labelAddress = ttk.Label(self,
                                      padding=20,
                                      text="// PROJECT AND "
                                      "BILLING ADDRESSES //")
        self.labelAddress.grid(row=cr, columnspan=4)
        cr += 1
        self.label5 = ttk.Label(self, text="Project Address:", justify='right')
        self.label5.grid(row=cr + 1, column=0)
        self.projectStreetEntry = ttk.Entry(self,
                                            textvariable=self.project_addr)
        self.projectStreetEntry.grid(row=cr + 1, column=1)
        self.label6 = ttk.Label(self, text="Project City,State,Zip:",
                                justify='right')
        self.label6.grid(row=cr + 2, column=0)
        self.projectCSZEntry = ttk.Entry(self, textvariable=self.project_csz)
        self.projectCSZEntry.grid(row=cr + 2, column=1)

        # Billing Name and Address
        self.label7 = ttk.Label(self, text="Billing Name:", justify='right')
        self.label7.grid(row=cr, column=2)
        self.billingNameEntry = ttk.Entry(self, textvariable=self.billing_name)
        self.billingNameEntry.grid(row=cr, column=3)
        self.label8 = ttk.Label(self, text="Billing Address:", justify='right')
        self.label8.grid(row=cr + 1, column=2)
        self.billingStreetEntry = ttk.Entry(self,
                                            textvariable=self.billing_addr)
        self.billingStreetEntry.grid(row=cr + 1, column=3)
        self.label9 = ttk.Label(self, text="Project City,State,Zip:",
                                justify='right')
        self.label9.grid(row=cr + 2, column=2)
        self.billingCSZEntry = ttk.Entry(self, textvariable=self.billing_csz)
        self.billingCSZEntry.grid(row=cr + 2, column=3)

        # Quit button at the bottom right
        cr += 3
        self.quitButton = ttk.Button(self, text='Quit',
                                     command=self.quit)
        self.quitButton.grid(column=3, row=cr
                             )


app = Application()
app.master.title('Project Create and Update')
app.mainloop()
