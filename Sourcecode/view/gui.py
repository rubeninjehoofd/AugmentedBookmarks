# Define directory
# ----------------------------------
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# Define imports
# ----------------------------------
import wx
from model.database import *
from controller.location import *

# Define class variables
location = Location()
db = App()

# Main frame
# ----------------------------------------------------------------------
class BERT_gui(wx.Frame):

    # Initialize 
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BERT - Augmented Bookmark")
        panel = wx.Panel(self, wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        buttons = [
            wx.Button(panel, label="Add person", name="addperson"),
            wx.Button(panel, label="Search person", name="searchperson"),
            wx.Button(panel, label="Location", name="location"),
            wx.Button(panel, label="Location", name="location"),
        ]

        for button in buttons:
            self.buildButtons(button, sizer)

        panel.SetSizer(sizer)

    # Create the buttons
    # ----------------------------------------------------------------------
    def buildButtons(self, btn, sizer):
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer.Add(btn, 0, wx.ALL, 5)

    # Function when buttons get pressed
    # ----------------------------------------------------------------------
    def onButton(self, event):
        button = event.GetEventObject()

        if button.GetLabel() == "Location":
            location.location()
        elif button.GetLabel() == "Add person":
            new_frame = createPerson_gui()
            self.Close()
            new_frame.Show()
        elif button.GetLabel() == "Search person":
            new_frame = findPerson_gui()
            self.Close()
            new_frame.Show()

# Create person frame
# ----------------------------------------------------------------------
class createPerson_gui(wx.Frame):

    # Initialize 
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BERT - Create person")
        panel = wx.Panel(self, wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        buttons = [
            wx.Button(panel, label="Home", name="home"),
            wx.Button(panel, label="Create person", name="createperson")
        ]

        for button in buttons:
            self.buildButtons(button, sizer)

        panel.SetSizer(sizer)

    # Create the buttons
    # ----------------------------------------------------------------------
    def buildButtons(self, btn, sizer):
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer.Add(btn, 0, wx.ALL, 5)

    # Function when buttons get pressed
    # ----------------------------------------------------------------------
    def onButton(self, event):
        button = event.GetEventObject()

        if button.GetLabel() == "Home":
            main_frame = BERT_gui()
            self.Close()
            main_frame.Show()
        elif button.GetLabel() == "Create person":
            db.create_person("Ruben")

# Find person frame
# ----------------------------------------------------------------------
class findPerson_gui(wx.Frame):

    # Initialize 
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BERT - Find person")
        panel = wx.Panel(self, wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        buttons = [
            wx.Button(panel, label="Home", name="home"),
            wx.Button(panel, label="Find person", name="Find person")
        ]

        for button in buttons:
            self.buildButtons(button, sizer)

        panel.SetSizer(sizer)

    # Create the buttons
    # ----------------------------------------------------------------------
    def buildButtons(self, btn, sizer):
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer.Add(btn, 0, wx.ALL, 5)

    # Function when buttons get pressed
    # ----------------------------------------------------------------------
    def onButton(self, event):
        button = event.GetEventObject()

        if button.GetLabel() == "Home":
            main_frame = BERT_gui()
            self.Close()
            main_frame.Show()
        elif button.GetLabel() == "Find person":
            db.find_person("Mark")

# Functions
# ----------------------------------------------------------------------
    

# Run the program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = BERT_gui()
    frame.Show()
    app.MainLoop()
