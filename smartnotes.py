from abc import update_abstractmethods
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog
 
import json
 
app = QApplication([])
 




MyNote = {
    "Example" :
    {
        "text" : "Very important note text",
        "tags" : ["draft","thoughts"]
    }
}



#application window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)
 
#application window widgets
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')
 


button_note_create = QPushButton('Create note') #a window appears with the field "Enter note name"
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')
 
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()
button_add = QPushButton('Add tag')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')
 
#arranging widgets by layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
 
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
 
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_search)
 
col_2.addLayout(row_3)
col_2.addLayout(row_4)
 
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def update():
    global MyNote
    list_notes.clear()
    with open("notes_data.json", "r") as file:
        MyNote =json.load(file)
    for note in MyNote:
        list_notes.addItem(note)
   
    

def add_tag():
    global MyNote
    note_name, ok = QInputDialog.getText(
    notes_win, "Add note", "Note name: ")
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in MyNote[key]["tags"]:
            MyNote[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(MyNote, file, sort_keys=True)
    else:
        print("No note selected to add tag!")



def save():
    global MyNote
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        MyNote[key]["text"] = field_text.toPlainText()
    with open("notes_data.json", "w") as file:
        json.dump(MyNote, file)


def g():
    global MyNote
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del MyNote[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(MyNote)

    with open("notes_data.json", "r") as file:
        MyNote =json.load(file)
g()
def show_note():
    #receiving text from the note with highlighted title and displaying it in the edit field
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(MyNote[key]["text"])
    list_tags.clear()
    list_tags.addItems(MyNote[key]["tags"])



def del_note():
    global MyNote
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del MyNote[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(MyNote)
        with open("notes_data.json", "w") as file:
            json.dump(MyNote, file, sort_keys=True)
        update()



def add_note():
    global MyNote
    note_name, ok = QInputDialog.getText(
    notes_win, "Add note", "Note name: ")
    if ok and note_name != "cancel":
        MyNote[note_name] = {"text" : "", "tags" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(MyNote[note_name]["tags"])
        with open("notes_data.json", "w") as file:
            json.dump(MyNote, file, sort_keys=True)
    update()

def search_tag():
    global MyNote
    tag = field_tag.text()
    if button_search.text() == "Search for notes by tag" and tag:
        notes_filtered = {} 
        for note in MyNote:
            if tag in MyNote[note]["tags"]:
                notes_filtered[note]=MyNote[note]
        button_search.setText("Clear search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_search.text() == "Clear search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(MyNote)
        button_search.setText("Search for notes by tag")
    else:
        pass

def add_tag():
    global MyNote
   
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        
        
        MyNote[key]["tags"].append(tag)
      
        list_tags.clear()
        for i in MyNote[key]['tags']:
            list_tags.addItem(i)
        with open("notes_data.json", "w") as file:
            json.dump(MyNote, file, sort_keys=True)
    else:
        print("No note selected to add tag!")
    update()  

def del_tag():
    global MyNote
    if list_notes.selectedItems():
        if list_tags.selectedItems():
            tag = list_tags.selectedItems()[0].text()
            key = list_notes.selectedItems()[0].text()
            MyNote[key]['tags'].remove(tag)
            list_tags.clear()
            list_notes.addItems(MyNote)
            with open("notes_data.json", "w") as file:
                json.dump(MyNote, file, sort_keys=True)
            update()


list_notes.itemClicked.connect(show_note)
button_add.clicked.connect(add_tag)
button_note_save.clicked.connect(save)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_search.clicked.connect(search_tag)
button_del.clicked.connect(del_tag)
update()

#run the application
notes_win.show()
app.exec_()