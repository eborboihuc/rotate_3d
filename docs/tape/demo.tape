# This file describes terminal videos with the `vhs` tool 
# See https://github.com/charmbracelet/vhs for docs
Output img/demo.chafa.gif 
Require "docker"
Set Shell "sh"
Set FontSize 16
Set Width 800
Set Height 800
Set TypingSpeed .05
Set PlaybackSpeed 1
Set CursorBlink false
Type "python imgrot.py img/icon.png --display --stretch --bg lightblue"
Sleep 1.1
Enter
Sleep 30

