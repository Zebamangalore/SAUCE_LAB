import re
from playwright.sync_api import Page, expect


class TodoPage:
    # Locator constants
    INPUT_PLACEHOLDER = "What needs to be done?"
    TODO_COUNT        = ".todo-count"
    FOOTER            = ".footer"

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────────────
    def add_todo(self, text: str):
        self.page.get_by_placeholder(self.INPUT_PLACEHOLDER).fill(text)
        self.page.keyboard.press("Enter")

    def complete_todo(self, text: str):
        self.get_item(text).get_by_role("checkbox").check()

    def delete_todo(self, text: str):
        item = self.get_item(text)
        item.hover()
        item.get_by_role("button", name="Delete").click()

    def edit_todo(self, old_text: str, new_text: str):
        item = self.get_item(old_text)
        item.locator("label").dblclick()
        edit_input = item.get_by_role("textbox")
        edit_input.fill(new_text)
        self.page.keyboard.press("Enter")

    def filter_active(self):
        self.page.get_by_role("link", name="Active").click()

    def take_screenshot(self, path: str):
        self.page.screenshot(path=path)

    # ── Getters ───────────────────────────────────────────────────
    def get_item(self, text: str):
        return self.page.get_by_test_id("todo-item").filter(has_text=text)

    def get_all_items(self):
        return self.page.get_by_test_id("todo-item")

    def get_count_text(self):
        return self.page.locator(self.TODO_COUNT)

    # ── Assertions ────────────────────────────────────────────────
    def expect_item_visible(self, text: str):
        expect(self.get_item(text)).to_be_visible()

    def expect_item_text(self, text: str):
        expect(self.get_item(text)).to_have_text(text)

    def expect_item_completed(self, text: str):
        expect(self.get_item(text)).to_have_class(re.compile(r"\bcompleted\b"))

    def expect_item_count(self, count: int):
        expect(self.get_all_items()).to_have_count(count)

    def expect_count_text(self, text: str):
        expect(self.get_count_text()).to_have_text(text)

    def expect_footer_hidden(self):
        expect(self.page.locator(self.FOOTER)).to_be_hidden()

    def expect_checkbox_checked(self, text: str):
        expect(self.get_item(text).get_by_role("checkbox")).to_be_checked()

    def expect_checkbox_not_checked(self, text: str):
        expect(self.get_item(text).get_by_role("checkbox")).not_to_be_checked()