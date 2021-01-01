from combo_client import ComboSentenceSplitter

text="""
Add-ons are like apps that you can install to make Firefox work the way you want.

    1. Click the menu button Fx57menu , click Fx57Addons-icon Add-ons and select Recommendations.
    2. To install a recommended add-on, click the blue + Install Theme or + Add to Firefox button, depending on the type of add-on. 

At the bottom of the list of recommended add-ons, there's also a Find more add-ons button you can click. It will take you to addons.mozilla.org where you can search for specific add-ons.

To learn more about add-ons, see Find and install add-ons to add features to Firefox. 
"""

splitter = ComboSentenceSplitter()

sentences = splitter.combo_split(text)

print(sentences)
