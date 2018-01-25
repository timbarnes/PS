#!/usr/bin/python
import tkinter
from tkinter import ttk
import utils as u

CURRENT_YEAR = '2018'
project_type = 'CAD'

pn = u.getProjectNumber()

project_data = {
    'year': pn[0],
    'number': pn[1],
    'type': project_type,
    'project_manager': '',
    'project_address': '',
    'project_csz': '',
    'billing_contact': '',
    'billing_address': '',
    'billing_csz': '',
    'validated': False,
}


class Application(ttk.Frame):
    """
    Build the application window
    """

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        project_type = tkinter.StringVar()
        project_type.set('Revit')
        # Action buttons along the top
        cr = 0  # current row
        self.label0 = ttk.Label(self, text="Actions:", justify='right')
        self.label0.grid(row=cr, column=0)
        self.createButton = ttk.Button(self, text='Create', width=12,
                                       command=u.create)
        self.createButton.grid(column=1, row=cr)

        self.updateButton = ttk.Button(self, text='Update', width=12,
                                       command=u.modify)
        self.updateButton.grid(column=2, row=cr)

        self.checkButton = ttk.Button(self, text='Check', width=12,
                                      command=u.check)
        self.checkButton.grid(column=3, row=cr)

        # Project number and name
        cr += 1
        next_project = u.getProjectNumber()
        label_string = "// BASICS // Next project number is: "
        label_string += "{:04d}.{:03d}".format(next_project[0], next_project[1])
        self.basicsLabel = ttk.Label(self, padding=20, text=label_string)
        self.basicsLabel.grid(row=cr, columnspan=4)
        cr += 1
        self.label1 = ttk.Label(self, text="Project Number:", justify='right')
        self.label1.grid(row=cr, column=0)
        self.projectNumberEntry = ttk.Entry(self)
        self.projectNumberEntry.grid(row=cr, column=1)
        self.label2 = ttk.Label(self, text="Project Name:", justify='right')
        self.label2.grid(row=cr, column=2)
        self.projectNameEntry = ttk.Entry(self)
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
        self.projectManagerEntry = ttk.Entry(self)
        self.projectManagerEntry.grid(row=cr, column=3)

        # Project Address
        cr += 1
        self.labelAddress = ttk.Label(self,
                                      padding=20,
                                      text="// PROJECT AND BILLING ADDRESSES //")
        self.labelAddress.grid(row=cr, columnspan=4)
        cr += 1
        self.label5 = ttk.Label(self, text="Project Address:", justify='right')
        self.label5.grid(row=cr + 1, column=0)
        self.projectStreetEntry = ttk.Entry(self)
        self.projectStreetEntry.grid(row=cr + 1, column=1)
        self.label6 = ttk.Label(self, text="Project City,State,Zip:",
                                justify='right')
        self.label6.grid(row=cr + 2, column=0)
        self.projectCSZEntry = ttk.Entry(self)
        self.projectCSZEntry.grid(row=cr + 2, column=1)

        # Billing Name and Address
        self.label7 = ttk.Label(self, text="Billing Name:", justify='right')
        self.label7.grid(row=cr, column=2)
        self.billingNameEntry = ttk.Entry(self)
        self.billingNameEntry.grid(row=cr, column=3)
        self.label8 = ttk.Label(self, text="Billing Address:", justify='right')
        self.label8.grid(row=cr + 1, column=2)
        self.billingStreetEntry = ttk.Entry(self)
        self.billingStreetEntry.grid(row=cr + 1, column=3)
        self.label9 = ttk.Label(self, text="Project City,State,Zip:",
                                justify='right')
        self.label9.grid(row=cr + 2, column=2)
        self.billingCSZEntry = ttk.Entry(self)
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
