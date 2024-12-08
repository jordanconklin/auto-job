class PageParser:
    def __init__(self, page):
        self.page = page

    def find_form_fields(self):
        fields = {
            'text_inputs': self.page.query_selector_all('input[type="text"]'),
            'email_inputs': self.page.query_selector_all('input[type="email"]'),
            'textareas': self.page.query_selector_all('textarea'),
            'selects': self.page.query_selector_all('select')
        }
        return fields

    def detect_free_response_questions(self):
        textareas = self.page.query_selector_all('textarea')
        questions = []
        
        for textarea in textareas:
            label = textarea.evaluate("""(element) => {
                const label = element.labels[0];
                return label ? label.textContent : null;
            }""")
            if label:
                questions.append({
                    'element': textarea,
                    'question': label.strip()
                })
        
        return questions