azkar v0.1
By ehab aboudaya

An Islamic azkar pop from quran, hadeeth and other text files.

Usage
./notify.py

will show a line from the files under textfiles directory and stores position.

./notify.py 1
will show a line from the files under textfiles directory and does NOT stores position.

The line number position is stored a settings file and will increment by one each time it is run or start from beginning.


install
just place all files under some directory and run as above.

dependencies
sudo apt-get install xsel
sudo apt-get install notify-osd

other info -  I use this script in cron as

*/10 * * * * export DISPLAY=:0 && path/prayer/notify.py > /tmp/py_error.txt 2>&1

notes
may allah reward my good intentions.
azkar text file was copied from  [ Sesame Soft ] Alnaseeha, Islamic reminder (Azkar)
http://download.exdat.com/alnaseeha_islamic_reminder_azkar/index-14478.html

