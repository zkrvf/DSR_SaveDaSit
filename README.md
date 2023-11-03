<h2 align="center">
<img src="src/logo.png" style="vertical-align: bottom">
  
DSR_SaveDaSit
</h2>

Ever wish there was an 'undo' button for that game mistake?" ⏪
Fed up with smacking innocent merchants in a plummeting capitalist society? 🤷‍♂️ 

<div align="center">
  <img src="src/hit.gif" width="200" />
</div>

> _No merchant was harmed in the making of this gif, at least in our timeline._

This project is your savior!🚀 
An automation tool for Dark Souls Remastered backups, taking you back in time where your in-game sins don't exist. Time travel without the DeLorean! 🕒🔙

⚠️ **DISCLAIMER:** _You're doing this at your own risk, I am not responsible for any data loss or damage that may occur._

## 📚 Table of Contents

- [How](#How)
- [Compile](#Compile)
- [Contribute](#Contribute)
- [License](#License)

## 📖 How

1. **Execution Options**:

   - **Using the Executable**:
     - Simply run `DSR_savedatsit.exe`.
     
   - **Using the Python Script**:
     - First, ensure you have all the dependencies resolved by installing them with:
       ```bash
       pip install -r requirements.txt
       ```
     - Then, run `DSR_savedatsit.py`.

<div align="center">
  <img src="src/gui.png" />
</div>

2. **Backup Tab**:
   - You'll find two main tabs: `Backup` and `Restore`.
   - In the `Backup` tab:
     - **Specify Save File Path**: Add the path to the save file. By default, it's located at `%USERPROFILE%\Documents\NBGI\DARK SOULS REMASTERED\123456`.
     - **Select Backup Destination**: Choose where you'd like the backups to be stored.
     - **Set Interval**: Define how often you want to create a backup (e.g., every 10 minutes).
     - **Start/Stop**: Once set, click on `Start Backup`. You can stop it whenever you wish.

3. **Restore Tab**:
   - In the `Restore` tab, you'll find:
     - **Backup List**: Displays all the backups made with brief details on their size and count.
     - **Buttons**:
       - `Update List`: Refreshes the backup list.
       - `Restore`: Allows you to restore from a selected backup.
       - `Modify`: Here, you can add a short descriptive text to your backup.

Happy gaming and safe saving! 🎮

## 🔧 Compile
```bash
git clone https://github.com/zkrvf/DSR_SaveDatSit
pip install pyinstaller
pyinstaller DSR_SaveDatSit.spec
```
## ➕ Contribute

Steps or guidelines for those wishing to contribute to the project. It might look something like:

    Fork the project.
    Create a new branch (git checkout -b my_new_branch).
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin my_new_branch).
    Open a new Pull Request.

## 📝 License
The GNU General Public License v3.0
