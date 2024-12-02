import json
import csv
from datetime import datetime

class Task:
    FILE_PATH = "tasks.json"

    def __init__(self, id, title, description="", done=False, priority="Средний", due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date or ""

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }

    @classmethod
    def load_tasks(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                return [cls(**task) for task in json.load(file)]
        except FileNotFoundError:
            return []

    @classmethod
    def save_tasks(cls, tasks):
        with open(cls.FILE_PATH, "w") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)

    @classmethod
    def create_task(cls, title, description="", priority="Средний", due_date=None):
        tasks = cls.load_tasks()
        task_id = len(tasks)+1
        new_task = cls(task_id, title, description, False, priority, due_date)
        tasks.append(new_task)
        cls.save_tasks(tasks)

    @classmethod
    def list_tasks(cls):
        tasks = cls.load_tasks()
        for task in tasks:
            status = "✔" if task.done else "✖"
            print(f"ID: {task.id}, Title: {task.title}, Priority: {task.priority}, Due Date: {task.due_date}, Done: {status}")

    @classmethod
    def mark_task_done(cls, task_id):
        tasks = cls.load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                cls.save_tasks(tasks)
                return
        print("Task not found!")

    @classmethod
    def delete_task(cls, task_id):
        tasks = cls.load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        cls.save_tasks(tasks)

    @classmethod
    def export_tasks_to_csv(cls):
        tasks = cls.load_tasks()
        with open("tasks.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Title", "Description", "Done", "Priority", "Due Date"])
            for task in tasks:
                writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])

    @classmethod
    def import_tasks_from_csv(cls):
        with open("tasks.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = [
                cls(
                    int(row["ID"]),
                    row["Title"],
                    row["Description"],
                    row["Done"].lower() == "true",
                    row["Priority"],
                    row["Due Date"]
                )
                for row in reader
            ]
        cls.save_tasks(tasks)

class FinanceRecord:
    FILE_PATH = "finance.json"

    def __init__(self, record_id, amount, category, date, description=""):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @classmethod
    def load_records(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                return [cls(**record) for record in json.load(file)]
        except FileNotFoundError:
            return []

    @classmethod
    def save_records(cls, records):
        with open(cls.FILE_PATH, "w") as file:
            json.dump([record.to_dict() for record in records], file, ensure_ascii=False, indent=4)

    @classmethod
    def create_record(cls, amount, category, date, description=""):
        records = cls.load_records()
        record_id = len(records) + 1
        new_record = cls(record_id, amount, category, date, description)
        records.append(new_record)
        cls.save_records(records)

    @classmethod
    def list_records(cls):
        records = cls.load_records()
        for record in records:
            print(f"ID: {record.id}, Amount: {record.amount}, Category: {record.category}, Date: {record.date}, Description: {record.description}")

    @classmethod
    def delete_record(cls, record_id):
        records = cls.load_records()
        updated_records = [record for record in records if record.id != record_id]
        cls.save_records(updated_records)
        print(f"Финансовая запись с ID {record_id} успешно удалена.")

    @classmethod
    def export_records_to_csv(cls):
        records = cls.load_records()
        with open("finance.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Amount", "Category", "Date", "Description"])
            for record in records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])

    @classmethod
    def import_records_from_csv(cls):
        with open("finance.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            records = [cls(int(row["ID"]), float(row["Amount"]), row["Category"], row["Date"], row["Description"]) for row in reader]
        cls.save_records(records)

class Contact:
    FILE_PATH = "contacts.json"

    def __init__(self, id, name, phone="", email=""):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone, "email": self.email}

    @classmethod
    def load_contacts(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                return [cls(**contact) for contact in json.load(file)]
        except FileNotFoundError:
            return []

    @classmethod
    def save_contacts(cls, contacts):
        with open(cls.FILE_PATH, "w") as file:
            json.dump([contact.to_dict() for contact in contacts], file, ensure_ascii=False, indent=4)

    @classmethod
    def create_contact(cls, name, phone="", email=""):
        contacts = cls.load_contacts()
        contact_id = len(contacts) + 1
        new_contact = cls(contact_id, name, phone, email)
        contacts.append(new_contact)
        cls.save_contacts(contacts)

    @classmethod
    def list_contacts(cls):
        contacts = cls.load_contacts()
        for contact in contacts:
            print(f"ID: {contact.id}, Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")

    @classmethod
    def search_contact(cls, search_term):
        contacts = cls.load_contacts()
        found_contacts = [c for c in contacts if search_term.lower() in c.name.lower() or search_term in c.phone]
        if not found_contacts:
            print("No contacts found.")
        for contact in found_contacts:
            print(f"ID: {contact.id}, Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}")

    @classmethod
    def delete_contact(cls, contact_id):
        contacts = cls.load_contacts()
        contacts = [c for c in contacts if c.id != contact_id]
        cls.save_contacts(contacts)

    @classmethod
    def export_contacts_to_csv(cls):
        contacts = cls.load_contacts()
        with open("contacts.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Name", "Phone", "Email"])
            for contact in contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])

    @classmethod
    def import_contacts_from_csv(cls):
        with open("contacts.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = [cls(int(row["ID"]), row["Name"], row["Phone"], row["Email"]) for row in reader]
        cls.save_contacts(contacts)


class Note:
    FILE_PATH = "notes.json"

    def __init__(self, id, title, content, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp or self.current_time()

    @staticmethod
    def current_time():
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content, "timestamp": self.timestamp}

    @classmethod
    def load_notes(cls):
        try:
            with open(cls.FILE_PATH, "r") as file:
                return [cls(**note) for note in json.load(file)]
        except FileNotFoundError:
            return []

    @classmethod
    def save_notes(cls, notes):
        with open(cls.FILE_PATH, "w") as file:
            json.dump([note.to_dict() for note in notes], file, ensure_ascii=False, indent=4)

    @classmethod
    def create_note(cls, title, content):
        notes = cls.load_notes()
        note_id = len(notes) + 1
        new_note = cls(note_id, title, content)
        notes.append(new_note)
        cls.save_notes(notes)

    @classmethod
    def list_notes(cls):
        notes = cls.load_notes()
        for note in notes:
            print(f"ID: {note.id}, Title: {note.title}, Timestamp: {note.timestamp}")

    @classmethod
    def view_note_details(cls, note_id):
        notes = cls.load_notes()
        for note in notes:
            if note.id == note_id:
                print(f"Title: {note.title}\nContent: {note.content}\nTimestamp: {note.timestamp}")
                return
        print("Note not found!")

    @classmethod
    def edit_note(cls, note_id, new_title=None, new_content=None):
        notes = cls.load_notes()
        for note in notes:
            if note.id == note_id:
                note.title = new_title or note.title
                note.content = new_content or note.content
                note.timestamp = cls.current_time()
                cls.save_notes(notes)
                return
        print("Note not found!")

    @classmethod
    def delete_note(cls, note_id):
        notes = cls.load_notes()
        notes = [note for note in notes if note.id != note_id]
        cls.save_notes(notes)

    @classmethod
    def export_notes_to_csv(cls):
        notes = cls.load_notes()
        with open("notes.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Title", "Content", "Timestamp"])
            for note in notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])

    @classmethod
    def import_notes_from_csv(cls):
        with open("notes.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            notes = [cls(int(row["ID"]), row["Title"], row["Content"], row["Timestamp"]) for row in reader]
        cls.save_notes(notes)


def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            manage_notes()
        elif choice == "2":
            manage_tasks()
        elif choice == "3":
            manage_contacts()
        elif choice == "4":
            manage_finances()
        elif choice == "5":
            calculator()
        elif choice == "6":
            print("Выход из приложения. До свидания!")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")


def manage_notes():
    print("\nУправление заметками:")
    print("1. Добавить новую заметку")
    print("2. Просмотреть список заметок")
    print("3. Просмотреть подробности заметки")
    print("4. Редактировать заметку")
    print("5. Удалить заметку")
    print("6. Экспорт заметок в CSV")
    print("7. Импорт заметок из CSV")
    print("8. Назад")

    choice = input("Выберите действие: ")

    if choice == "1":
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        Note.create_note(title, content)
        print("Заметка успешно добавлена!")
    elif choice == "2":
        Note.list_notes()
    elif choice == "3":
        note_id = int(input("Введите ID заметки: "))
        note = next((n for n in Note.load_notes() if n.id == note_id), None)
        if note:
            print(f"Заметка ID{note.id}: {note.title}\nСодержание: {note.content}")
        else:
            print("Заметка не найдена.")
    elif choice == "4":
        note_id = int(input("Введите ID заметки: "))
        new_title = input("Введите новый заголовок: ")
        new_content = input("Введите новое содержимое: ")
        Note.edit_note(note_id, new_title, new_content)
        print("Заметка успешно обновлена!")
    elif choice == "5":
        note_id = int(input("Введите ID заметки для удаления: "))
        Note.delete_note(note_id)
        print("Заметка удалена.")
    elif choice == "6":
        Note.export_notes_to_csv()
        print("Заметки экспортированы в CSV.")
    elif choice == "7":
        Note.import_notes_from_csv()
        print("Заметки импортированы из CSV.")
    elif choice == "8":
        return


def manage_tasks():
    print("\nУправление задачами:")
    print("1. Добавить новую задачу")
    print("2. Просмотреть задачи")
    print("3. Отметить задачу как выполненную")
    print("4. Редактировать задачу")
    print("5. Удалить задачу")
    print("6. Экспорт задач в CSV")
    print("7. Импорт задач из CSV")
    print("8. Назад")

    choice = input("Выберите действие: ")

    if choice == "1":
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
        Task.create_task(title, description, priority, due_date)
        print("Задача успешно добавлена!")
    elif choice == "2":
        Task.list_tasks()
    elif choice == "3":
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))
        Task.mark_task_done(task_id)
        print("Задача отмечена как выполненная.")
    elif choice == "4":
        task_id = int(input("Введите ID задачи для редактирования: "))
        new_title = input("Введите новое название: ")
        new_description = input("Введите новое описание: ")
        Task.create_task(task_id, new_title, new_description)
        print("Задача успешно обновлена!")
    elif choice == "5":
        task_id = int(input("Введите ID задачи для удаления: "))
        Task.delete_task(task_id)
        print("Задача удалена.")
    elif choice == "6":
        Task.export_tasks_to_csv()
        print("Задачи экспортированы в CSV.")
    elif choice == "7":
        Task.import_tasks_from_csv()
        print("Задачи импортированы из CSV.")
    elif choice == "8":
        return


def manage_contacts():
    print("\nУправление контактами:")
    print("1. Добавить новый контакт")
    print("2. Поиск контакта")
    print("3. Редактировать контакт")
    print("4. Удалить контакт")
    print("5. Экспорт контактов в CSV")
    print("6. Импорт контактов из CSV")
    print("7. Назад")

    choice = input("Выберите действие: ")

    if choice == "1":
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите email: ")
        Contact.create_contact(name, phone, email)
        print("Контакт успешно добавлен!")
    elif choice == "2":
        search_term = input("Введите имя или номер телефона для поиска: ")
        Contact.search_contact(search_term)
    elif choice == "3":
        contact_id = int(input("Введите ID контакта для редактирования: "))
        new_name = input("Введите новое имя: ")
        new_phone = input("Введите новый номер телефона: ")
        Contact.create_contact(contact_id, new_name, new_phone)
        print("Контакт успешно обновлен!")
    elif choice == "4":
        contact_id = int(input("Введите ID контакта для удаления: "))
        Contact.delete_contact(contact_id)
        print("Контакт удален.")
    elif choice == "5":
        Contact.export_contacts_to_csv()
        print("Контакты экспортированы в CSV.")
    elif choice == "6":
        Contact.import_contacts_from_csv()
        print("Контакты импортированы из CSV.")
    elif choice == "7":
        return


def manage_finances():
    print("\nУправление финансовыми записями:")
    print("1. Добавить новую запись")
    print("2. Просмотреть все записи")
    print("3. Генерация отчёта")
    print("4. Удалить запись")
    print("5. Экспорт финансовых записей в CSV")
    print("6. Импорт финансовых записей из CSV")
    print("7. Назад")

    choice = input("Выберите действие: ")

    if choice == "1":
        amount = float(input("Введите сумму операции: "))
        category = input("Введите категорию: ")
        date = input("Введите дату (ДД-ММ-ГГГГ): ")
        description = input("Введите описание: ")
        FinanceRecord.create_record(amount, category, date, description)
        print("Финансовая запись добавлена!")
    elif choice == "2":
        FinanceRecord.list_records()
    elif choice == "3":
        start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
        end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
        FinanceRecord.create_record(start_date, end_date)
    elif choice == "4":
        record_id = int(input("Введите ID записи для удаления: "))
        FinanceRecord.delete_record(record_id)
        print("Запись удалена.")
    elif choice == "5":
        FinanceRecord.export_records_to_csv()
        print("Финансовые записи экспортированы в CSV.")
    elif choice == "6":
        FinanceRecord.import_records_from_csv()
        print("Финансовые записи импортированы из CSV.")
    elif choice == "7":
        return

def calculator():
    print("\nКалькулятор:")
    expression = input("Введите выражение для вычисления: ")
    try:
        result = eval(expression)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка в вычислении: {e}")


if __name__ == "__main__":
    main_menu()