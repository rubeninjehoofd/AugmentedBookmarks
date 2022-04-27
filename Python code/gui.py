import wx
from location import *


# Define class variables
location = Location()

class BERT_gui(wx.Frame):

    # Initialize 
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "BERT - Augmented Bookmark")
        panel = wx.Panel(self, wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonOne = wx.Button(panel, label="One", name="one")
        buttonTwo = wx.Button(panel, label="Two", name="two")
        buttonThree = wx.Button(panel, label="Location", name="location")
        buttons = [buttonOne, buttonTwo, buttonThree]

        for button in buttons:
            self.buildButtons(button, sizer)

        panel.SetSizer(sizer)

    # Create the buttons
    # ----------------------------------------------------------------------
    def buildButtons(self, btn, sizer):
        """"""
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer.Add(btn, 0, wx.ALL, 5)

    # Function when buttons get pressed
    # ----------------------------------------------------------------------
    def onButton(self, event):

        # button = event.GetEventObject()
        # print("The button you pressed was labeled: " + str(button.GetLabel()))
        # print("The button's name is " + str(button.GetName()))

        button = event.GetEventObject()
        print("The button you pressed was labeled: " + str(button.GetLabel()))
        print("The button's name is " + str(button.GetName()))

        if button.GetLabel() == "Location":
            self.getLocation()

    # Functions
    # ----------------------------------------------------------------------
    def getLocation(self):
        location.location()

# Run the program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = BERT_gui()
    frame.Show()
    app.MainLoop()
