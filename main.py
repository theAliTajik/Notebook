import os
import json

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    notes_dir = "notes"
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    notebooks = {}
    # Load existing notebooks
    for file in os.listdir(notes_dir):
        if file.endswith(".json"):
            name = file.replace(".json", "")
            notebooks[name] = Notebook.load_from_file(os.path.join(notes_dir, name))

    while True:
        clear_screen()
        if not notebooks:
            print("No notebooks found. Please create a new notebook.")
            name = input("Enter notebook name: ")
            notebooks[name] = Notebook(name)
            continue

        print("Select a notebook (enter 0 to create a new one):")
        for i, name in enumerate(notebooks, start=1):
            print(f"{i}) {name}")

        choice = input("Enter choice: ")
        if choice == '0':
            name = input("Enter notebook name: ")
            notebooks[name] = Notebook(name)
            notebooks[name].save_to_file()
            continue
        elif choice.isdigit() and 1 <= int(choice) <= len(notebooks):
            notebook = notebooks[list(notebooks)[int(choice) - 1]]
            while True:
                clear_screen()
                print(f"Notebook: {notebook.name}\n")
                print("Select a note (enter 0 to go back):")
                for i, title in enumerate(notebook.list_notes(), start=1):
                    print(f"{i}) {title}")
                print("N) Create new note")

                note_choice = input("Enter choice: ")
                if note_choice == '0':
                    notebook.save_to_file()
                    break
                elif note_choice.upper() == 'N':
                    title = input("Enter note title: ")
                    body = input("Enter note body:\n")
                    notebook.create_note(title, body)
                elif note_choice.isdigit() and 1 <= int(note_choice) <= len(notebook.notes):
                    note_title = notebook.list_notes()[int(note_choice) - 1]
                    note_body = notebook.find_note(note_title)
                    while True:
                        clear_screen()
                        print(f"Title: {note_title}\nBody:\n{note_body}\n")
                        print("1) Edit\n2) Rename\n3) Delete\n0) Back")
                        edit_choice = input("Enter choice: ")
                        if edit_choice == '0':
                            break
                        elif edit_choice == '1':
                            new_body = input("Enter new body:\n")
                            notebook.edit_note(note_title, new_body)
                            note_body = new_body
                        elif edit_choice == '2':
                            new_title = input("Enter new title: ")
                            notebook.rename_note(note_title, new_title)
                            note_title = new_title
                        elif edit_choice == '3':
                            notebook.delete_note(note_title)
                            break

if __name__ == "__main__":
    main()
