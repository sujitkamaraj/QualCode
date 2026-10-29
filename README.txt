QualCode - simple qualitative coding tool
=========================================

NEEDS: Python 3 (free, https://www.python.org/downloads/ - on Windows tick
"Add Python to PATH" during install). Nothing else to install. Any browser works.

HOW TO START
1. Keep this "QualCode" folder somewhere permanent (e.g. Documents).
2. Start it:
     Windows: double-click start.bat
     Mac:     double-click start.command (first time: right-click > Open)
     Or in a terminal inside this folder:  python server.py
3. Your browser opens at http://127.0.0.1:8765 . Keep the small black window
   open while you work; close it when you're done.

CODING
- Click "+ New", give the document a name, paste your text, click Create.
- Select any part of the text -> a box appears. Type a code; the dropdown shows
  codes you've used in all your documents and narrows as you type.
  Press Enter (or click) to apply. You can add several codes to the same selection.
- Click a highlight to see its codes or remove one.
- Click a code on the right to show only its highlights; use the pencil to rename,
  the x to remove it from the document.

WHAT GETS SAVED (automatically after every change)
QualCode/
  index.html, server.py, start.bat, start.command, README.txt
  Interview_P01/
    document.txt          <- your pasted text
    codes.csv             <- unique codes + frequency
    coded_segments.csv    <- code, highlighted text, position, memo, date
    project.json          <- full state, used to resume exactly where you left off
  Interview_P02/
    ...

The two export buttons download the same two CSVs on demand.
CSV files open correctly in Excel (UTF-8).

PICKING UP LATER
Run start.bat / start.command again - all documents are listed on the left and
the one you were last working on opens automatically.

NOTES
- Don't edit document.txt by hand after coding; highlights are stored by
  character position.
- To delete a document, delete its subfolder.
- Back up by copying the whole QualCode folder.
- The server only listens on your own computer (127.0.0.1); nothing is online.
