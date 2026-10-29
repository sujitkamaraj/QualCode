# QualCode

A simple qualitative coding tool that runs in your browser and saves everything to folders on your computer.

**Needs:** Python 3 ([python.org/downloads](https://www.python.org/downloads/)). On Windows, tick **"Add Python to PATH"** during install. Nothing else to install, and any browser works.

---

## Starting the tool

1. Keep the `QualCode` folder somewhere permanent (e.g. Documents).
2. Start it:
   - **Windows:** double-click `start.bat`
   - **Mac:** double-click `start.command` (first time: right-click → **Open**)
   - **Or** in a terminal inside the folder: `python server.py`
3. Your browser opens at <http://127.0.0.1:8765>. Keep the small terminal window open while you work, and close it when you're done.

## Adding a document

Click **+ New**, give the document a name, paste your text, and click **Create**.

## Coding

- **Select** (drag over) any part of the text and a coding box appears.
- **Type a code.** The dropdown shows codes you've used across *all* your documents and narrows as you type. Press **Enter** (or click a code) to apply it.
- **↑ / ↓** pick from the list, and **Esc** closes the box.
- Add as many codes to the same passage as you like.
- **Memo** (optional) is a note on why you applied that code, e.g. *"sarcastic tone"*. It's saved in the `memo` column of `coded_segments.csv`.

## Working with existing highlights

- **Click a highlight** to open the coding box for that passage. There you can:
  - add more codes to it
  - edit a code's memo (✎)
  - remove a code (✕)
- **Overlapping highlights:** if you click where two highlights overlap, the box opens on the smaller passage. The other passage is listed under *Overlapping passages*, and you can click it to code that one instead.
- **Drag over just part of a highlight** to code only that new selection. The original highlight stays as it is.
- Text with more than one code has a dark underline.

## The right-hand panel

- **Codes in this document:** click a code to show only its highlights (click again, or **show all**, to clear). Hover over a code for:
  - ✎ to rename it in this document
  - ✕ to remove it from this document
- **Coded segments:** lists every coded passage. Click one to jump to it in the text.

## Editing the text

- Click **✎ Edit text** at the top, change anything, then click **Save text** (or press **Ctrl/⌘ + S**). **Cancel** discards your changes.
- Highlights move with the text. Adding text, fixing a typo inside a passage, or moving a paragraph keeps the codes on the right words.
- If you delete all of a highlighted passage, you'll be asked before that highlight is removed.

## What gets saved

Everything saves automatically after every change:

```
QualCode/
├── index.html, server.py, start.bat, start.command, README.md
├── Interview_P01/
│   ├── document.txt          ← your text
│   ├── codes.csv             ← unique codes + frequency
│   ├── coded_segments.csv    ← document, code, highlighted text,
│   │                            start/end character, memo, date coded
│   └── project.json          ← full state, used to resume where you left off
└── Interview_P02/
    └── ...
```

The two **Export** buttons download the same two CSVs for the open document. The CSVs open correctly in Excel (UTF-8).

## Picking up later

Run `start.bat` / `start.command` again. All your documents are listed on the left, and the one you worked on last opens automatically.

## Updating the tool

After you replace `index.html` with a newer version, **hard-refresh** the page (**Ctrl+Shift+R** on Windows, **⌘+Shift+R** on Mac) so the browser loads the new copy.

## Notes

- Edit text inside the tool (**Edit text**), not in `document.txt` directly, because highlights are stored by character position.
- To delete a document, delete its subfolder, then refresh the page.
- Back up by copying the whole `QualCode` folder.
- The server only runs on your own computer (`127.0.0.1`), so nothing goes online.
