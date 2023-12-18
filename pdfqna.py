import sys
import fitz
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog


class PDFSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Search Interface")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.file_label = QLabel("Selected PDF: No file selected")
        self.layout.addWidget(self.file_label)

        self.load_file_button = QPushButton("Load PDF File")
        self.load_file_button.clicked.connect(self.load_pdf_file)
        self.layout.addWidget(self.load_file_button)

        self.search_label = QLabel("Enter your search query:")
        self.layout.addWidget(self.search_label)

        self.search_text_edit = QTextEdit()
        self.layout.addWidget(self.search_text_edit)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_pdf)
        self.layout.addWidget(self.search_button)

        self.result_label = QLabel("Search Results:")
        self.layout.addWidget(self.result_label)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        self.layout.addWidget(self.result_text_edit)

        self.load_next_button = QPushButton("Load Next Question")
        self.load_next_button.clicked.connect(self.load_next_question)
        self.layout.addWidget(self.load_next_button)

        self.current_question_index = 0
        self.questions = []
        self.answers = []

        self.setLayout(self.layout)

    def load_pdf_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")

        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.file_label.setText(f"Selected PDF: {file_path}")
            self.clear_results()

    def search_pdf(self):
        if not hasattr(self, 'pdf_document'):
            self.result_text_edit.setPlainText("Error: No PDF file selected.")
            return

        query = self.search_text_edit.toPlainText().strip()
        if not query:
            self.result_text_edit.setPlainText("Error: Please enter a search query.")
            return

        self.result_text_edit.clear()

        for i, question in enumerate(self.questions):
            if question.lower() in query.lower():
                result = self.get_text_after_search(query)
                self.result_text_edit.append(f"Question {i + 1}: {result}")

    def get_text_after_search(self, query, max_chars=2000):
        result = ""
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            text = page.get_text("text")

            bold_search = f"<b>{query}</b>"
            index_bold = text.lower().find(bold_search.lower())
            if index_bold != -1:
                # Find the following italic text (not bolded)
                index_italic = text.lower().find("<i>", index_bold)
                if index_italic != -1:
                    index_italic_end = text.lower().find("</i>", index_italic)
                    if index_italic_end != -1:
                        result += text[index_italic + 3:index_italic_end]

        return result[:max_chars]  # Return up to max_chars characters

    def load_next_question(self):
        self.questions.append(self.search_text_edit.toPlainText().strip())
        self.answers.append(self.result_text_edit.toPlainText().strip())
        self.clear_results()
        self.current_question_index += 1
        self.search_text_edit.clear()

    def clear_results(self):
        self.result_text_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFSearchApp()
    window.show()
    sys.exit(app.exec_())
