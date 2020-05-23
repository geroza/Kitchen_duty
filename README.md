# Kitchen_duty
Script for scheduling kitchen duties
## 1. Initial setup.
Get a .csv list of all the people in the house sorted by how long ago it was that they have done kitchen duty(the ones who didn't do it the longest on the top, the ones that did it most recently on the bottom), with their room numbers in the next column, and write the unavailabilities in the next column. The unavailabilities have to days of the month written either as lone numbers or as an interval of days, the entries must be separated by spaces. For example:

|      |   |        |
|------|---|-------|
| Anna |1| 12 23 |
| Biff  |2| 14 18-24|
| Chad |3| 12-30   |

Place that .csv file inside the unavailability folder and input it's name when asked for unavailability list. Enter month and enter year.
In the folder bottle_schedule the Bottle duty schedule will appear and in the folder kitchen_schedule the kitchen duty schedule will appear. In the Unavailability folder the Unavailability list for the next month will appear.
## 2 Subsequent scheduling
Get the Unavailability list from the Unavailabilty folder and fill it out (as before) with the unavailability dates. Input the file name when prompted. Enter month and enter year.
In the folder bottle_schedule the Bottle duty schedule will appear and in the folder kitchen_schedule the kitchen duty schedule will appear.
## 3 Sending E-mails
In order to send a personalized email to everyone on the Kitchen and Bottle duty schedules press y when being asked. You need to provide a csv file with the names in one column and the email adresses in the other. For example:
|      |        |
|------|-------|
| Anna | anna@email.com |
| Biff  | biff@email.com|
| Chad | chad@email.com|

You will also need to provide an gmail account (with IMAP/POP enabled, [less secure apps acces allowed](https://support.google.com/accounts/answer/6010255), [app-specific passwords created](https://support.google.com/accounts/answer/185833)(if you have two factor authorization turned on)) and it's password. I recommed using a throwaway email, since this is not the most secure. If you get a authentication error try [Display unlock capcha](https://accounts.google.com/DisplayUnlockCaptcha).
## 4 Improvements
If you have improvement ideas leave a comment or edit the script.
