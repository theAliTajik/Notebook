import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QListWidget, QTextEdit, QInputDialog



class Notebook:
    def __init__(self, name):
        self.name = name
        self.notes = {}

    def create_note(self, title, body):
        self.notes[title] = body
        self.save_to_file()

    def delete_note(self, title):
        del self.notes[title]
        self.save_to_file()

    def rename_note(self, old_title, new_title):
        self.notes[new_title] = self.notes.pop(old_title)
        self.save_to_file()

    def edit_note(self, title, new_body):
        self.notes[title] = new_body
        self.save_to_file()

    def list_notes(self):
        return list(self.notes.keys())

    def find_note(self, title):
        return self.notes.get(title, None)

    def save_to_file(self):
        notes_dir = "notes"
        with open(os.path.join(notes_dir, f"{self.name}.json"), 'w') as file:
            json.dump(self.notes, file, indent=4)

    @staticmethod
    def load_from_file(name):
            notes_dir = "notes"
            try:
                with open(os.path.join(notes_dir, f"{name}.json"), 'r') as file:
                    notes = json.load(file)
                    notebook = Notebook(name)
                    notebook.notes = notes
                    return notebook
            except FileNotFoundError:
                return Notebook(name)

class NotebookGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.notebooks = {}
        self.current_notebook = None
        self.current_note = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Notebook GUI')

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Layout for notebooks and notebook buttons
        notebook_layout = QVBoxLayout()
        self.notebook_list = QListWidget()
        notebook_layout.addWidget(self.notebook_list)

        # Buttons for notebooks
        self.add_notebook_btn = QPushButton('Add Notebook')
        self.remove_notebook_btn = QPushButton('Remove Notebook')
        self.edit_notebook_btn = QPushButton('Edit Notebook Title')
        notebook_layout.addWidget(self.add_notebook_btn)
        notebook_layout.addWidget(self.remove_notebook_btn)
        notebook_layout.addWidget(self.edit_notebook_btn)
        main_layout.addLayout(notebook_layout)

        self.add_notebook_btn.clicked.connect(self.add_notebook)
        self.notebook_list.itemClicked.connect(self.on_notebook_selected)

        # Layout for notes and note buttons
        note_layout = QVBoxLayout()
        self.note_list = QListWidget()
        note_layout.addWidget(self.note_list)

        # Buttons for notes
        self.add_note_btn = QPushButton('Add Note')
        self.remove_note_btn = QPushButton('Remove Note')
        self.edit_note_btn = QPushButton('Edit Note Title')
        note_layout.addWidget(self.add_note_btn)
        note_layout.addWidget(self.remove_note_btn)
        note_layout.addWidget(self.edit_note_btn)
        main_layout.addLayout(note_layout)

        self.add_note_btn.clicked.connect(self.add_note)

        # Note body text editor
        body_layout = QVBoxLayout()
        self.note_body = QTextEdit()
        body_layout.addWidget(self.note_body)
        self.save_note_btn = QPushButton("save")
        body_layout.addWidget(self.save_note_btn)
        main_layout.addLayout(body_layout)

        self.save_note_btn.clicked.connect(self.save_note)
        self.note_list.itemClicked.connect(self.on_note_selected)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the window size
        self.setGeometry(100, 100, 900, 600)

    def add_notebook(self):
        name, ok = QInputDialog.getText(self, 'Add Notebook', 'Enter notebook name:')
        if ok and name:
            notebook = Notebook(name)
            self.notebook_list.addItem(name)
            # If you have a list or dict to keep track of notebooks
            self.notebooks[name] = notebook
            # Save the notebook list if required
            notebook.save_to_file()

    def on_notebook_selected(self, item):
        notebook_name = item.text()
        notebook = self.notebooks.get(notebook_name)
        if notebook:
            self.note_body.clear()
            self.note_list.clear()  # Clear the list before adding new items
            for title in notebook.list_notes():
                self.note_list.addItem(title)
            self.current_notebook = notebook

    def add_note(self):
        name, ok = QInputDialog.getText(self, 'Add Note', 'Enter note name:')
        if ok and name and self.current_notebook:
            self.note_list.addItem(name)
            self.current_notebook.create_note(name,"")

    def on_note_selected(self, item):
        note = item.text()
        if note:
            self.note_body.clear()
            self.note_body.setText(self.current_notebook.find_note(note))
            self.current_note = note

    def save_note(self):
        print("save button clicked")
        if self.current_notebook and self.current_note:
            self.current_notebook.edit_note(self.current_note, self.note_body.toPlainText())
            print(f"saved current note {self.current_note}")



def main():
    app = QApplication(sys.argv)
    ex = NotebookGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()