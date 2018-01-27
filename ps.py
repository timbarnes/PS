#
import os
import tkinter
from tkinter import ttk

CURRENT_YEAR = '2018'
project_type = 'CAD'
PROJECT_ROOT = '.'
ready = False
FOLDER_LIST = os.listdir(PROJECT_ROOT)


def error(message):
    """
    Print an error to a pop-up and set ready to False.
    """
    w = tkinter.Toplevel()
    w.title = "Error"
    m = tkinter.Message(w, text=message, width=400)
    m.grid(row=0, column=0, pady=20)
    e = ttk.Button(w, text="OK", command=w.destroy)
    e.grid(row=1, column=0, pady=20)
    print("Error: {}".format(message))
    ready = False


def getProjectNumber():
    """
    Get the number of the most recent project,
    and return the next number up as a 2 or 3 digit string..
    """
    fileList = filter(lambda x: x[:4] == CURRENT_YEAR,
                      FOLDER_LIST)
    try:
        latestProject = sorted(fileList, reverse=True)[0]
        projectNumber = int(latestProject[5:8])
        return (CURRENT_YEAR, projectNumber + 1)
    except IndexError:
        print("No projects found.")
        return ('0000', '000')


def getProjectData(pn):
    """
    Get information for a given project and return a dictionary.
    Return False if there's no such project.
    pn is a string representing the project number
    """
    result = {}
    l = len(pn)
    pf = [x for x in FOLDER_LIST if x[:l] == pn]
    if len(pf) == 1:
        # We found the folder
        result['project_number'] = pn
        result['project_name'] = pf[pn:]
    else:
        return False


def makeProjectFolder(name):
    """
    Create the project name and create the folder for it.
    """
    folderName = CURRENT_YEAR + '.' + getProjectNumber() + ' - ' + name
    os.mkdir(folderName)


def createProject():
    """
    Create a new project using pre-validated information.
    """
    print(("Creating Project '{} - {}'"
           "for {}.").format(app.project_number.get(),
                             app.project_name.get(),
                             app.project_pm.get()))


def modifyProject():
    """
    Alter project information for an existing project.
    """
    pass


def checkProject():
    """
    Check data prior to creating or modifying a project.
    If a project number is specified, and exists, fill in the missing data.
    If it doesn't exist, fill in the next project number, and check
    that project data is accurate
    """
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
        return True
    else:
        # We're modifying an existing project_type:
        # Start by pulling in existing data for the project
        data = getProjectData(project_number)
        if data:
            app.project_name.set(data['project_name'])
            app.project_pm.set(data['project_pm'])
            app.project_addr.set(data['project_addr'])
            app.project_csz.set(data['project_csz'])
            app.billing_name.set(data['billing_name'])
            app.billing_addr.set(data['billing_addr'])
            app.billing_csz.set(data['billing_csz'])
        else:
            error("No such project: {}".format(project_number))


# pn=getProjectNumber()

# project_data = {
#     'year': pn[0],
#     'number': pn[1],
#     'type': project_type,
#     'project_manager': '',
#     'project_address': '',
#     'project_csz': '',
#     'billing_contact': '',
#     'billing_address': '',
#     'billing_csz': '',
#     'validated': False,
# }


class Application(ttk.Frame):
    """
    Build the application window
    """

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.project_number = tkinter.StringVar()
        self.project_number.set('-')
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
        # Action buttons along the top
        cr = 0  # current row
        self.label0 = ttk.Label(self, text="Actions:", justify='right')
        self.label0.grid(row=cr, column=0)
        self.createButton = ttk.Button(self, text='Create', width=12,
                                       command=createProject)
        self.createButton.grid(column=1, row=cr)

        self.updateButton = ttk.Button(self, text='Update', width=12,
                                       command=modifyProject)
        self.updateButton.grid(column=2, row=cr)

        self.checkButton = ttk.Button(self, text='Check', width=12,
                                      command=checkProject)
        self.checkButton.grid(column=3, row=cr)

        # Project number and name
        cr += 1
        next_project = getProjectNumber()
        label_string = "// BASICS // Next project number is: "
        label_string += "{}.{}".format(*next_project)
        self.basicsLabel = ttk.Label(self, padding=20, text=label_string)
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
