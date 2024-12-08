class FormFiller:
    def __init__(self, user_profile, response_templates):
        self.profile = user_profile
        self.templates = response_templates

    def fill_common_fields(self, page):
        print("\nAttempting to fill personal information...")
        
        # Fill personal information
        fields_to_fill = {
            'name': self.profile.get_field('personal', 'first_name') + ' ' + 
                    self.profile.get_field('personal', 'last_name'),
            'email': self.profile.get_field('personal', 'email'),
            'phone': self.profile.get_field('personal', 'phone')
        }
        
        for field_name, value in fields_to_fill.items():
            print(f"\nLooking for {field_name} field...")
            print(f"Current URL: {page.url}")
            print(f"Trying to fill value: {value}")
            success = self._fill_by_attribute(page, field_name, value)
            if success:
                print(f"✅ Filled {field_name} successfully")
            else:
                print(f"⚠️ Could not find or fill {field_name} field")
                print("Attempted selectors:")
                for selector in [
                    f'input[name*="{field_name}" i]',
                    f'input[id*="{field_name}" i]',
                    f'input[placeholder*="{field_name}" i]'
                ]:
                    elements = page.query_selector_all(selector)
                    print(f"  - {selector}: found {len(elements)} elements")

    def fill_free_response(self, element, response):
        try:
            element.fill(response)
            return True
        except Exception as e:
            print(f"Error filling free response: {e}")
            return False

    def _fill_by_attribute(self, page, attr_name, value):
        filled = False
        selectors = [
            f'input[name*="{attr_name}" i]',
            f'input[id*="{attr_name}" i]',
            f'input[placeholder*="{attr_name}" i]'
        ]
        
        for selector in selectors:
            elements = page.query_selector_all(selector)
            if elements:
                for element in elements:
                    try:
                        element.fill(value)
                        filled = True
                        print(f"Successfully filled element with selector: {selector}")
                    except Exception as e:
                        print(f"Failed to fill element with selector {selector}: {str(e)}")
                        continue
        
        if not filled:
            print(f"Could not find any fillable elements for {attr_name}")
            # Try to print all input elements for debugging
            all_inputs = page.query_selector_all('input')
            print(f"\nFound {len(all_inputs)} total input elements on page")
            print("Available input elements:")
            for input_el in all_inputs:
                try:
                    attrs = page.evaluate("""(element) => {
                        const attributes = {};
                        for (const attr of element.attributes) {
                            attributes[attr.name] = attr.value;
                        }
                        return attributes;
                    }""", input_el)
                    print(f"  Input attributes: {attrs}")
                except Exception as e:
                    print(f"Error getting attributes: {e}")
        
        return filled