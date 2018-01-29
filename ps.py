#
import os
import datetime
import tkinter
from tkinter import ttk
import openpyxl

CURRENT_YEAR = datetime.datetime.now().year  # This year
PROJECT_ROOT = '.'                        # Where we look (P drive)
project_type = 'CAD'                      # Default to CAD
ready = False                             # Has project been validated?
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
    Print an error to a pop-up and set ready to False.
    """
    global ready
    popup("Error: {}".format(message))
    ready = False


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


def getProjectData(app):
    """
    Get information for a given project and instantiate in the GUI.
    Return False if there's no such project.
    """
    pnum = app.project_number.get()
    length = len(pnum)
    pfolder = [x for x in FOLDER_LIST if x[: length] == pnum]
    if len(pfolder) == 1:
        # We found the folder: return a tuple of fullname, number and name
        pname = pfolder[0][9:]
        while pname[0] in ['-', ' ']:
            pname = pname[1:]
        app.project_name.set(pname)
        return (pfolder[0], pnum, pname)
    else:
        error("getProjectData: No such project: {}".format(pnum))
        return False


def makeProjectFolder(app):
    """
    Create the project name and create the folder for it.
    Assumes data has been validated.
    """
    folderName = "{} - {}".format(app.project_number.get(),
                                  app.project_name.get())
    try:
        os.mkdir(folderName)
        popup("Folder {} created".format(folderName))
    except FileExistsError:
        error("makeProjectFolder: Folder already exists")


def copyFiles(app, folder):
    """
    Copy files based on project type to the pre-created folder.
    """
    if app.mode == 'CAD':
        # Copy CAD files
        pass
    elif app.mode == 'Revit':
        # Copy Revit files
        pass
    else:
        # 02 Folder only
        pass


def readProjectData(app):
    """
    Read project information from an Excel template file.
    """
    filename = "{} - {}".format(app.project_number, app.project_name)
    print('Opening file: %s', fileName)
    pf = openpyxl.load_workbook(fileName)
    sheet = pf.active
    app.project_pm.set(sheet['B6'])
    app.project_type.set(sheet['B7'])
    app.project_addr.set(sheet['B9'])
    app.project_csz.set(sheet['B10'])
    app.billing_name.set(sheet['B12'])
    app.billing_title.set(sheet['B13'])
    app.billing_addr.set(sheet['B17'])
    app.csz.set(sheet['B18'])


def setMode(app, mode):
    """
    Sets the mode to 'create' or 'modify' based on button press.
    """
    app.mode = mode
    if mode == 'create':
        app.project_number.set(app.next_pnum)
        app.mode_label.set("// Mode: CREATE - Enter name, type, and PM. //")
    if app.mode == 'modify':
        app.mode_label.set("// Mode: UPDATE - Enter Project Number //")
        app.project_number.set('-.-')


def createProject(app):
    """
    Create a new project using pre-validated information.
    """
    global ready
    if not app.mode == 'create':
        error('createProject: Mode not set to create')
        ready = False
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
    print("Modify project {}".format(app.project_number.get()))


def checkNewProject(app):
    """
    Check data prior to creating a project.
    """
    global ready
    project_number = app.project_number.get()
    if len(project_number) < 7:
        # We're creating a new project
        project_number = "{:4}.{:}".format(*getProjectNumber())
        app.project_number.set(project_number)
        if len(app.project_name.get()) < 6:
            error("Please provide a descriptive project name.")
            return False
        if len(app.project_pm.get()) < 3:
            error("Enter a valid project manager name")
            return False
        ready = True
        return True


def checkProject(app):
    """
    Either check elements of a new project, or load an existing project.
    """
    if app.mode == 'create':
        checkNewProject(app)
    elif app.mode == 'modify':
        result = getProjectData(app)
        if result:
            # Set up the information retrieved.
            pass
    else:
        error("checkProject: Invalid mode")


def go(app):
    """
    Executes a function based on the current mode.
    """
    if app.mode == 'create':
        createProject(app)
    elif app.mode == 'modify':
        modifyProject(app)
    else:
        error("Invalid mode: {}".format(app.mode))


class Application(ttk.Frame):
    """
    Build the application window and initialize a project
    """
    # Initialize an empty project
    mode = 'Create'
    next_pnum = "{}.{}".format(CURRENT_YEAR, getProjectNumber())

    def __init__(self, master=None):
        # Create the main frame
        ttk.Frame.__init__(self, master)
        # Create the communicating variables
        self.mode_label = tkinter.StringVar()
        self.mode_label.set("// Select Mode: Create or Update. //")
        self.pnum = getProjectNumber()
        self.project_number = tkinter.StringVar()
        self.project_number.set(self.next_pnum)
        self.project_name = tkinter.StringVar()
        self.project_name.set('-')
        self.project_type = tkinter.StringVar()
        self.project_type.set('Revit')
        self.project_pm = tkinter.StringVar()
        self.project_pm.set('-')
        self.project_addr = tkinter.StringVar()
        self.project_addr.set('-')
        self.project_csz = tkinter.StringVar()
        self.project_csz.set('-')
        self.billing_name = tkinter.StringVar()
        self.billing_name.set('-')
        self.billing_addr = tkinter.StringVar()
        self.billing_addr.set('-')
        self.billing_csz = tkinter.StringVar()
        self.billing_csz.set('-')
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """
        Create all the elements of the UI and connect to variables.
        """
        # Action buttons along the top
        cr = 0  # current row
        self.createButton = ttk.Button(
            self, text='Create', width=12,
            command=lambda: setMode(self, 'create'))
        self.createButton.grid(column=0, row=cr)

        self.updateButton = ttk.Button(
            self, text='Update', width=12,
            command=lambda: setMode(self, 'modify'))
        self.updateButton.grid(column=1, row=cr)

        self.createButton = ttk.Button(
            self, text='Check', width=12,
            command=lambda: checkProject(self))
        self.createButton.grid(column=2, row=cr)

        self.checkButton = ttk.Button(
            self, text='GO', width=12,
            command=lambda: go(self))
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
            text='CAD', value='CAD', variable=project_type)
        self.cadRadio.grid(row=0, column=1)
        self.revitRadio = ttk.Radiobutton(
            self.projectTypeFrame,
            text='Revit', value='Revit', variable=project_type)
        self.revitRadio.grid(row=0, column=2)
        self.otherRadio = ttk.Radiobutton(
            self.projectTypeFrame,
            text='Other', value='Other', variable=project_type)
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
