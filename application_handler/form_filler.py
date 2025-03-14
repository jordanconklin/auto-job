class FormFiller:
    def __init__(self, user_profile, response_templates):
        self.profile = user_profile
        self.templates = response_templates

    def fill_common_fields(self, page):
        print("\nAttempting to fill personal information...")
        
        # Greenhouse.io specific field mapping
        greenhouse_fields = {
            'first_name': self.profile.get_field('personal', 'first_name'),
            'last_name': self.profile.get_field('personal', 'last_name'),
            'email': self.profile.get_field('personal', 'email'),
            'phone': self.profile.get_field('personal', 'phone'),
            'question_7392021005': self.profile.get_field('personal', 'linkedin'),  # LinkedIn field
            'question_7392022005': self.profile.get_field('personal', 'website')   # Website field
        }
        
        # Handle website field first with debug info
        website_value = self.profile.get_field('personal', 'website')
        print(f"\nAttempting to fill website field with value: {website_value}")
        
        # Try multiple approaches for website field
        website_selectors = [
            'input#question_7392022005',
            'input[aria-label="Website"]',
            '[id="question_7392022005"]',
            'input[name*="website" i]',
            'input[placeholder*="website" i]'
        ]
        
        website_filled = False
        for selector in website_selectors:
            try:
                print(f"Trying selector: {selector}")
                element = page.query_selector(selector)
                if element:
                    print(f"Found element with selector: {selector}")
                    # Try different fill methods
                    try:
                        element.fill(website_value)
                        website_filled = True
                        print(f"✅ Filled website using fill() method with selector: {selector}")
                        break
                    except Exception as e1:
                        print(f"fill() failed, trying type: {e1}")
                        try:
                            element.type(website_value)
                            website_filled = True
                            print(f"✅ Filled website using type() method with selector: {selector}")
                            break
                        except Exception as e2:
                            print(f"type() failed: {e2}")
            except Exception as e:
                print(f"Failed with selector {selector}: {e}")
        
        if not website_filled:
            print("⚠️ Could not fill website field with any method")
            # Print all input elements for debugging
            inputs = page.query_selector_all('input')
            print("\nAvailable input elements:")
            for input_el in inputs:
                attrs = input_el.evaluate('(element) => { return {...element.attributes} }')
                print(f"Input attributes: {attrs}")
        
        # Continue with other fields...
        for field_id, value in greenhouse_fields.items():
            if field_id != 'question_7392022005':  # Skip website as we handled it separately
                try:
                    # Try to find element by ID first
                    element = page.query_selector(f'#{field_id}')
                    if element:
                        element.fill(value)
                        print(f"✅ Filled {field_id} successfully")
                        continue
                    
                    # If ID fails, try by aria-label
                    aria_labels = {
                        'first_name': 'First Name',
                        'last_name': 'Last Name',
                        'email': 'Email',
                        'phone': 'Phone',
                        'question_7392021005': 'LinkedIn Profile'
                    }
                    
                    if field_id in aria_labels:
                        element = page.query_selector(f'input[aria-label="{aria_labels[field_id]}"]')
                        if element:
                            element.fill(value)
                            print(f"✅ Filled {field_id} successfully")
                            continue
                    
                    print(f"⚠️ Could not find field {field_id}")
                    
                except Exception as e:
                    print(f"Error filling {field_id}: {e}")

        # Fall back to generic field filling if needed
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

    def _get_greenhouse_selectors(self, field_type):
        selectors = {
            'first_name': ['#first_name', 'input[aria-label="First Name"]'],
            'last_name': ['#last_name', 'input[aria-label="Last Name"]'],
            'email': ['#email', 'input[aria-label="Email"]'],
            'phone': ['#phone', 'input[aria-label="Phone"]'],
            'linkedin': ['#question_7392021005', 'input[aria-label="LinkedIn Profile"]'],
            'website': ['#question_7392022005', 'input[aria-label="Website"]']
        }
        return selectors.get(field_type, [])

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

    def _handle_location_dropdowns(self, page, location):
        # Parse location (assuming format like "Los Angeles, CA")
        parts = location.split(',')
        state = parts[1].strip() if len(parts) > 1 else ''
        
        # Try standard location dropdowns first
        standard_selectors = [
            'select[name*="location" i]',
            'select[id*="location" i]',
            'select[aria-label*="location" i]',
            'select[name*="state" i]',
            'select[id*="state" i]'
        ]
        
        # Try template field selectors (matching the application's format)
        template_selectors = [
            'select.form-control.clonedInputElm',
            'select[class*="form-control clonedInputElm"]',
            'select[name*="templateField"]',
            'select[id*="templateField"]'
        ]
        
        # Try standard selectors first
        for selector in standard_selectors:
            dropdown = page.query_selector(selector)
            if dropdown and self._try_select_location(dropdown, state):
                return True
            
        # If standard selectors fail, try template selectors
        for selector in template_selectors:
            dropdown = page.query_selector(selector)
            if dropdown and self._try_select_location(dropdown, state):
                return True
        
        print("⚠️ Could not find or interact with location dropdown")
        return False

    def _try_select_location(self, dropdown, state):
        try:
            # Get available options
            options = dropdown.evaluate("""(element) => {
                return Array.from(element.options).map(opt => ({
                    value: opt.value,
                    text: opt.text
                }));
            }""")
            
            # Try to find best match for location
            location_terms = [
                state, "CA", "California",
                "United States", "USA"
            ]
            
            for term in location_terms:
                for option in options:
                    if term.lower() in option['text'].lower():
                        dropdown.select_option(value=option['value'])
                        print(f"✅ Selected location: {option['text']}")
                        return True
                    
        except Exception as e:
            print(f"Failed to select location: {e}")
        
        return False

    def fill_work_experience(self, page, resume_parser):
        print("\nAttempting to fill work experience...")
        
        job = resume_parser.get_most_recent_job()
        if not job:
            print("⚠️ No work experience found in resume")
            return
        
        fields_to_fill = {
            'company': job['company'],
            'jobTitle': job['title'],
            'employmentPeriod': job['dates'],
            'jobDescription': '\n'.join(job['description'])
        }
        
        # Fill regular fields
        for field_name, value in fields_to_fill.items():
            print(f"\nLooking for {field_name} field...")
            success = self._fill_by_attribute(page, field_name, value)
            if success:
                print(f"✅ Filled {field_name} successfully")
            else:
                print(f"⚠️ Could not find or fill {field_name} field")
        
        # Handle location separately
        if job['location']:
            print("\nLooking for location dropdown...")
            self._handle_location_dropdowns(page, job['location'])

    def handle_greenhouse_dropdowns(self, page):
        # Handle dropdown fields that use the select__input class
        dropdown_fields = {
            'question_7392023005': {'label': 'Work Authorization', 'value': 'Yes'},
            'question_7392024005': {'label': 'Will you now or in the future require sponsorship', 'value': 'No'},  # Explicitly set to No
            'gender': {'label': 'Gender', 'value': 'Male'},
            'hispanic_ethnicity': {'label': 'Hispanic/Latino', 'value': 'No'},
            'race': {'label': 'Race', 'value': 'Two or More Races'},
            'veteran_status': {'label': 'Veteran Status', 'value': 'I am not a protected veteran'},
            'disability_status': {'label': 'Disability Status', 'value': 'No, I Have Never Had A Disability'}
        }
        
        for field_id, info in dropdown_fields.items():
            try:
                # Find the dropdown container
                dropdown = page.query_selector(f'#{field_id}')
                if dropdown:
                    # Click to open dropdown
                    dropdown.click()
                    page.wait_for_timeout(1000)  # Wait for dropdown to open
                    
                    # Special handling for sponsorship question to ensure "No" is selected
                    if field_id == 'question_7392024005':
                        options = page.query_selector_all('[class*="select__option"]')
                        for option in options:
                            option_text = option.text_content().strip()
                            if option_text.lower() == 'no':
                                option.click()
                                print(f"✅ Selected 'No' for sponsorship requirement")
                                break
                        continue

                    # Handle other dropdowns normally
                    options = page.query_selector_all('[class*="select__option"]')
                    for option in options:
                        option_text = option.text_content().strip()
                        if option_text == info['value']:
                            option.click()
                            print(f"✅ Selected '{option_text}' for {info['label']}")
                            break
                    
                    page.wait_for_timeout(500)  # Wait for selection to register
                
            except Exception as e:
                print(f"⚠️ Failed to handle dropdown {info['label']}: {e}")