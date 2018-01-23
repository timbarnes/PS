#!/usr/bin/python

import tkinter as tk
import pprint
import utils

CURRENT_YEAR = '2018'
project_type = 'CAD'
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


class Application(tk.Frame):
    """
    Build the application window
    """

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        pn = utils.getProjectNumber()

    def createWidgets(self):
        # Action buttons along the top
        cr = 0  # current row
        self.label0 = tk.Label(self, text="Actions:", justify=tk.RIGHT)
        self.label0.grid(row=cr, column=0)
        self.createButton = tk.Button(self, text='Create', width=12,
                                      command=utils.create)
        self.createButton.grid(column=1, row=cr)

        self.updateButton = tk.Button(self, text='Update', width=12,
                                      command=utils.modify)
        self.updateButton.grid(column=2, row=cr)

        self.checkButton = tk.Button(self, text='Check', width=12,
                                     command=utils.check)
        self.checkButton.grid(column=3, row=cr)

        # Project number and name
        cr += 1
        self.labelBasics = tk.Label(self,
                                    pady=20,
                                    text="BASICS", justify='left')
        self.labelBasics.grid(row=cr, columnspan=4)
        cr += 1
        self.label1 = tk.Label(self, text="Project Number:", justify=tk.RIGHT)
        self.label1.grid(row=cr, column=0)
        self.projectNumberEntry = tk.Entry(self)
        self.projectNumberEntry.grid(row=cr, column=1)
        self.label2 = tk.Label(self, text="Project Name:", justify=tk.RIGHT)
        self.label2.grid(row=cr, column=2)
        self.projectNameEntry = tk.Entry(self)
        self.projectNameEntry.grid(row=cr, column=3)

        # Project type (CAD or Revit or Other) and Project Manager
        cr += 1
        self.label3 = tk.Label(self, text="Project Type:", justify='right')
        self.label3.grid(row=cr, column=0)
        self.projectTypeFrame = tk.Frame(self, borderwidth=1)
        self.projectTypeFrame.grid(row=cr, column=1)
        self.cadRadio = tk.Radiobutton(
            self.projectTypeFrame,
            text='CAD', value='CAD', variable=project_type)
        self.cadRadio.grid(row=0, column=1)
        self.revitRadio = tk.Radiobutton(
            self.projectTypeFrame,
            text='Revit', value='Revit', variable=project_type)
        self.revitRadio.grid(row=0, column=2)
        self.otherRadio = tk.Radiobutton(
            self.projectTypeFrame,
            text='Other', value='Other', variable=project_type)
        self.otherRadio.grid(row=0, column=3)

        self.label4 = tk.Label(self, text="Project Manager:", justify=tk.RIGHT)
        self.label4.grid(row=cr, column=2)
        self.projectManagerEntry = tk.Entry(self)
        self.projectManagerEntry.grid(row=cr, column=3)

        # Project Address
        cr += 1
        self.labelAddress = tk.Label(self,
                                     pady=20,
                                     text="PROJECT AND BILLING ADDRESSES")
        self.labelAddress.grid(row=cr, columnspan=4)
        cr += 1
        self.label5 = tk.Label(self, text="Project Address:", justify=tk.RIGHT)
        self.label5.grid(row=cr + 1, column=0)
        self.projectStreetEntry = tk.Entry(self)
        self.projectStreetEntry.grid(row=cr + 1, column=1)
        self.label6 = tk.Label(self, text="Project City,State,Zip:",
                               justify=tk.RIGHT)
        self.label6.grid(row=cr + 2, column=0)
        self.projectCSZEntry = tk.Entry(self)
        self.projectCSZEntry.grid(row=cr + 2, column=1)

        # Billing Name and Address
        self.label7 = tk.Label(self, text="Billing Name:", justify=tk.RIGHT)
        self.label7.grid(row=cr, column=2)
        self.billingNameEntry = tk.Entry(self)
        self.billingNameEntry.grid(row=cr, column=3)
        self.label8 = tk.Label(self, text="Billing Address:", justify=tk.RIGHT)
        self.label8.grid(row=cr + 1, column=2)
        self.billingStreetEntry = tk.Entry(self)
        self.billingStreetEntry.grid(row=cr + 1, column=3)
        self.label9 = tk.Label(self, text="Project City,State,Zip:",
                               justify=tk.RIGHT)
        self.label9.grid(row=cr + 2, column=2)
        self.billingCSZEntry = tk.Entry(self)
        self.billingCSZEntry.grid(row=cr + 2, column=3)

        # Quit button at the bottom right
        cr += 3
        self.quitButton = tk.Button(self, text='Quit',
                                    command=self.quit)
        self.quitButton.grid(column=3, row=cr
                             )


app = Application()
app.master.title('Project Create and Update')
app.mainloop()
