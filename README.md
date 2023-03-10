# TOML-UI
Short Description: Uses python to create a UI given a TOML file with comments included as ToolTips. Saves the values you enter.

This project was thought up while playing modded Minecraft dealing with all the TOML config files I wanted a quicker way to edit them. So, with the help of chatGPT, I created one. 

This UI changes true/false variables into red and green buttons, green representing true and red representing false. It obviously also displays the rest of the variables as well. Along with displaying the variables, it even has tooltips for when you hover over a variable and shows what comments belong to that variable. 

Variables with array entries have been given longer entry boxes determined by their length. One way to view these arrays is using the horizontal scrolling functionality which is used by holding ctrl and scrolling. Unfortunately I have not figured out a way to allow horizontal scrolling using a touch pad by just scrolling left and right, that still produces the Y (up and down) scrolling. 

There is a 'SAVE' and 'OPEN' button implemented to allow saving of the file under the EXACT same name and same location, so please keep that in mind, if you want a back-up, you will have to create it yourself. However, the saving of the file shouldn't remove the comments from it, so there shouldn't be any issue. However, I do believe there are still some errors opening a handful of files, but typically well made/properly made TOML files won't have issues. I will be slowly, hopefully, patching these issues out one by one. It also refuses to open any file other than a TOML file. It will tell you to enter a new file due to it not being a TOML. This way its less errors/crashes.

There is also a 'SEARCH' feature that allows you to search for a variable in the UI. It allows you to either put spaces in between your variable or not. It searches for both regardless. Once found it scrolls to that position/variable, and highlights it so you can see it better. If nothing is found, it remains in the same location, not scrolling, and puts 'No results found."

Along with those features, there is a 'DARK MODE' feature that allows you to change the UI into a dark mode version of itself. This saves for the session of the UI, but once you fully close the python script/UI, it no-longer remembers what you have selected. However, if you click open from the UI that is already open, it keeps that info, and opens it in Dark Mode again, this is what I mean by the 'session'. I didn't want to have to create a config file for the UI to rely on, as that forces people to download more than just this one file. This actually was the reason I had to change my true/false's, originally they were images, but I figured out a way to change them into just colors.

If you happen to create something better than I have created using my code/using it as a basis, all I ask is you link my UI/credit me in some way. Thanks and hope you enjoy!

Dark Mode:
![Image](https://user-images.githubusercontent.com/102988477/224393413-14f8af71-f1d4-454f-a27d-45788105f9ac.png)


Light Mode:
![Image](https://user-images.githubusercontent.com/102988477/224393476-7a4c6300-449e-46fe-85e3-0f6fd0d206ca.png)

Example of array entries stretching to allow more characters:
![Image](https://user-images.githubusercontent.com/102988477/224393605-2cafd3b4-13eb-4ec2-a061-95da63f73a6f.png)
