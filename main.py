import json
import random
import string
from pathlib import Path
from datetime import datetime


class Library:
    database="library.json"
    data={"books":[], "members":[]}

    #load existing data to json

    if Path(database).exists():
        with open(database,"r") as f:
            content=f.read().strip()
            if content:
                data = json.loads(content)
    else:
        with open(database,"w") as f:
            json.dump(data,f,indent=4)



    def generate_id(prefix="B"):
        randomm_id = ""
        for i in range (5):
            randomm_id+= random.choice(string.ascii_uppercase + string.digits )
        
        return prefix + "_" + randomm_id

    @classmethod
    def save_data(cls):
        with open(cls.database,'w') as f:
            json.dump(cls.data,f,indent=4,default=str
                       )




    def add_book(self):
        title=input("Enter book title : ")
        aurthor=input("Enter the book aurthor : ")
        copies=int(input("How many copies : "))

        book={
            "id": Library.generate_id(),
            "title" : title,
            "aurthor" : aurthor,
            "total_copies" : copies,
            "avilable_copies" :  copies,   
            "added_on" :  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        Library.data['books'].append(book)
        Library.save_data()

    

    def list_books(self):
        if not Library.data['books']:
            print("Sorry no books found")
            return
        for b in Library.data['books']:
            print(f"{b['id']:12} {b['title'][:24]:25} {b['aurthor'][:19]:20} {b['total_copies']}/{b['avilable_copies']:>3}")
    print()



    def add_members(self):
        name=input("Enter the name : ")
        email=input("Enter the email : ")

        member={
            "id" :  Library.generate_id("M"),
            "name" : name,
            "email" : email,
            "borrowed" : []
        }
        Library.data['members'].append(member)
        Library.save_data()
        print("Member added successfully")
    

    def list_members(self):
        if not Library.data['members']:
            print("Sorry no member found")
            return
        for b in Library.data['members']:
            print(f"{b['id']:12} {b['name'][:24]:25} {b['email']:30}")
            print("this guy has currently : ")
            print(f"{b['borrowed']}")
    print()


    def borrow_book(self):
        member_id=input("Enter the member ID :").strip()
        members = [m for m in Library.data['members'] if m['id']==member_id ]
        if not members:
            print("No such ID exist")
            return
        member=members[0]

        book_id=input("enter the book id")
        books = [m for m in Library.data['books'] if m['id']==book_id ]
        if not books:
            print("No such ID exist")
            return
        book=books[0]

        if book['avilable_copies']<=0:
            print("Sorry no books exist")
            return
        
        borrow_entry={
            "book_id" : book['id'],
            "title" : book['title'],
            "borrow_on" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        member['borrowed'].append(borrow_entry)
        book['avilable_copies']-=1
        Library.save_data()



    def return_book(self):
        member_id=input("Enter the member ID :").strip()
        members = [m for m in Library.data['members'] if m['id']==member_id ]
        if not members:
            print("No such ID exist")
            return
        member=members[0]

        if not  member['borrowed']:
            print("No borrowed book")
            return
        
        print("Borrowed books : ")
        for i,b in enumerate(member['borrowed'],start=1):
            print(f"{i}.  {b['title']:25} {b['book_id']:25}")

        try:
            choice=int(input("Enter serial no. to return :-"))
            selected=member['borrowed'].pop(choice-1)
        except Exception as ex:
            print(f"Some error occured! {ex} please try again")

        books=[bk for bk in Library.data['books'] if bk['id']== selected['book_id']]
        if books:
            books[0]['avilable_copies'] +=1

        Library.save_data()



hello=Library()
while True:
    print("="*50)
    print("Library Management System")
    print("="*50)
    print("1. Add Book")
    print("2. List Book")
    print("3. Add Member")
    print("4. List Member")
    print("5. Borrow Book")
    print("6. Return Book")
    print("0. Exit the Portal")
    print("_"*50)
    choice = input("what task you want to do. ")

    if choice=="1":
        hello.add_book()

    if choice=="2":
        hello.list_books()

    if choice=="3":
        hello.add_members()

    if choice=="4":
        hello.list_members()

    if choice=="5":
        hello.borrow_book()

    if choice=="6":
        hello.return_book()

    if choice=="0":
        exit(0)