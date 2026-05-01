import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ---------------- BACKEND ----------------
class Library:
    database = "library.json"

    def __init__(self):
        self.data = {"books": [], "members": []}
        self.load_data()

    def load_data(self):
        if Path(self.database).exists():
            with open(self.database, "r") as f:
                try:
                    self.data = json.load(f)
                except:
                    self.data = {"books": [], "members": []}
        else:
            self.save_data()

    def save_data(self):
        with open(self.database, "w") as f:
            json.dump(self.data, f, indent=4)

    @staticmethod
    def generate_id(prefix="B"):
        return prefix + "_" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )

# ---------------- UI ----------------
lib = Library()

st.set_page_config(page_title="Library System", layout="centered")

st.title("📚 Library Management System")

menu = st.sidebar.selectbox(
    "Choose Action",
    ["Add Book", "View Books", "Add Member", "View Members", "Borrow Book", "Return Book"]
)

# ---------------- ADD BOOK ----------------
if menu == "Add Book":
    st.subheader("➕ Add Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    copies = st.number_input("Copies", min_value=1, step=1)

    if st.button("Add Book"):
        book = {
            "id": lib.generate_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        lib.data["books"].append(book)
        lib.save_data()
        st.success("✅ Book added successfully!")

# ---------------- VIEW BOOKS ----------------
elif menu == "View Books":
    st.subheader("📖 Book List")

    if lib.data["books"]:
        st.table(lib.data["books"])
    else:
        st.warning("No books found")

# ---------------- ADD MEMBER ----------------
elif menu == "Add Member":
    st.subheader("👤 Add Member")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add Member"):
        member = {
            "id": lib.generate_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }
        lib.data["members"].append(member)
        lib.save_data()
        st.success("✅ Member added!")

# ---------------- VIEW MEMBERS ----------------
elif menu == "View Members":
    st.subheader("👥 Members List")

    if lib.data["members"]:
        st.table(lib.data["members"])
    else:
        st.warning("No members found")

# ---------------- BORROW BOOK ----------------
elif menu == "Borrow Book":
    st.subheader("📚 Borrow Book")

    member_ids = [m["id"] for m in lib.data["members"]]
    book_ids = [b["id"] for b in lib.data["books"]]

    member_id = st.selectbox("Select Member", member_ids)
    book_id = st.selectbox("Select Book", book_ids)

    if st.button("Borrow"):
        member = next((m for m in lib.data["members"] if m["id"] == member_id), None)
        book = next((b for b in lib.data["books"] if b["id"] == book_id), None)

        if book["available_copies"] > 0:
            member["borrowed"].append({
                "book_id": book["id"],
                "title": book["title"],
                "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            book["available_copies"] -= 1
            lib.save_data()
            st.success("✅ Book borrowed!")
        else:
            st.error("❌ No copies available")

# ---------------- RETURN BOOK ----------------
elif menu == "Return Book":
    st.subheader("🔄 Return Book")

    member_ids = [m["id"] for m in lib.data["members"]]
    member_id = st.selectbox("Select Member", member_ids)

    member = next((m for m in lib.data["members"] if m["id"] == member_id), None)

    if member and member["borrowed"]:
        borrowed_titles = [b["title"] for b in member["borrowed"]]
        selected = st.selectbox("Select Book to Return", borrowed_titles)

        if st.button("Return Book"):
            for b in member["borrowed"]:
                if b["title"] == selected:
                    member["borrowed"].remove(b)

                    book = next((bk for bk in lib.data["books"] if bk["id"] == b["book_id"]), None)
                    if book:
                        book["available_copies"] += 1

                    lib.save_data()
                    st.success("✅ Book returned!")
                    break
    else:
        st.warning("No borrowed books")