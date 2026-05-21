from playwright.sync_api import Page
class TodoPage():
    #Locators
    INPUT_FIELD = "#todo-input"
    ADD_BUTTON = ".new-todo"
    DELETE_BUTTON = ".destroy"
    TODO_ITEM = ".todo-list li"
    CLEAR_ITEM = ".clear-completed"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def add_todo(self, text: str):
        self.page.fill(self.INPUT_FIELD, text)
        self.page.keyboard.press("Enter")

    def delete_todo(self, text: str):
        item = self.page.locator(self.TODO_ITEM, has_text=text)
        item.hover()  # makes the delete button appear
        item.locator(self.DELETE_BUTTON).click()

    def mark_completed(self, text: str):
        self.page.locator(self.TODO_ITEM, has_text=text).locator(".toggle").click()

    def clear_all_todo(self):
        self.page.click(self.CLEAR_ITEM)

