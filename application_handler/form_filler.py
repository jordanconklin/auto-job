class FormFiller:
    def __init__(self, user_profile, response_templates):
        self.profile = user_profile
        self.templates = response_templates

    def fill_common_fields(self, page):
        print("\nAttempting to fill personal information...")
        
        fields_to_fill = {
            'firstName': self.profile.get_field('personal', 'first_name'),
            'lastName': self.profile.get_field('personal', 'last_name'),
            'email': self.profile.get_field('personal', 'email'),
            'phoneNumber': self.profile.get_field('personal', 'phone'),
            'addressLine1': self.profile.get_field('personal', 'address.street'),
            'addressLine2': '',  # Leave blank or add if needed
            'city': self.profile.get_field('personal', 'address.city'),
            'state': self.profile.get_field('personal', 'address.state'),
            'zipCode': self.profile.get_field('personal', 'address.zip')
        }
        
        # Fill regular input fields
        for field_name, value in fields_to_fill.items():
            print(f"\nLooking for {field_name} field...")
            success = self._fill_by_attribute(page, field_name, value)
            if success:
                print(f"✅ Filled {field_name} successfully")
            else:
                print(f"⚠️ Could not find or fill {field_name} field")

        # Handle country dropdown separately
        print("\nLooking for country dropdown...")
        self._handle_country_dropdown(page)

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

    def _get_selectors(self, field_name):
        # Define field-specific selectors
        if field_name == 'first':
            return [
                'input[name*="first" i]',
                'input[id*="first" i]',
                'input[placeholder*="first" i]',
                'input[name*="firstname" i]',
                'input[id*="firstname" i]'
            ]
        elif field_name == 'last':
            return [
                'input[name*="last" i]',
                'input[id*="last" i]',
                'input[placeholder*="last" i]',
                'input[name*="lastname" i]',
                'input[id*="lastname" i]'
            ]
        elif field_name == 'address1':
            return [
                'input[name*="address1" i]',
                'input[id*="address1" i]',
                'input[name*="addressline1" i]',    
                'input[id*="addressline1" i]',
                'input[name*="street" i]',
                'input[id*="street" i]',
                'input[placeholder*="address line 1" i]',
                'input[aria-label*="address line 1" i]',
                'input[name*="line1" i]',
                'input[id*="line1" i]'
            ]
        else:
            return [
                f'input[name*="{field_name}" i]',
                f'input[id*="{field_name}" i]',
                f'input[placeholder*="{field_name}" i]'
            ]

    def _handle_country_dropdown(self, page):
        try:
            # Common selectors for country dropdowns
            selectors = [
                'select[name*="country" i]',
                'select[id*="country" i]',
                'select[aria-label*="country" i]'
            ]
            
            for selector in selectors:
                dropdown = page.query_selector(selector)
                if dropdown:
                    # Try to select "United States" or similar
                    try:
                        dropdown.select_option(value="United States")
                        print("✅ Selected 'United States' in country dropdown")
                        return True
                    except:
                        try:
                            dropdown.select_option(label="United States")
                            print("✅ Selected 'United States' in country dropdown")
                            return True
                        except Exception as e:
                            print(f"Failed to select country: {e}")
            
            print("⚠️ Could not find or interact with country dropdown")
            return False
        except Exception as e:
            print(f"Error handling country dropdown: {e}")
            return False