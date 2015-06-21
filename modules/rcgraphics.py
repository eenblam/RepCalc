"""
rcgraphics.py
-------------
Graphical component of RepCalc.
"""
import sys
import os
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import modules.rcfuncs as rcf

# Application inherits from tk.Frame
class Application(tk.Frame):
    """
    #TODO Document this class
    #TODO Document all class methods
    """
    def __init__(self,master=None):
        # Call constructor of parent class
        tk.Frame.__init__(self, master)
        # Place application on screen
        self.grid()
        self.__createWidgets()
        
    def __createWidgets(self):
        # Create ALL elements/widgets

        # Import help docs
        try:
            print(rcf.LOCAL_PATH) #TESTCODE
            self.help_dict = rcf.gethelp(os.path.join(rcf.LOCAL_PATH,"data", "helpstrings.txt"))
        except IOError:
            helpkeys = ["TE", "ROI", "OUTPUT", "CONFIG", "ANALTYPE", "REGIONLENGTH"]
            self.help_dict = {}
            for key in helpkeys:
                self.help_dict[key] = "helpstrings.txt not found."
            print("helpstrings.txt not found.") #TESTCODE

        # fas file Button
        def fashandler(event, self=self):
            return self.__fasHandler(event)

        self.fasName = tk.StringVar()

        self.fasButton = tk.Button(self, 
            text='Transposable element annotation file', 
            command=fashandler)
        self.fasButton.grid(row=0, columnspan=3, sticky=tk.E+tk.W)       
        self.fasButton.bind('<1>', fashandler)

        def fashelphandler(event, self=self):
            return self.__fasHelpHandler(event)

        self.fasHelpButton = tk.Button(self,
            text="?",
            command=fashelphandler)
        self.fasHelpButton.bind('<1>', fashelphandler)
        self.fasHelpButton.grid(row=0, column=3, sticky=tk.E+tk.W)

        # fas column numbers
        self.fasColLabel1 = tk.Label(self,
            text='Repeat Class')
        self.fasColLabel1.grid(row=1, column=0)
        self.fasColLength1 = tk.StringVar()
        self.fasColLength1.set('0')
        self.fasColEntry1 = tk.Entry(self,
            textvariable=self.fasColLength1,
            justify=tk.CENTER)
        self.fasColEntry1.grid(row=2, column=0)

        self.fasColLabel2 = tk.Label(self,
            text='Chromosome')
        self.fasColLabel2.grid(row=1, column=1)
        self.fasColLength2 = tk.StringVar()
        self.fasColLength2.set('1')
        self.fasColEntry2 = tk.Entry(self,
            textvariable=self.fasColLength2,
            justify=tk.CENTER)
        self.fasColEntry2.grid(row=2, column=1)

        self.fasColLabel3 = tk.Label(self,
            text='Start')
        self.fasColLabel3.grid(row=1, column=2)
        self.fasColLength3 = tk.StringVar()
        self.fasColLength3.set('2')
        self.fasColEntry3 = tk.Entry(self,
            textvariable=self.fasColLength3,
            justify=tk.CENTER)
        self.fasColEntry3.grid(row=2, column=2)

        self.fasColLabel4 = tk.Label(self,
            text='End')
        self.fasColLabel4.grid(row=1, column=3)
        self.fasColLength4 = tk.StringVar()
        self.fasColLength4.set('3')
        self.fasColEntry4 = tk.Entry(self,
            textvariable=self.fasColLength4,
            justify=tk.CENTER)
        self.fasColEntry4.grid(row=2, column=3)


        # pi file Button
        def pihandler(event, self=self):
            return self.__piHandler(event)
        self.piName = tk.StringVar()
        # Set default piName to empty to allow for analysisA.
        self.piName.set('')
        self.piButton = tk.Button(self, 
            text='Ranges of regions of interest', 
            command=pihandler)
        self.piButton.grid(row=3, columnspan=3, sticky=tk.E+tk.W)
        self.piButton.bind('<1>', pihandler)

        def pihelphandler(event, self=self):
            return self.__piHelpHandler(event)

        self.piHelpButton = tk.Button(self,
            text="?",
            command=pihelphandler)
        self.piHelpButton.bind('<1>', pihelphandler)
        self.piHelpButton.grid(row=3, column=3, sticky=tk.E+tk.W)

        # pi column numbers
        self.piColLabel1 = tk.Label(self,
            text='ID')
        self.piColLabel1.grid(row=4, column=0)
        self.piColLength1 = tk.StringVar()
        self.piColLength1.set('0')
        self.piColEntry1 = tk.Entry(self,
            textvariable=self.piColLength1,
            justify=tk.CENTER)
        self.piColEntry1.grid(row=5, column=0)

        self.piColLabel2 = tk.Label(self,
            text='Chromosome')
        self.piColLabel2.grid(row=4, column=1)
        self.piColLength2 = tk.StringVar()
        self.piColLength2.set('1')
        self.piColEntry2 = tk.Entry(self,
            textvariable=self.piColLength2,
            justify=tk.CENTER)
        self.piColEntry2.grid(row=5, column=1)

        self.piColLabel3 = tk.Label(self,
            text='Start')
        self.piColLabel3.grid(row=4, column=2)
        self.piColLength3 = tk.StringVar()
        self.piColLength3.set('2')
        self.piColEntry3 = tk.Entry(self,
            textvariable=self.piColLength3,
            justify=tk.CENTER)
        self.piColEntry3.grid(row=5, column=2)

        self.piColLabel4 = tk.Label(self,
            text='End')
        self.piColLabel4.grid(row=4, column=3)
        self.piColLength4 = tk.StringVar()
        self.piColLength4.set('3')
        self.piColEntry4 = tk.Entry(self,
            textvariable=self.piColLength4,
            justify=tk.CENTER)
        self.piColEntry4.grid(row=5, column=3)

        # output file Button
        def outhandler(event, self=self):
            return self.__outHandler(event)
        self.outName = tk.StringVar()
        self.outButton = tk.Button(self, 
            text='Output file', 
            command=outhandler)
        self.outButton.grid(row=6, columnspan=3, sticky=tk.E+tk.W)
        self.outButton.bind('<1>', outhandler)

        def outhelphandler(event, self=self):
            return self.__outHelpHandler(event)

        self.outHelpButton = tk.Button(self,
            text="?",
            command=outhelphandler)
        self.outHelpButton.bind('<1>', outhelphandler)
        self.outHelpButton.grid(row=6, column=3, sticky=tk.E+tk.W)


        # config file Button
        def confhandler(event, self=self):
            return self.__confHandler(event)
        self.confName = tk.StringVar()
        # Set empty config as default.
        self.confName.set('')
        self.confButton = tk.Button(self, 
            text='Config File (optional)', 
            command=confhandler)
        self.confButton.grid(row=7, columnspan=3, sticky=tk.E+tk.W)
        self.confButton.bind('<1>', confhandler)

        def confhelphandler(event, self=self):
            return self.__confHelpHandler(event)

        self.confHelpButton = tk.Button(self,
            text="?",
            command=confhelphandler)
        self.confHelpButton.bind('<1>', confhelphandler)
        self.confHelpButton.grid(row=7, column=3, sticky=tk.E+tk.W)

        # Choose analysis type - Radiobuttons
        # a, b, c map to analysisA, analysisB, and analysisC, respectively.
        # analType keys into a command dict in __runHandler.
        self.analType = tk.StringVar()
        self.analType.set('b')

        def ahandler(self=self):
            self.lengthEntry.configure(state=tk.NORMAL)
            self.transposeCB.configure(state=tk.DISABLED)

            self.fasColEntry2.configure(state=tk.DISABLED)
            self.piColEntry1.configure(state=tk.DISABLED)
            self.piColEntry2.configure(state=tk.DISABLED)
            self.piColEntry3.configure(state=tk.DISABLED)
            self.piColEntry4.configure(state=tk.DISABLED)

        def bhandler(self=self):
            self.lengthEntry.configure(state=tk.NORMAL)
            self.transposeCB.configure(state=tk.DISABLED)

            self.fasColEntry2.configure(state=tk.NORMAL)
            self.piColEntry1.configure(state=tk.DISABLED)
            self.piColEntry2.configure(state=tk.NORMAL)
            self.piColEntry3.configure(state=tk.NORMAL)
            self.piColEntry4.configure(state=tk.NORMAL)

        def chandler(self=self):
            self.lengthEntry.configure(state=tk.DISABLED)
            self.transposeCB.configure(state=tk.NORMAL)

            self.fasColEntry2.configure(state=tk.NORMAL)
            self.piColEntry1.configure(state=tk.NORMAL)
            self.piColEntry2.configure(state=tk.NORMAL)
            self.piColEntry3.configure(state=tk.NORMAL)
            self.piColEntry4.configure(state=tk.NORMAL)

        self.aRadio = tk.Radiobutton(self,
            text='TE density within the whole genome (WG)',
            variable=self.analType,
            value='a',
            command=ahandler)
        self.aRadio.grid(row=8,columnspan=3)

        self.bRadio = tk.Radiobutton(self, 
            text='TE density within regions of interest (ROI)', 
            variable=self.analType,  
            value='b',
            command=bhandler)
        self.bRadio.grid(row=9, columnspan=3)

        self.cRadio = tk.Radiobutton(self,
            text='TE families/subfamilies distribution within regions of interest (MXROI)', 
            variable=self.analType, 
            value='c',
            command=chandler)
        self.cRadio.grid(row=10, columnspan=3)

        def analhelphandler(event, self=self):
            return self.__analHelpHandler(event)

        self.analHelpButton = tk.Button(self,
            text="?",
            command=analhelphandler)
        self.analHelpButton.bind('<1>', analhelphandler)
        self.analHelpButton.grid(row=8, column=3, sticky=tk.E+tk.W)

        # Specify region_length, when applicable.
        self.lengthLabel = tk.Label(self,
            text='Please specify the length of the region below.')
        self.lengthLabel.grid(row=11, columnspan=3, sticky=tk.E+tk.W)
        
        self.regionLength = tk.StringVar()
        self.lengthEntry = tk.Entry(self,
            textvariable=self.regionLength)
        self.lengthEntry.grid(row=12, columnspan=3, sticky=tk.E+tk.W)

        def regionhelphandler(event, self=self):
            return self.__regionHelpHandler(event)

        self.regionHelpButton = tk.Button(self,
            text="?",
            command=regionhelphandler)
        self.regionHelpButton.bind('<1>', regionhelphandler)
        self.regionHelpButton.grid(row=11, column=3, sticky=tk.E+tk.W)

        # Transpose CB
        self.transposeVar = tk.IntVar()
        self.transposeVar.set(0)
        self.transposeCB = tk.Checkbutton(self, 
            text='Transpose matrix output?', 
            variable=self.transposeVar,
            state=tk.DISABLED)
        self.transposeCB.grid(row=13, column=1)

        # Run Button
        def runhandler(event, self=self):
            return self.__runHandler(event)
        self.runButton = tk.Button(self,
            text='Run',
            command=runhandler)
        self.runButton.bind('<1>', runhandler)
        self.runButton.grid(row=14, columnspan=3, sticky=tk.E+tk.W)

        # Quit Button
        self.quitButton = tk.Button(self, 
            text='Quit', 
            command=self.quit)
        self.quitButton.grid(row=14, column=3, sticky=tk.E+tk.W)

    def __fasHandler(self, event):
        self.fasName.set(fd.askopenfilename( defaultextension='.fas'))

    def __fasHelpHandler(self, event):
        mb.showinfo("TE data (.fas)",
            self.help_dict["TE"])

    def __piHandler(self, event):
        self.piName.set(fd.askopenfilename( defaultextension='.gff'))

    def __piHelpHandler(self, event):
        mb.showinfo("Regions of Interest",
            self.help_dict["ROI"])

    def __outHandler(self, event):
        self.outName.set(fd.asksaveasfilename( defaultextension='.txt'))

    def __outHelpHandler(self, event):
        mb.showinfo("Output",
            self.help_dict["OUTPUT"])

    def __confHandler(self, event):
        self.confName.set(fd.askopenfilename( defaultextension='.conf'))

    def __confHelpHandler(self, event):
        mb.showinfo("Specify configuration file.",
            self.help_dict["CONFIG"])

    def __analHelpHandler(self, event):
        mb.showinfo("Specify analysis type.",
            self.help_dict["ANALTYPE"])

    def __regionHelpHandler(self, event):
        mb.showinfo("Determine region length",
            self.help_dict["REGIONLENGTH"])

    def __runHandler(self, event):

        # Load control variables into locals, for future conciseness.
        anal_type = self.analType.get()
        transpose = bool(self.transposeVar.get())
        region_length = int(self.regionLength.get())

        fcl1 = self.fasColLength1.get()
        fcl2 = self.fasColLength2.get()
        fcl3 = self.fasColLength3.get()
        fcl4 = self.fasColLength4.get()


        pcl1 = self.piColLength1.get() 
        pcl2 = self.piColLength2.get()
        pcl3 = self.piColLength3.get()
        pcl4 = self.piColLength4.get()


        # Handle data input.
        fas_filename = self.fasName.get()
        pi_filename = self.piName.get()

        out_filename = self.outName.get()
        conf_filename = self.confName.get()
        config_dict = rcf.getconfig(conf_filename)

        a = anal_type is 'a'
        b = anal_type is 'b'
        c = anal_type is 'c'

        opt_dict = {'a': a, 'b': b, 'c': c, 't': transpose, 'A': True, 'B': True}

        if a:
            # fcl2 not needed; pi_columns not needed
            fas_columns = [fcl1, fcl3, fcl4]
            args = [region_length, fas_filename] + fas_columns + [out_filename]

        if b:
            # pcl1 not needed
            fas_columns = [fcl1, fcl2, fcl3, fcl4]
            p_columns = [pcl2, pcl3, pcl4]
            args = [region_length, fas_filename] + fas_columns + \
                [pi_filename] + pi_columns + [out_filename]

        if c:
            # All 8 columns elements must be specified.
            fas_columns = [fcl1, fcl2, fcl3, fcl4]
            p_columns = [pcl1, pcl2, pcl3, pcl4]
            args = [fas_filename] + fas_columns + \
                [pi_filename] + pi_columns + [out_filename]

        if conf_filename:
            args.append(conf_filename)

        commands = {'a': rcf.analysisA,
            'b': rcf.analysisB,
            'c': rcf.analysisC,}

        result = commands[anal_type](args)

        result_dict = {0: 'Program complete!',
            1: 'Column indexing error.  No output written.',
            2: 'Column value error.  Please provide positive integer values for column indices.  No output written.',
            3: 'Length error.  No output written.  Please provide a valid length.',}

        mb.showinfo("Run",
            result_dict[result])

    def centerWindow(self):
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        
        self.master.geometry('+%d+%d' % (x,y))

def maingui():
    """
    #TODO Document this function
    """
    app = Application()
    # Set title of the window to 'Sample application'
    app.master.title('RepCalc')
    #app.master.geometry("250x150+300+300")
    #app.master.geometry("+300+300")
    app.centerWindow()
    # Main loop; wait for mouse and keyboard events
    app.mainloop()
