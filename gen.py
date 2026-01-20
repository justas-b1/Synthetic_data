import json
import secrets
import random
import csv
import os

def generate_random_file_name(secure=True):
    """
    Generates random 32-character strings that perfectly mimic MD5 hash format
    Uses the exact same character set as real MD5: 0-9 and a-f
    """
    md5_chars = '0123456789abcdef'
    
    if secure:
        return ''.join(secrets.choice(md5_chars) for _ in range(32))
    else:
        return ''.join(random.choice(md5_chars) for _ in range(32))

def weighted_choice(options):
    """
    Select an option based on percentage chances
    """
    # Debug: Check if options list is empty
    if not options:
        print("ERROR: Empty options list provided to weighted_choice")
        return ""
    
    # Debug: Check structure of options
    for i, option_data in enumerate(options):
        if "option" not in option_data or "percentage_chance" not in option_data:
            print(f"ERROR: Malformed option at index {i}: {option_data}")
            return ""
    
    choices = []
    weights = []
    
    for option_data in options:
        choices.append(option_data["option"])
        weights.append(option_data["percentage_chance"])
    
    # Debug: Verify lengths match
    if len(choices) != len(weights):
        print(f"ERROR: Choices length ({len(choices)}) doesn't match weights length ({len(weights)})")
        print(f"Choices: {choices}")
        print(f"Weights: {weights}")
        return ""
    
    # Debug: Check for zero weights
    if sum(weights) == 0:
        print("ERROR: All weights are zero")
        return random.choice(choices) if choices else ""
    
    # Debug: Print what we're about to process
    #print(f"DEBUG weighted_choice: {len(choices)} choices, {len(weights)} weights")
    #print(f"  Choices: {choices}")
    #print(f"  Weights: {weights}")
    
    try:
        result = random.choices(choices, weights=weights, k=1)[0]
        #print(f"  Selected: {result}")
        return result
    except ValueError as e:
        print(f"ERROR in random.choices: {e}")
        print(f"Choices: {choices} (length: {len(choices)})")
        print(f"Weights: {weights} (length: {len(weights)})")
        # Fallback to simple random choice
        return random.choice(choices) if choices else ""

def get_age_from_range(age_range):
    """
    For age ranges like "18-24", pick a random number within that range
    """
    if "-" in age_range:
        try:
            start, end = age_range.split("-")
            return str(random.randint(int(start), int(end)))
        except:
            return age_range
    return age_range

class DataGenerator:
    def __init__(self, datasets_folder="datasets"):
        self.datasets_folder = datasets_folder
        self.female_names = []
        self.male_names = []
        self.last_names = []
        self.common_words = []
        self.streets = []
        
        # Load all datasets
        self.load_datasets()
        
    def load_datasets(self):
        """Load all dataset files from the datasets folder"""
        try:
            # Load female names
            with open(os.path.join(self.datasets_folder, "Female.txt"), 'r', encoding='utf-8') as f:
                self.female_names = [line.strip() for line in f if line.strip()]
            
            # Load male names
            with open(os.path.join(self.datasets_folder, "Male.txt"), 'r', encoding='utf-8') as f:
                self.male_names = [line.strip() for line in f if line.strip()]
            
            # Load last names
            with open(os.path.join(self.datasets_folder, "Last.txt"), 'r', encoding='utf-8') as f:
                self.last_names = [line.strip() for line in f if line.strip()]
            
            # Load common words
            with open(os.path.join(self.datasets_folder, "Common_words.txt"), 'r', encoding='utf-8') as f:
                self.common_words = [line.strip() for line in f if line.strip()]
            
            # Load streets
            with open(os.path.join(self.datasets_folder, "Streets.txt"), 'r', encoding='utf-8') as f:
                self.streets = [line.strip() for line in f if line.strip()]
                
            #print(f"✅ Loaded datasets: {len(self.female_names)} female, {len(self.male_names)} male, "
            #      f"{len(self.last_names)} last names, {len(self.common_words)} words, {len(self.streets)} streets")
                  
        except FileNotFoundError as e:
            print(f"❌ Error loading datasets: {e}")
            print("Please make sure the 'datasets' folder exists with all required .txt files")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def get_gender_from_identity(self, gender_identity):
        """Convert gender identity to simple male/female for name selection"""
        gender_identity_lower = gender_identity.lower()
        
        if any(word in gender_identity_lower for word in ["woman", "female", "feminine"]):
            return "female"
        elif any(word in gender_identity_lower for word in ["man", "male", "masculine"]):
            return "male"
        else:
            # For non-binary, transgender, agender, etc., default to male
            return "male"

    def generate_middle_name(self, first_name, last_name, has_middle_name):
        """Generate realistic middle name ensuring it doesn't equal first or last name"""
        if not has_middle_name:
            return ""
        
        # Determine middle name type with weighted probabilities
        middle_name_type = random.choices(
            ['full_name', 'initial_with_period', 'initial_no_period', 'double_initial'],
            weights=[65, 20, 10, 5],  # 65% full names, 20% initial with period, etc.
            k=1
        )[0]
        
        if middle_name_type == 'full_name':
            # Use a full middle name (most common)
            for _ in range(15):  # Increased attempts to find unique name
                all_names = self.male_names + self.female_names
                middle_name = random.choice(all_names)
                
                # Additional checks to ensure the middle name is distinct and realistic
                if (middle_name.lower() != first_name.lower() and 
                    middle_name.lower() != last_name.lower() and
                    len(middle_name) > 1 and  # Ensure it's not a single letter
                    middle_name[0].lower() != first_name[0].lower() and  # Not same initial as first name
                    middle_name[0].lower() != last_name[0].lower() and   # Not same initial as last name
                    not middle_name.startswith(first_name[:2]) and  # Doesn't start with first 2 chars of first name
                    not middle_name.startswith(last_name[:2])):     # Doesn't start with first 2 chars of last name
                    return middle_name
        
        elif middle_name_type == 'initial_with_period':
            # Initial with period (e.g., "J.", "M.")
            initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            # Ensure initial doesn't match first or last name initial
            if initial != first_name[0] and initial != last_name[0]:
                return f"{initial}."
            else:
                # If initials match, try a different letter
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    if letter != first_name[0] and letter != last_name[0]:
                        return f"{letter}."
        
        elif middle_name_type == 'initial_no_period':
            # Initial without period (less common but exists)
            initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if initial != first_name[0] and initial != last_name[0]:
                return initial
        
        elif middle_name_type == 'double_initial':
            # Double initial (e.g., "AJ", "MK") - rare but realistic
            first_initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            second_initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            double_initial = f"{first_initial}{second_initial}"
            # Ensure it doesn't match first name initials
            if (double_initial != first_name[:2].upper() and 
                double_initial != last_name[:2].upper() and
                first_initial != first_name[0] and 
                first_initial != last_name[0]):
                return double_initial
        
        # Fallback: if we couldn't generate a suitable middle name, return empty
        # But first try a few common middle names as last resort
        common_middle_names = ["Marie", "Ann", "Lynn", "James", "Michael", "David", "Lee", "Ray", "Jean", "Grace"]
        for common_name in common_middle_names:
            if (common_name.lower() != first_name.lower() and 
                common_name.lower() != last_name.lower()):
                return common_name
        
        return ""

    def generate_email_variations(self, first_name, last_name):
        """Generate email with multiple variations using Pareto principle for domains"""
        # Pareto principle: 80% of emails use 20% of domains
        domains = [
            # Top Tier - 80% probability (gmail, outlook, icloud, yahoo)
            {"domain": "gmail.com", "weight": 35},
            {"domain": "outlook.com", "weight": 20},
            {"domain": "yahoo.com", "weight": 12},
            {"domain": "icloud.com", "weight": 13},
            
            # Established Providers - 12% probability
            {"domain": "hotmail.com", "weight": 4},
            {"domain": "aol.com", "weight": 3},
            {"domain": "protonmail.com", "weight": 2},
            {"domain": "mail.com", "weight": 1},
            {"domain": "gmx.com", "weight": 1},
            {"domain": "zoho.com", "weight": 1},
            
            # Regional & Specialized - 5% probability
            {"domain": "yandex.com", "weight": 1},
            {"domain": "fastmail.com", "weight": 1},
            {"domain": "live.com", "weight": 1},
            {"domain": "me.com", "weight": 1},
            {"domain": "msn.com", "weight": 1},
            
            # Business & Professional - 2% probability
            {"domain": "outlook.co.uk", "weight": 0.5},
            {"domain": "yahoo.co.uk", "weight": 0.5},
            {"domain": "yahoo.de", "weight": 0.5},
            {"domain": "yahoo.fr", "weight": 0.5},
            {"domain": "rocketmail.com", "weight": 0.5},
            
            # Additional Common Domains - 1% probability
            {"domain": "inbox.com", "weight": 0.3},
            {"domain": "hushmail.com", "weight": 0.3},
            {"domain": "lavabit.com", "weight": 0.2},
            {"domain": "lycos.com", "weight": 0.2},
            {"domain": "aim.com", "weight": 0.2},
            {"domain": "gmx.us", "weight": 0.2},
            {"domain": "gmx.de", "weight": 0.2},
            {"domain": "gmx.fr", "weight": 0.2},
            {"domain": "web.de", "weight": 0.2},
            {"domain": "t-online.de", "weight": 0.2},
            {"domain": "orange.fr", "weight": 0.2},
            {"domain": "sfr.fr", "weight": 0.2},
            {"domain": "libero.it", "weight": 0.2},
            {"domain": "alice.it", "weight": 0.2},
            {"domain": "mail.ru", "weight": 0.2},
            {"domain": "rambler.ru", "weight": 0.2},
            {"domain": "qq.com", "weight": 0.2},
            {"domain": "163.com", "weight": 0.2},
            {"domain": "126.com", "weight": 0.2},
            {"domain": "naver.com", "weight": 0.2},
            {"domain": "daum.net", "weight": 0.2},
            {"domain": "hanmail.net", "weight": 0.2},
            {"domain": "seznam.cz", "weight": 0.2},
            {"domain": "wp.pl", "weight": 0.2},
            {"domain": "o2.pl", "weight": 0.2},
            {"domain": "onet.pl", "weight": 0.2},
            {"domain": "interia.pl", "weight": 0.2},
            {"domain": "ziggo.nl", "weight": 0.2},
            {"domain": "kpnmail.nl", "weight": 0.2},
            {"domain": "planet.nl", "weight": 0.2},
            {"domain": "telenet.be", "weight": 0.2},
            {"domain": "skynet.be", "weight": 0.2},
            {"domain": "bluewin.ch", "weight": 0.2},
            {"domain": "sunrise.ch", "weight": 0.2},
            {"domain": "swissonline.ch", "weight": 0.2},
            {"domain": "bigpond.com", "weight": 0.2},
            {"domain": "optusnet.com.au", "weight": 0.2},
            {"domain": "telstra.com", "weight": 0.2},
            {"domain": "iinet.net.au", "weight": 0.2},
            {"domain": "comcast.net", "weight": 0.2},
            {"domain": "verizon.net", "weight": 0.2},
            {"domain": "att.net", "weight": 0.2},
            {"domain": "sbcglobal.net", "weight": 0.2},
            {"domain": "bellsouth.net", "weight": 0.2},
            {"domain": "earthlink.net", "weight": 0.2},
            {"domain": "cox.net", "weight": 0.2},
            {"domain": "charter.net", "weight": 0.2},
            {"domain": "juno.com", "weight": 0.2},
            {"domain": "netzero.net", "weight": 0.2},
            {"domain": "frontier.com", "weight": 0.2},
            {"domain": "windstream.net", "weight": 0.2},
            {"domain": "centurylink.net", "weight": 0.2},
        ]
        
        # More realistic number ranges
        short_numbers = random.randint(1, 99)  # Most common: 1-2 digits
        medium_numbers = random.randint(100, 999)  # Less common: 3 digits  
        long_numbers = random.randint(1000, 9999)  # Rare: 4 digits
        
        current_year = random.randint(1990, 2024)
        birth_year = random.randint(1950, 2005)  # More realistic for age context
        
        email_formats = [
            # Basic name combinations (most common - 30%)
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{last_name[0].lower()}",
            f"{first_name.lower()}_{last_name.lower()}",
            f"{first_name.lower()}-{last_name.lower()}",
            
            # With SHORT numbers (common - 20%)
            f"{first_name.lower()}{short_numbers}",
            f"{last_name.lower()}{short_numbers}",
            f"{first_name.lower()}.{last_name.lower()}{short_numbers}",
            f"{first_name.lower()}{last_name.lower()}{short_numbers}",
            f"{first_name[0].lower()}{last_name.lower()}{short_numbers}",
            f"{first_name.lower()}{last_name[0].lower()}{short_numbers}",
            
            # Year-based (age appropriate - 8%)
            f"{first_name.lower()}{birth_year}",
            f"{last_name.lower()}{birth_year}",
            f"{first_name.lower()}{str(birth_year)[-2:]}",  # Last 2 digits of birth year
            f"{first_name.lower()}.{last_name.lower()}{str(birth_year)[-2:]}",
            
            # Initial combinations (4%)
            f"{first_name[0].lower()}{last_name[0].lower()}{short_numbers}",
            f"{first_name[0].lower()}.{last_name[0].lower()}.{short_numbers}",
            f"{first_name[0].lower()}_{last_name[0].lower()}_{short_numbers}",
            
            # Name fragments (4%)
            f"{first_name[:3].lower()}{last_name[:3].lower()}",
            f"{first_name[:4].lower()}{last_name[:2].lower()}",
            f"{first_name[:2].lower()}{last_name[:4].lower()}{short_numbers}",
            
            # With medium/long numbers (less common - 4%)
            f"{first_name.lower()}{medium_numbers}",
            f"{first_name[0].lower()}{last_name.lower()}{medium_numbers}",
            f"{first_name.lower()}{last_name[0].lower()}{long_numbers}",
            
            # COMMON WORD COMBINATIONS (25%)
            # Single common word + numbers
            f"{random.choice(self.common_words).lower()}{short_numbers}",
            f"{random.choice(self.common_words).lower()}{medium_numbers}",
            
            # Common word + name combinations
            f"{random.choice(self.common_words).lower()}.{first_name.lower()}",
            f"{first_name.lower()}.{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}_{first_name.lower()}",
            f"{first_name.lower()}_{random.choice(self.common_words).lower()}",
            
            # Common word + last name combinations
            f"{random.choice(self.common_words).lower()}.{last_name.lower()}",
            f"{last_name.lower()}.{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}_{last_name.lower()}",
            f"{last_name.lower()}_{random.choice(self.common_words).lower()}",
            
            # Double common word combinations
            f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}.{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}_{random.choice(self.common_words).lower()}",
            
            # Common word + name + numbers
            f"{random.choice(self.common_words).lower()}{first_name.lower()}{short_numbers}",
            f"{first_name.lower()}{random.choice(self.common_words).lower()}{short_numbers}",
            f"{random.choice(self.common_words).lower()}{last_name.lower()}{short_numbers}",
            f"{last_name.lower()}{random.choice(self.common_words).lower()}{short_numbers}",
            
            # Common word fragments + numbers
            f"{random.choice(self.common_words)[:3].lower()}{short_numbers}",
            f"{random.choice(self.common_words)[:4].lower()}{medium_numbers}",
        ]
        
        # FIXED: Updated weights - EXACTLY matching the number of email formats
        format_weights = [
            # Basic name combinations (6 weights - 30%)
            14, 14, 13, 10, 10, 8,
            
            # With short numbers (6 weights - 20%)
            9, 9, 9, 6, 5, 5,
            
            # Year-based (4 weights - 8%)
            4, 3, 2, 1,
            
            # Initial combinations (3 weights - 4%)
            3, 2, 2,
            
            # Name fragments (3 weights - 4%)
            3, 2, 2,
            
            # With medium/long numbers (3 weights - 4%)
            3, 2, 2,
            
            # COMMON WORD COMBINATIONS (20 weights - 25%)
            # Single common word + numbers (2)
            1, 1,
            
            # Common word + name combinations (4)
            1, 1, 1, 1,
            
            # Common word + last name combinations (4)
            1, 1, 1, 1,
            
            # Double common word combinations (3)
            1, 1, 1,
            
            # Common word + name + numbers (4)
            1, 1, 1, 1,
            
            # Common word fragments + numbers (2)
            1, 1,
        ]
        
        # Select domain using weighted choice
        domain_choices = [d["domain"] for d in domains]
        domain_weights = [d["weight"] for d in domains]
        selected_domain = random.choices(domain_choices, weights=domain_weights, k=1)[0]
        
        # DEBUG: Check if email format counts match
        #print(f"DEBUG EMAIL: {len(email_formats)} formats vs {len(format_weights)} weights")
        if len(email_formats) != len(format_weights):
            print(f"❌ EMAIL FORMAT MISMATCH! Using fallback random choice")
            selected_format = random.choice(email_formats)
        else:
            # Select email format using weighted choice
            selected_format = random.choices(email_formats, weights=format_weights, k=1)[0]
        
        return f"{selected_format}@{selected_domain}"

    def generate_phone_number(self, country, include_phone=True):
        """Generate phone number with correct format for country"""
        if not include_phone:
            return "", "", ""  # Return empty strings when no phone is requested
            
        phone_formats = {
            "United States": {
                "format": "+1-{}-{}-{}",
                "code": "+1",
                "parts": [
                    lambda: f"{random.randint(200, 999)}",
                    lambda: f"{random.randint(200, 999)}", 
                    lambda: f"{random.randint(1000, 9999)}"
                ]
            },
            "United Kingdom": {
                "format": "+44-{} {}",
                "code": "+44", 
                "parts": [
                    lambda: f"{random.randint(20, 28)}",
                    lambda: f"{random.randint(1000, 9999)} {random.randint(1000, 9999)}"
                ]
            },
            "Canada": {
                "format": "+1-{}-{}-{}",
                "code": "+1",
                "parts": [
                    lambda: f"{random.randint(200, 999)}",
                    lambda: f"{random.randint(200, 999)}",
                    lambda: f"{random.randint(1000, 9999)}"
                ]
            },
            "Australia": {
                "format": "+61-{} {}",
                "code": "+61",
                "parts": [
                    lambda: f"{random.randint(2, 9)}",
                    lambda: f"{random.randint(1000, 9999)} {random.randint(1000, 9999)}"
                ]
            },
            "Ireland": {
                "format": "+353-{}",
                "code": "+353", 
                "parts": [
                    lambda: f"{random.randint(1, 99)} {random.randint(100000, 999999)}"
                ]
            },
            "New Zealand": {
                "format": "+64-{}",
                "code": "+64",
                "parts": [
                    lambda: f"{random.randint(2, 9)} {random.randint(100000, 999999)}"
                ]
            }
        }
        
        country_data = phone_formats.get(country, phone_formats["United States"])
        
        # Generate the phone parts
        phone_parts = [part() for part in country_data["parts"]]
        
        # Format the phone number
        try:
            full_phone = country_data["format"].format(*phone_parts)
        except IndexError:
            # Fallback to simple format if there's a formatting error
            full_phone = f"{country_data['code']}-{'-'.join(phone_parts)}"
        
        return full_phone, full_phone, country_data["code"]

    def generate_personal_info(self, gender_identity, age, country):
        """Generate realistic personal information using cached gender, age, and country"""
        # Convert gender identity to simple male/female for name selection
        simple_gender = self.get_gender_from_identity(gender_identity)
        
        # Determine if names should be empty (18% chance) or filled (67% chance)
        names_empty = random.random() < 0.12
        
        if names_empty:
            # 18% of the time: all names are empty
            first_name = ""
            last_name = ""
            middle_name = ""
            has_middle_name = False
            # When names are empty, phone number should also be blank
            include_phone = False
        else:
            # 67% of the time: generate names
            if simple_gender == "female":
                first_name = random.choice(self.female_names)
            else:
                first_name = random.choice(self.male_names)
                
            last_name = random.choice(self.last_names)
            
            # From the 67% with names, 22% should have middle names (which is about 33% of the filled names)
            has_middle_name = random.random() < 0.33
            middle_name = self.generate_middle_name(first_name, last_name, has_middle_name)
            
            # Only generate phone number when names are present (30% chance)
            include_phone = random.random() < 0.3
        
        # Generate email with variations (only if we have names to work with)
        if first_name and last_name:
            email = self.generate_email_variations(first_name, last_name)
        else:
            # If no names, generate email using common words only
            email = self.generate_email_from_common_words_only()
        
        # Generate nickname (only if we have at least a first name)
        if first_name:
            nickname = self.generate_nickname_variations(first_name, last_name, simple_gender)
        else:
            nickname = self.generate_nickname_from_common_words_only()
        
        # Generate timezone FIRST so it's available for address generation
        timezone_variations = {
            "United States": [
                "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
                "America/Phoenix", "America/Anchorage", "America/Honolulu", "America/Detroit",
                "America/Indiana/Indianapolis", "America/Boise", "America/Juneau"
            ],
            "United Kingdom": [
                "Europe/London", "Europe/Belfast", "Europe/Guernsey", "Europe/Isle_of_Man",
                "Europe/Jersey"
            ],
            "Canada": [
                "America/Toronto", "America/Vancouver", "America/Edmonton", "America/Winnipeg",
                "America/Halifax", "America/St_Johns", "America/Regina", "America/Yellowknife",
                "America/Whitehorse", "America/Iqaluit"
            ],
            "Australia": [
                "Australia/Sydney", "Australia/Melbourne", "Australia/Brisbane", "Australia/Perth",
                "Australia/Adelaide", "Australia/Darwin", "Australia/Hobart", "Australia/Lord_Howe",
                "Australia/Eucla", "Australia/Lindeman"
            ],
            "Ireland": [
                "Europe/Dublin", "Europe/Cork", "Europe/Galway", "Europe/Limerick",
                "Europe/Waterford"
            ],
            "New Zealand": [
                "Pacific/Auckland", "Pacific/Chatham", "Pacific/Wellington", "Pacific/Christchurch",
                "Pacific/Hamilton", "Pacific/Dunedin"
            ]
        }
        
        # Get timezone variations for the country, fallback to common timezones
        country_timezones = timezone_variations.get(country, [
            "UTC", "Europe/London", "America/New_York", "Europe/Berlin", 
            "Europe/Paris", "Asia/Tokyo", "Australia/Sydney"
        ])
        
        timezone = random.choice(country_timezones)
        
        # NOW generate address with the timezone available
        has_address = random.random() < 0.25
        if has_address:
            address, zip_code = self.generate_address_variations(country, timezone)
        else:
            address = ""
            zip_code = ""
        
        # Generate phone number (will be blank if include_phone is False)
        phone, mobile, phone_code = self.generate_phone_number(country, include_phone)
        
        return {
            "email": email,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "nick_name": nickname,
            "gender": simple_gender,
            "age": age,
            "country": country,
            "state": "",
            "city": "",
            "address": address,
            "zip": zip_code,
            "phone": phone,
            "mobile": mobile,
            "phone_country_code": phone_code,
            "timezone": timezone,
            "customer_key": ""
        }
        
    def generate_email_from_common_words_only(self):
        """Generate email using only common words when no names are available"""
        # More realistic domains for anonymous accounts
        domains = [
            # Top Tier - 80% probability (gmail, outlook, icloud, yahoo)
            {"domain": "gmail.com", "weight": 35},
            {"domain": "outlook.com", "weight": 20},
            {"domain": "yahoo.com", "weight": 12},
            {"domain": "icloud.com", "weight": 13},
            
            # Established Providers - 12% probability
            {"domain": "hotmail.com", "weight": 4},
            {"domain": "aol.com", "weight": 3},
            {"domain": "protonmail.com", "weight": 2},
            {"domain": "mail.com", "weight": 1},
            {"domain": "gmx.com", "weight": 1},
            {"domain": "zoho.com", "weight": 1},
            
            # Regional & Specialized - 5% probability
            {"domain": "yandex.com", "weight": 1},
            {"domain": "fastmail.com", "weight": 1},
            {"domain": "live.com", "weight": 1},
            {"domain": "me.com", "weight": 1},
            {"domain": "msn.com", "weight": 1},
            
            # Business & Professional - 2% probability
            {"domain": "outlook.co.uk", "weight": 0.5},
            {"domain": "yahoo.co.uk", "weight": 0.5},
            {"domain": "yahoo.de", "weight": 0.5},
            {"domain": "yahoo.fr", "weight": 0.5},
            {"domain": "rocketmail.com", "weight": 0.5},
            
            # Additional Common Domains - 1% probability
            {"domain": "inbox.com", "weight": 0.3},
            {"domain": "hushmail.com", "weight": 0.3},
            {"domain": "lavabit.com", "weight": 0.2},
            {"domain": "lycos.com", "weight": 0.2},
            {"domain": "aim.com", "weight": 0.2},
            {"domain": "gmx.us", "weight": 0.2},
            {"domain": "gmx.de", "weight": 0.2},
            {"domain": "gmx.fr", "weight": 0.2},
            {"domain": "web.de", "weight": 0.2},
            {"domain": "t-online.de", "weight": 0.2},
            {"domain": "orange.fr", "weight": 0.2},
            {"domain": "sfr.fr", "weight": 0.2},
            {"domain": "libero.it", "weight": 0.2},
            {"domain": "alice.it", "weight": 0.2},
            {"domain": "mail.ru", "weight": 0.2},
            {"domain": "rambler.ru", "weight": 0.2},
            {"domain": "qq.com", "weight": 0.2},
            {"domain": "163.com", "weight": 0.2},
            {"domain": "126.com", "weight": 0.2},
            {"domain": "naver.com", "weight": 0.2},
            {"domain": "daum.net", "weight": 0.2},
            {"domain": "hanmail.net", "weight": 0.2},
            {"domain": "seznam.cz", "weight": 0.2},
            {"domain": "wp.pl", "weight": 0.2},
            {"domain": "o2.pl", "weight": 0.2},
            {"domain": "onet.pl", "weight": 0.2},
            {"domain": "interia.pl", "weight": 0.2},
            {"domain": "ziggo.nl", "weight": 0.2},
            {"domain": "kpnmail.nl", "weight": 0.2},
            {"domain": "planet.nl", "weight": 0.2},
            {"domain": "telenet.be", "weight": 0.2},
            {"domain": "skynet.be", "weight": 0.2},
            {"domain": "bluewin.ch", "weight": 0.2},
            {"domain": "sunrise.ch", "weight": 0.2},
            {"domain": "swissonline.ch", "weight": 0.2},
            {"domain": "bigpond.com", "weight": 0.2},
            {"domain": "optusnet.com.au", "weight": 0.2},
            {"domain": "telstra.com", "weight": 0.2},
            {"domain": "iinet.net.au", "weight": 0.2},
            {"domain": "comcast.net", "weight": 0.2},
            {"domain": "verizon.net", "weight": 0.2},
            {"domain": "att.net", "weight": 0.2},
            {"domain": "sbcglobal.net", "weight": 0.2},
            {"domain": "bellsouth.net", "weight": 0.2},
            {"domain": "earthlink.net", "weight": 0.2},
            {"domain": "cox.net", "weight": 0.2},
            {"domain": "charter.net", "weight": 0.2},
            {"domain": "juno.com", "weight": 0.2},
            {"domain": "netzero.net", "weight": 0.2},
            {"domain": "frontier.com", "weight": 0.2},
            {"domain": "windstream.net", "weight": 0.2},
            {"domain": "centurylink.net", "weight": 0.2},
        ]
        
        # More realistic number patterns for anonymous emails
        short_numbers = random.randint(1, 99)  # Most common
        medium_numbers = random.randint(100, 999)  # Less common
        current_year = random.randint(2010, 2024)
        
        email_formats = [
            # Common word combinations (most realistic)
            f"{random.choice(self.common_words).lower()}{short_numbers}",
            f"{random.choice(self.common_words).lower()}.{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}_{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}{current_year}",
            
            # Double common words
            f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}",
            f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{short_numbers}",
        ]
        
        # Select domain
        domain_choices = [d["domain"] for d in domains]
        domain_weights = [d["weight"] for d in domains]
        selected_domain = random.choices(domain_choices, weights=domain_weights, k=1)[0]
        
        selected_format = random.choice(email_formats)
        return f"{selected_format}@{selected_domain}"

    def generate_nickname_from_common_words_only(self):
        """Generate nickname using only common words when no names are available"""
        nickname_patterns = [
            # Basic combinations (most common)
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).lower()}{random.randint(1, 999)}",
            lambda: f"{random.choice(self.common_words).capitalize()}{random.choice(self.common_words).capitalize()}",
            lambda: f"{random.choice(self.common_words).lower()}{random.randint(10, 99)}{random.choice(self.common_words).lower()}",
            lambda: f"{random.randint(100, 999)}{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).lower()}-{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).lower()}_{random.choice(self.common_words).lower()}",
            
            # More variations in the same style
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.randint(1, 99)}",
            lambda: f"{random.randint(1, 99)}{random.choice(self.common_words).lower()}{random.randint(1, 99)}",
            lambda: f"{random.choice(self.common_words).upper()}{random.choice(self.common_words).upper()}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(['x','z','q','v'])}{random.randint(1, 999)}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).capitalize()}{random.choice(self.common_words).lower()}{random.randint(10, 999)}",
            lambda: f"{random.choice(self.common_words).lower()}{random.randint(1000, 9999)}",
            lambda: f"{random.randint(100, 999)}{random.choice(self.common_words).lower()}{random.randint(100, 999)}",
            lambda: f"{random.choice(self.common_words).lower()}.{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(['','','','','','_','-'])}{random.randint(100, 999)}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words)[:3].lower()}",
            lambda: f"{random.choice(self.common_words)[:3].lower()}{random.choice(self.common_words).lower()}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(['','','','','','1','2','3'])}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.choice(['','','','_','-'])}{random.randint(1, 99)}",
            lambda: f"{random.randint(1, 9)}{random.choice(self.common_words).lower()}{random.randint(1, 9)}",
            lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.randint(1, 9)}",
            lambda: f"{random.choice(self.common_words).capitalize()}{random.choice(self.common_words).capitalize()}{random.randint(10, 99)}",
            lambda: f"{random.choice(self.common_words).lower()}-{random.randint(100, 999)}-{random.choice(self.common_words).lower()}",
            
            # 22% fast-typed gibberish patterns
            lambda: ''.join(random.choices('asdfghjklqwertyuiopzxcvbnm', k=random.randint(4, 8))),
            lambda: ''.join(random.choices('asdfghjkl', k=random.randint(3, 6))),
            lambda: ''.join(random.choices('qwertyuiop', k=random.randint(4, 7))),
            lambda: ''.join(random.choices('zxcvbnm', k=random.randint(3, 5))),
            lambda: f"{''.join(random.choices('asdfghjkl', k=3))}{random.randint(10, 999)}",
            lambda: f"{random.randint(10, 99)}{''.join(random.choices('qwertyuiop', k=4))}",
            lambda: f"{''.join(random.choices('asdf', k=2))}{''.join(random.choices('jkl', k=2))}{random.randint(1, 9)}",
            lambda: f"{''.join(random.choices('asdfgh', k=4))}{random.choice(['','','1','2','12','123'])}",
            lambda: f"{random.randint(100, 999)}{''.join(random.choices('jklpoiu', k=3))}",
            lambda: ''.join(random.choices('asdfjkl', k=random.randint(5, 8))),
        ]
        
        # 22% chance for gibberish (last 11 patterns out of 39 total)
        gibberish_patterns = nickname_patterns[-11:]
        normal_patterns = nickname_patterns[:-11]
        
        if random.random() < 0.5:
            return random.choice(gibberish_patterns)()
        else:
            return random.choice(normal_patterns)()

    def generate_address_variations(self, country, timezone=""):
        """Generate realistic address variations with matching ZIP/postal codes"""
        street = random.choice(self.streets)
        
        # Enhanced address format variations with weights
        address_formats = [
            # Standard formats (most common)
            {"pattern": lambda: f"{random.randint(1, 9999)} {street}", "weight": 35},
            {"pattern": lambda: f"{random.randint(1, 999)} {random.choice(['N', 'S', 'E', 'W'])} {street}", "weight": 12},
            {"pattern": lambda: f"{random.randint(1, 999)} {street} {random.choice(['Apt', 'Unit', 'Suite'])} {random.randint(1, 999)}", "weight": 10},
            {"pattern": lambda: f"{random.randint(1, 999)} {random.choice(['North', 'South', 'East', 'West'])} {street}", "weight": 8},
            
            # PO Box variations
            {"pattern": lambda: f"PO Box {random.randint(100, 9999)}", "weight": 6},
            {"pattern": lambda: f"P.O. Box {random.randint(100, 9999)}", "weight": 3},
            
            # Rural/route addresses
            {"pattern": lambda: f"RR {random.randint(1, 9)} Box {random.randint(10, 999)}", "weight": 4},
            {"pattern": lambda: f"Route {random.randint(1, 9)} Box {random.randint(10, 999)}", "weight": 2},
            {"pattern": lambda: f"County Road {random.randint(1, 99)}", "weight": 2},
            
            # Building names (apartments/condos)
            {"pattern": lambda: f"{random.randint(1, 999)} {random.choice(['Park', 'Garden', 'View', 'Lake', 'Oak', 'Maple', 'Pine'])} {random.choice(['Avenue', 'Drive', 'Lane'])}", "weight": 5},
            {"pattern": lambda: f"{random.choice(['The', ''])}{random.choice(self.common_words).capitalize()} {random.choice(['Building', 'Plaza', 'Center', 'Towers'])}", "weight": 3},
            {"pattern": lambda: f"{random.randint(1, 999)} {random.choice(['Apartment', 'Condominium', 'Complex'])} {random.choice(['A', 'B', 'C', 'D'])}", "weight": 2},
            
            # Complex numbers (like 123A, 456-B)
            {"pattern": lambda: f"{random.randint(1, 9999)}{random.choice(['', 'A', 'B', 'C', 'D'])} {street}", "weight": 5},
            {"pattern": lambda: f"{random.randint(1, 999)}-{random.choice(['A', 'B', 'C', 'D'])} {street}", "weight": 2},
            
            # Fractional addresses (like 123 1/2)
            {"pattern": lambda: f"{random.randint(1, 999)} 1/2 {street}", "weight": 1},
            
            # Named buildings with units
            {"pattern": lambda: f"{random.choice(self.common_words).capitalize()} {random.choice(['House', 'Hall', 'Manor', 'Court'])} Unit {random.randint(1, 99)}", "weight": 2},
            
            # Intersections (less common)
            {"pattern": lambda: f"Corner of {street} and {random.choice(self.streets)}", "weight": 1},
            
            # UK-style addresses
            {"pattern": lambda: f"{random.randint(1, 999)} {random.choice(['High Street', 'Main Road', 'Church Lane', 'Station Road'])}", "weight": 3},
            {"pattern": lambda: f"Flat {random.randint(1, 99)}, {random.randint(1, 999)} {street}", "weight": 2},
        ]
        
        # Select address format using weights
        patterns = [p["pattern"] for p in address_formats]
        weights = [p["weight"] for p in address_formats]
        address = random.choices(patterns, weights=weights, k=1)[0]()
        
        # Generate matching ZIP/postal code based on country and timezone
        has_zip = random.random() < 0.7
        if has_zip:
            zip_code = self.generate_matching_zip_code(country, timezone)
        else:
            zip_code = ""
        
        return address, zip_code

    def generate_matching_zip_code(self, country, timezone=""):
        """Generate ZIP/postal codes that match the geographic location"""
        
        # More specific ZIP code ranges by major cities and regions
        us_zip_ranges = {
            # Northeast - America/New_York
            "America/New_York": [
                # New York City
                (10001, 10282),  # Manhattan
                (10301, 10314),  # Staten Island
                (10451, 10475),  # Bronx
                (11201, 11256),  # Brooklyn
                (11351, 11451),  # Queens
                # New Jersey (NYC metro)
                (7001, 8999),    # Northern NJ
                # Philadelphia
                (19019, 19199),  # Philadelphia, PA
                # Boston
                (2108, 2137),    # Boston, MA
                (2201, 2238),    # Boston suburbs
                # Washington DC
                (20001, 20020),  # Washington DC
                (20331, 20599),  # DC area
                # Atlanta
                (30002, 30399),  # Atlanta, GA
                # Miami
                (33101, 33199),  # Miami, FL
            ],
            
            # Midwest - America/Chicago
            "America/Chicago": [
                # Chicago
                (60007, 60827),  # Chicago metro
                (60601, 60661),  # Chicago city
                # Detroit
                (48021, 48375),  # Detroit metro
                (48201, 48288),  # Detroit city
                # Minneapolis
                (55016, 56763),  # Minnesota
                (55101, 55488),  # Minneapolis-St Paul
                # St. Louis
                (62002, 63199),  # St. Louis area
                # Indianapolis
                (46032, 46298),  # Indianapolis
                # Milwaukee
                (53001, 53295),  # Milwaukee area
                # Kansas City
                (64012, 64199),  # Kansas City area
            ],
            
            # Mountain - America/Denver
            "America/Denver": [
                # Denver
                (80001, 81658),  # Colorado
                (80002, 80299),  # Denver metro
                # Phoenix
                (85001, 86556),  # Arizona
                (85001, 85099),  # Phoenix metro
                # Salt Lake City
                (84001, 84791),  # Utah
                (84101, 84199),  # Salt Lake City
                # Las Vegas
                (88901, 89883),  # Nevada
                (89001, 89199),  # Las Vegas metro
                # Albuquerque
                (87001, 88441),  # New Mexico
                (87101, 87199),  # Albuquerque
            ],
            
            # Pacific - America/Los_Angeles
            "America/Los_Angeles": [
                # Los Angeles
                (90001, 91609),  # Los Angeles County
                (90001, 90099),  # Los Angeles city
                # San Francisco
                (94002, 96130),  # Northern CA
                (94102, 94199),  # San Francisco
                # Seattle
                (98001, 99403),  # Washington
                (98101, 98199),  # Seattle
                # Portland
                (97001, 97920),  # Oregon
                (97201, 97299),  # Portland
                # San Diego
                (91901, 92199),  # San Diego area
            ],
            
            # Arizona - America/Phoenix
            "America/Phoenix": [
                (85001, 86556),  # Arizona statewide
                (85001, 85099),  # Phoenix metro
                (85201, 85299),  # Mesa/Chandler
                (85301, 85395),  # Glendale/Peoria
                (85601, 85747),  # Tucson area
            ],
            
            # Idaho - America/Boise
            "America/Boise": [
                (83201, 83876),  # Idaho statewide
                (83605, 83799),  # Boise metro
                (83201, 83299),  # Pocatello/Idaho Falls
                (83401, 83499),  # Eastern Idaho
            ],
            
            # Alaska - America/Anchorage
            "America/Anchorage": [
                (99501, 99950),  # Alaska statewide
                (99501, 99599),  # Anchorage area
                (99611, 99695),  # Southern Alaska
                (99701, 99799),  # Fairbanks area
            ],
            
            # Hawaii - America/Honolulu
            "America/Honolulu": [
                (96701, 96898),  # Hawaii statewide
                (96801, 96899),  # Honolulu/Oahu
                (96701, 96797),  # Other islands
            ],
            
            # Michigan - America/Detroit
            "America/Detroit": [
                (48021, 49971),  # Michigan statewide
                (48021, 48375),  # Detroit metro
                (48201, 48288),  # Detroit city
                (48501, 48599),  # Flint area
                (48801, 48899),  # Lansing area
            ],
            
            # Indiana - America/Indiana/Indianapolis
            "America/Indiana/Indianapolis": [
                (46032, 47997),  # Indiana statewide
                (46032, 46298),  # Indianapolis metro
                (46601, 46699),  # South Bend
                (47701, 47799),  # Evansville
            ],
            # In your us_zip_ranges dictionary, add proper Alaska ranges:
            "America/Juneau": [
                (99801, 99899),  # Juneau area
                (99801, 99824),  # Juneau city
            ],
            "America/Anchorage": [
                (99501, 99999),  # Alaska statewide (most populated areas)
                (99501, 99599),  # Anchorage area
                (99611, 99695),  # Southern Alaska
            ],
            "America/Nome": [
                (99762, 99762),  # Nome
                (99720, 99790),  # Western Alaska
            ],
            "America/Adak": [
                (99546, 99546),  # Adak
            ],
            "America/Sitka": [
                (99835, 99835),  # Sitka
            ],
        }
        
        # UK postcode areas by specific cities
        uk_postcode_areas = {
            "Europe/London": [
                # London areas
                "E", "EC", "N", "NW", "SE", "SW", "W", "WC",
                # London suburbs
                "BR", "CR", "DA", "EN", "HA", "IG", "KT", "RM", "SM", "TW", "UB", "WD",
            ],
            "Europe/Belfast": [
                "BT1", "BT2", "BT3", "BT4", "BT5", "BT6", "BT7", "BT8", "BT9",  # Belfast
                "BT10", "BT11", "BT12", "BT13", "BT14", "BT15", "BT16", "BT17", # Belfast suburbs
            ],
            "Europe/Jersey": [
                "JE1", "JE2", "JE3", "JE4",  # Jersey
            ],
            "Europe/Guernsey": [
                "GY1", "GY2", "GY3", "GY4", "GY5", "GY6", "GY7", "GY8", "GY9",  # Guernsey
            ],
        }
        
        # More specific Australian postcodes
        australia_postcodes = {
            "Australia/Sydney": [
                (2000, 2019),  # Sydney CBD
                (2021, 2038),  # Eastern suburbs
                (2040, 2059),  # Inner west
                (2060, 2079),  # North shore
                (2080, 2109),  # Northern beaches
                (2110, 2129),  # Western suburbs
            ],
            "Australia/Melbourne": [
                (3000, 3010),  # Melbourne CBD
                (3011, 3079),  # Western suburbs
                (3080, 3159),  # Northern suburbs
                (3160, 3199),  # Southern suburbs
                (3200, 3259),  # South-eastern suburbs
            ],
            "Australia/Brisbane": [
                (4000, 4019),  # Brisbane CBD
                (4020, 4079),  # Northern suburbs
                (4100, 4179),  # Southern suburbs
                (4300, 4359),  # Ipswich/Toowoomba
            ],
            "Australia/Perth": [
                (6000, 6019),  # Perth CBD
                (6020, 6079),  # Northern suburbs
                (6080, 6119),  # Eastern suburbs
                (6120, 6159),  # Southern suburbs
            ],
            "Australia/Adelaide": [
                (5000, 5019),  # Adelaide CBD
                (5020, 5079),  # Western suburbs
                (5080, 5119),  # Northern suburbs
                (5120, 5159),  # Eastern suburbs
                (5160, 5199),  # Southern suburbs
            ],
        }
        
        # More specific Canadian postal codes
        canada_postal_formats = {
            "America/Toronto": {
                "areas": ["M", "L", "N", "K"],
                "cities": ["Toronto", "Mississauga", "Brampton", "Hamilton", "London"]
            },
            "America/Vancouver": {
                "areas": ["V"],
                "cities": ["Vancouver", "Surrey", "Burnaby", "Richmond"]
            },
            "America/Edmonton": {
                "areas": ["T"],
                "cities": ["Edmonton", "Calgary", "Red Deer"]
            },
            "America/Winnipeg": {
                "areas": ["R"],
                "cities": ["Winnipeg", "Brandon"]
            },
            "America/Halifax": {
                "areas": ["B"],
                "cities": ["Halifax", "Dartmouth"]
            },
            "America/Regina": {
                "areas": ["S"],
                "cities": ["Regina", "Saskatoon"]
            },
        }
        
        if country == "United States":
            # Get ZIP range for timezone, or use general US range
            if timezone and timezone in us_zip_ranges:
                zip_ranges = us_zip_ranges[timezone]
                selected_range = random.choice(zip_ranges)
                # Ensure we generate valid ZIP codes within the range
                zip_code = str(random.randint(selected_range[0], selected_range[1]))
                # Pad with leading zeros if needed for smaller ranges
                if len(zip_code) < 5:
                    zip_code = zip_code.zfill(5)
            else:
                # Fallback to general US ZIP
                zip_code = str(random.randint(10001, 99999))
                
        elif country == "United Kingdom":
            # Get postcode area for timezone, or use general UK
            if timezone and timezone in uk_postcode_areas:
                area = random.choice(uk_postcode_areas[timezone])
                # Format: Area + numbers + space + number + two letters
                zip_code = f"{area}{random.randint(1, 99)} {random.randint(1, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            else:
                # General UK postcode
                areas = ["AB", "AL", "B", "BA", "BB", "BD", "BH", "BL", "BN", "BR", "BS", "BT", "CA", "CB", "CF", "CH", "CM", "CO", "CR", "CT", "CV", "CW", "DA", "DD", "DE", "DG", "DH", "DL", "DN", "DT", "DY", "E", "EC", "EH", "EN", "EX", "FK", "FY", "G", "GL", "GU", "HA", "HD", "HG", "HP", "HR", "HS", "HU", "HX", "IG", "IP", "IV", "KA", "KT", "KW", "KY", "L", "LA", "LD", "LE", "LL", "LN", "LS", "LU", "M", "ME", "MK", "ML", "N", "NE", "NG", "NN", "NP", "NR", "NW", "OL", "OX", "PA", "PE", "PH", "PL", "PO", "PR", "RG", "RH", "RM", "S", "SA", "SE", "SG", "SK", "SL", "SM", "SN", "SO", "SP", "SR", "SS", "ST", "SW", "SY", "TA", "TD", "TF", "TN", "TQ", "TR", "TS", "TW", "UB", "W", "WA", "WC", "WD", "WF", "WN", "WR", "WS", "WV", "YO", "ZE"]
                area = random.choice(areas)
                zip_code = f"{area}{random.randint(1, 99)} {random.randint(1, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
                
        elif country == "Australia":
            if timezone and timezone in australia_postcodes:
                postcode_ranges = australia_postcodes[timezone]
                selected_range = random.choice(postcode_ranges)
                zip_code = str(random.randint(selected_range[0], selected_range[1]))
            else:
                zip_code = str(random.randint(2000, 9999))
                
        elif country == "Canada":
            # Canadian postal code: A1A 1A1 format
            if timezone and timezone in canada_postal_formats:
                area_data = canada_postal_formats[timezone]
                forward_sortation_area = random.choice(area_data["areas"])
            else:
                forward_sortation_area = random.choice("ABCEGHJKLMNPRSTVXY")
            
            local_delivery_unit = f"{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0,9)}"
            zip_code = f"{forward_sortation_area}{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} {local_delivery_unit}"
            
        else:
            # Fallback for other countries
            zip_code = str(random.randint(10000, 99999))
        
        return zip_code
        
        
    def add_emergency_information(self, responses, personal_info):
        """Add emergency information section 50% of the time with same user data"""
        if random.random() < 0.5:  # 50% chance
            # Use the same personal information for emergency contact
            full_name = f"{personal_info['first_name']} {personal_info['last_name']}".strip()
            address = personal_info['address']
            phone = personal_info['phone']
            
            # Add the section in the exact format
            responses.append("\"EMERGENCY INFORMATION\"")
            responses.append("emergency_name,emergency_address,emergency_phone")
            responses.append(f'"{full_name}","{address}",{phone}')
        else:
            # Add empty emergency information section
            responses.append("\"EMERGENCY INFORMATION\"")
            responses.append("emergency_name,emergency_address,emergency_phone")
            responses.append(",,")

    def generate_nickname_variations(self, first_name, last_name, gender):
        """Generate nickname with multiple realistic variations using common words"""
        # Common nickname patterns with weights (more common patterns have higher weights)
        nickname_patterns = [
            # Simple name + numbers (most common)
            {"pattern": lambda: f"{first_name.lower()}{random.randint(1, 99)}", "weight": 20},
            {"pattern": lambda: f"{last_name.lower()}{random.randint(1, 99)}", "weight": 22},
            
            # Shortened names
            {"pattern": lambda: f"{first_name[:3].lower()}", "weight": 3},
            {"pattern": lambda: f"{first_name[:4].lower()}", "weight": 2},
            {"pattern": lambda: f"{first_name[:2].lower()}{last_name[:2].lower()}", "weight": 1},
            
            # Name combinations
            {"pattern": lambda: f"{first_name[0].lower()}{last_name.lower()}", "weight": 14},
            {"pattern": lambda: f"{first_name.lower()}-{last_name[0].lower()}", "weight": 10},
            {"pattern": lambda: f"{first_name.lower()}_{last_name.lower()}", "weight": 8},
            
            # Year-based
            {"pattern": lambda: f"{first_name.lower()}{random.randint(24, 90)}", "weight": 8},
            {"pattern": lambda: f"{first_name.lower()}19{random.randint(70, 99)}", "weight": 7},
            
            # NEW: Enhanced common word combinations
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{first_name.lower()}", "weight": 6},
            {"pattern": lambda: f"{first_name.lower()}{random.choice(self.common_words).lower()}", "weight": 6},
            {"pattern": lambda: f"{last_name.lower()}{random.choice(self.common_words).lower()}", "weight": 5},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{last_name.lower()}", "weight": 5},
            
            # NEW: Name + common word + numbers
            {"pattern": lambda: f"{first_name.lower()}{random.choice(self.common_words).lower()}{random.randint(1, 99)}", "weight": 3},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{first_name.lower()}{random.randint(1, 99)}", "weight": 2},
            {"pattern": lambda: f"{last_name.lower()}{random.choice(self.common_words).lower()}{random.randint(1, 99)}", "weight": 2},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{last_name.lower()}{random.randint(1, 99)}", "weight": 2},
            
            # NEW: Common word + name combinations with separators
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}-{first_name.lower()}", "weight": 2},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}_{first_name.lower()}", "weight": 2},
            {"pattern": lambda: f"{first_name.lower()}_{random.choice(self.common_words).lower()}", "weight": 2},
            
            # NEW: Double common word combinations with name elements
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}", "weight": 2},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{random.choice(self.common_words).lower()}{random.randint(1, 99)}", "weight": 2},
            {"pattern": lambda: f"{random.choice(self.common_words).capitalize()}{random.choice(self.common_words).capitalize()}", "weight": 2},
            
            # NEW: Name fragments with common words
            {"pattern": lambda: f"{first_name[:2].lower()}{random.choice(self.common_words).lower()}", "weight": 3},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{last_name[:2].lower()}", "weight": 3},
            {"pattern": lambda: f"{first_name[:3].lower()}{random.choice(self.common_words).lower()}{random.randint(1, 99)}", "weight": 2},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{last_name[:3].lower()}{random.randint(1, 99)}", "weight": 2},
            
            # NEW: Mixed patterns with initials and common words
            {"pattern": lambda: f"{first_name[0].lower()}{random.choice(self.common_words).lower()}{last_name[0].lower()}", "weight": 4},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{first_name[0].lower()}{last_name[0].lower()}", "weight": 3},
            {"pattern": lambda: f"{first_name[0].lower()}{last_name[0].lower()}{random.choice(self.common_words).lower()}", "weight": 3},
            
            # NEW: Common word patterns with numbers only
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{random.randint(1, 999)}", "weight": 6},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{random.randint(10, 99)}{random.choice(self.common_words).lower()}", "weight": 3},
            {"pattern": lambda: f"{random.randint(100, 999)}{random.choice(self.common_words).lower()}", "weight": 3},
            
            # Initial-based
            {"pattern": lambda: f"{first_name[0].lower()}{last_name[0].lower()}{random.randint(10, 999)}", "weight": 3},
            {"pattern": lambda: f"{first_name[0].upper()}{last_name[0].upper()}{random.randint(100, 999)}", "weight": 3},
            {"pattern": lambda: f"{random.choice(self.common_words)[0].upper()}{random.choice(self.common_words)[0].upper()}{random.randint(100, 999)}", "weight": 3},
            
            # Gender-specific (less common)
            {"pattern": lambda: f"Mr{first_name}" if gender == "male" else f"Ms{first_name}", "weight": 3},
            {"pattern": lambda: f"Sir{last_name}" if gender == "male" else f"Lady{last_name}", "weight": 3},
            
            # NEW: Complex mixed patterns
            {"pattern": lambda: f"{first_name[:2].lower()}{last_name[:2].lower()}{random.choice(self.common_words).lower()}", "weight": 5},
            {"pattern": lambda: f"{random.choice(self.common_words).lower()}{first_name[:2].lower()}{last_name[:2].lower()}", "weight": 3},
            {"pattern": lambda: f"{first_name[0].lower()}{random.choice(self.common_words).lower()}{last_name[0].lower()}{random.randint(1, 99)}", "weight": 5},
            {"pattern": lambda: f"{random.randint(1, 99)}{first_name[0].lower()}{random.choice(self.common_words).lower()}{last_name[0].lower()}", "weight": 5},
        ]
        
        # Select pattern using weights
        patterns = [p["pattern"] for p in nickname_patterns]
        weights = [p["weight"] for p in nickname_patterns]
        selected_pattern = random.choices(patterns, weights=weights, k=1)[0]
        
        return selected_pattern()
        
    def generate_ip_and_location(self, country, timezone=""):
        """Generate realistic IP address and location based on country and timezone with population weighting"""
        
        # Define timezone_to_region mapping as local variable
        timezone_to_region = {
            # US - FIXED MAPPINGS
            "America/New_York": "Northeast",
            "America/Chicago": "Central",
            "America/Denver": "Mountain", 
            "America/Los_Angeles": "Pacific",
            "America/Phoenix": "Mountain",
            "America/Anchorage": "Alaska",
            "America/Honolulu": "Hawaii",
            "America/Detroit": "Northeast",
            "America/Boise": "Mountain",
            "America/Juneau": "Alaska",
            "America/Indiana/Indianapolis": "Northeast",
            "America/Nome": "Alaska",
            "America/Adak": "Alaska",
            "America/Sitka": "Alaska",
            
            # Canada
            "America/Toronto": "Eastern Canada",
            "America/Vancouver": "Western Canada",
            "America/Edmonton": "Western Canada", 
            "America/Winnipeg": "Central Canada",
            "America/Halifax": "Eastern Canada",
            "America/Regina": "Central Canada",
            "America/St_Johns": "Eastern Canada",
            "America/Whitehorse": "Northern Canada",
            "America/Iqaluit": "Northern Canada",
            
            # UK
            "Europe/London": "UK",
            "Europe/Belfast": "UK",
            "Europe/Jersey": "UK",
            "Europe/Guernsey": "UK",  
            "Europe/Isle_of_Man": "UK",
            
            # Australia
            "Australia/Sydney": "Eastern Australia",
            "Australia/Brisbane": "Eastern Australia",
            "Australia/Perth": "Western Australia",
            "Australia/Adelaide": "Eastern Australia",
            "Australia/Darwin": "Eastern Australia",
            
            # New Zealand
            "Pacific/Auckland": "Eastern Australia",
        }
        
        ip_ranges = {
            # US Regions - VERIFIED RANGES that actually geolocate correctly
            "Northeast": [
                {"range": (24, 0, 0, 255), "isp": "Comcast"},           # US - Comcast
                {"range": (50, 0, 0, 255), "isp": "Verizon"},           # US - Verizon
                {"range": (63, 0, 0, 255), "isp": "Spectrum"},          # US - Spectrum
                {"range": (68, 0, 0, 255), "isp": "Comcast"},           # US - Comcast
                {"range": (73, 0, 0, 255), "isp": "Comcast"},           # US - Comcast
                {"range": (96, 0, 0, 255), "isp": "Optimum"},           # US - Optimum
                {"range": (107, 0, 0, 255), "isp": "Verizon"},          # US - Verizon
                {"range": (108, 0, 0, 255), "isp": "AT&T"},             # US - AT&T
                {"range": (162, 0, 0, 255), "isp": "Comcast"},          # US - Comcast
                {"range": (174, 0, 0, 255), "isp": "Verizon"}           # US - Verizon
            ],
            "Central": [
                {"range": (47, 148, 0, 255), "isp": "AT&T Chicago"},    # US - AT&T
                {"range": (65, 128, 0, 255), "isp": "Comcast Chicago"}, # US - Comcast
                {"range": (71, 203, 0, 255), "isp": "Comcast Chicago"}, # US - Comcast
                {"range": (96, 80, 0, 255), "isp": "Comcast Chicago"},  # US - Comcast
                {"range": (104, 130, 0, 255), "isp": "AT&T Chicago"},   # US - AT&T
                {"range": (107, 130, 0, 255), "isp": "Spectrum"},       # US - Spectrum
                {"range": (173, 0, 0, 255), "isp": "Comcast"},          # US - Comcast
                {"range": (184, 0, 0, 255), "isp": "AT&T"},             # US - AT&T
                {"range": (192, 0, 0, 255), "isp": "Spectrum"}          # US - Spectrum
            ],
            "Mountain": [
                {"range": (50, 218, 0, 255), "isp": "CenturyLink"},     # US - CenturyLink
                {"range": (96, 90, 0, 255), "isp": "Comcast Denver"},   # US - Comcast
                {"range": (97, 117, 0, 255), "isp": "Cable One"},       # US - Cable One
                {"range": (104, 129, 0, 255), "isp": "Sparklight"},     # US - Sparklight
                {"range": (107, 178, 0, 255), "isp": "CenturyLink"},    # US - CenturyLink
                {"range": (107, 191, 0, 255), "isp": "CenturyLink"},    # US - CenturyLink
                {"range": (136, 0, 0, 255), "isp": "Comcast"},          # US - Comcast
                {"range": (162, 0, 0, 255), "isp": "Comcast"}           # US - Comcast
            ],
            "Pacific": [
                {"range": (64, 0, 0, 255), "isp": "Comcast California"},# US - Comcast
                {"range": (96, 0, 0, 255), "isp": "Frontier"},          # US - Frontier
                {"range": (104, 0, 0, 255), "isp": "Google Fiber"},     # US - Google
                {"range": (107, 0, 0, 255), "isp": "Frontier"},         # US - Frontier
                {"range": (136, 0, 0, 255), "isp": "Comcast"},          # US - Comcast
                {"range": (162, 0, 0, 255), "isp": "Comcast"},          # US - Comcast
                {"range": (198, 0, 0, 255), "isp": "AT&T"},             # US - AT&T
                {"range": (208, 0, 0, 255), "isp": "Comcast"}           # US - Comcast
            ],
            "Alaska": [
                {"range": (63, 128, 0, 255), "isp": "AT&T Alaska"},     # US - AT&T
                {"range": (72, 128, 0, 255), "isp": "GCI"},             # US - GCI
                {"range": (137, 128, 0, 255), "isp": "ACS"},            # US - ACS
                {"range": (209, 128, 0, 255), "isp": "MTA"}             # US - MTA
            ],
            "Hawaii": [
                {"range": (66, 128, 0, 255), "isp": "Hawaiian Telcom"}, # US - Hawaiian Telcom
                {"range": (97, 128, 0, 255), "isp": "Spectrum"},        # US - Spectrum
                {"range": (107, 128, 0, 255), "isp": "Hawaiian Telcom"},# US - Hawaiian Telcom
                {"range": (184, 128, 0, 255), "isp": "Hawaiian Telcom"} # US - Hawaiian Telcom
            ],
            
            # Canada - ACTUAL CANADIAN IP RANGES
            "Eastern Canada": [
                {"range": (24, 128, 0, 255), "isp": "Rogers"},          # CA - Rogers
                {"range": (50, 128, 0, 255), "isp": "Bell Canada"},     # CA - Bell
                {"range": (70, 128, 0, 255), "isp": "Telus"},           # CA - Telus
                {"range": (99, 128, 0, 255), "isp": "Bell Canada"},     # CA - Bell
                {"range": (104, 128, 0, 255), "isp": "Rogers"},         # CA - Rogers
                {"range": (107, 128, 0, 255), "isp": "Telus"},          # CA - Telus
                {"range": (142, 128, 0, 255), "isp": "Bell Canada"},    # CA - Bell
                {"range": (162, 128, 0, 255), "isp": "Rogers"}          # CA - Rogers
            ],
            "Western Canada": [
                {"range": (96, 128, 0, 255), "isp": "Shaw"},            # CA - Shaw
                {"range": (97, 128, 0, 255), "isp": "Telus"},           # CA - Telus
                {"range": (104, 128, 0, 255), "isp": "Shaw"},           # CA - Shaw
                {"range": (107, 128, 0, 255), "isp": "Telus"},          # CA - Telus
                {"range": (142, 128, 0, 255), "isp": "Shaw"},           # CA - Shaw
                {"range": (162, 128, 0, 255), "isp": "Telus"},          # CA - Telus
                {"range": (184, 128, 0, 255), "isp": "Shaw"}            # CA - Shaw
            ],
            "Central Canada": [
                {"range": (64, 128, 0, 255), "isp": "SaskTel"},         # CA - SaskTel
                {"range": (96, 128, 0, 255), "isp": "MTS"},             # CA - MTS
                {"range": (104, 128, 0, 255), "isp": "SaskTel"},        # CA - SaskTel
                {"range": (142, 128, 0, 255), "isp": "MTS"},            # CA - MTS
                {"range": (162, 128, 0, 255), "isp": "SaskTel"},        # CA - SaskTel
                {"range": (198, 128, 0, 255), "isp": "Access Comm"}     # CA - Access
            ],
            "Northern Canada": [
                {"range": (24, 128, 0, 255), "isp": "Northwestel"},     # CA - Northwestel
                {"range": (70, 128, 0, 255), "isp": "SSI Micro"},       # CA - SSI Micro
                {"range": (96, 128, 0, 255), "isp": "Northwestel"},     # CA - Northwestel
                {"range": (142, 128, 0, 255), "isp": "SSI Micro"}       # CA - SSI Micro
            ],
            
            # UK - ACTUAL UK IP RANGES
            "UK": [             # UK - BT
                {"range": (37, 128, 0, 255), "isp": "Sky Broadband"},   # UK - Sky
                {"range": (51, 128, 0, 255), "isp": "BT"},              # UK - BT
                {"range": (62, 128, 0, 255), "isp": "Sky Broadband"},   # UK - Sky
                {"range": (77, 128, 0, 255), "isp": "Virgin Media"},    # UK - Virgin
                {"range": (79, 128, 0, 255), "isp": "TalkTalk"},        # UK - TalkTalk
                {"range": (81, 128, 0, 255), "isp": "Vodafone UK"},     # UK - Vodafone
                {"range": (86, 128, 0, 255), "isp": "Plusnet"},         # UK - Plusnet
                {"range": (87, 128, 0, 255), "isp": "EE"},              # UK - EE
                {"range": (88, 128, 0, 255), "isp": "BT"},              # UK - BT
                {"range": (89, 128, 0, 255), "isp": "Sky Broadband"},   # UK - Sky
                {"range": (91, 128, 0, 255), "isp": "Virgin Media"},    # UK - Virgin
                {"range": (92, 128, 0, 255), "isp": "TalkTalk"},        # UK - TalkTalk
                {"range": (94, 128, 0, 255), "isp": "BT"},              # UK - BT
                {"range": (95, 128, 0, 255), "isp": "Virgin Media"}     # UK - Virgin
            ],
            
            # Australia - ACTUAL AUSTRALIAN IP RANGES
            "Eastern Australia": [
                {"range": (101, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (103, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (110, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (112, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (113, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (114, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (115, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (116, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (117, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (118, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (119, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (120, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (121, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (122, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (123, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (124, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (125, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (126, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (139, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (144, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (150, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (153, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (155, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (158, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (175, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (180, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (182, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (203, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra          # AU - TPG
            ],
            "Western Australia": [
                {"range": (101, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (103, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (110, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (118, 128, 0, 255), "isp": "iiNet"},          # AU - iiNet
                {"range": (139, 128, 0, 255), "isp": "Vodafone AU"},    # AU - Vodafone
                {"range": (144, 128, 0, 255), "isp": "iiNet"},          # AU - iiNet
                {"range": (150, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (153, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (155, 128, 0, 255), "isp": "TPG"},            # AU - TPG
                {"range": (158, 128, 0, 255), "isp": "iiNet"},          # AU - iiNet
                {"range": (175, 128, 0, 255), "isp": "Vodafone AU"},    # AU - Vodafone
                {"range": (180, 128, 0, 255), "isp": "Telstra"},        # AU - Telstra
                {"range": (182, 128, 0, 255), "isp": "Optus"},          # AU - Optus
                {"range": (203, 128, 0, 255), "isp": "Dodo"},           # AU - Dodo        # AU - Telstra
            ],
            
            # New Zealand - ACTUAL NZ IP RANGES
            "Eastern Australia": [  # Note: This key is reused but IPs are NZ-specific
                {"range": (49, 128, 0, 255), "isp": "Spark NZ"},        # NZ - Spark
                {"range": (101, 128, 0, 255), "isp": "Vodafone NZ"},    # NZ - Vodafone
                {"range": (103, 128, 0, 255), "isp": "2degrees"},       # NZ - 2degrees
                {"range": (118, 128, 0, 255), "isp": "Spark NZ"},       # NZ - Spark
                {"range": (119, 128, 0, 255), "isp": "Vodafone NZ"},    # NZ - Vodafone
                {"range": (121, 128, 0, 255), "isp": "2degrees"},       # NZ - 2degrees
                {"range": (122, 128, 0, 255), "isp": "Spark NZ"},       # NZ - Spark
                {"range": (123, 128, 0, 255), "isp": "Vodafone NZ"},    # NZ - Vodafone
                {"range": (125, 128, 0, 255), "isp": "2degrees"},       # NZ - 2degrees
                {"range": (202, 128, 0, 255), "isp": "Spark NZ"},       # NZ - Spark
                {"range": (203, 128, 0, 255), "isp": "Vodafone NZ"},    # NZ - Vodafone
                {"range": (210, 128, 0, 255), "isp": "2degrees"},       # NZ - 2degrees
                {"range": (218, 128, 0, 255), "isp": "Spark NZ"},       # NZ - Spark
                {"range": (219, 128, 0, 255), "isp": "Vodafone NZ"},    # NZ - Vodafone
                {"range": (220, 128, 0, 255), "isp": "2degrees"}        # NZ - 2degrees
            ]
        }
        
        # Population-weighted cities by timezone
        timezone_to_weighted_cities = {
            # US Timezones - weighted by metro population
            "America/New_York": [
                {"city": "New York", "weight": 350}, {"city": "Philadelphia", "weight": 120}, 
                {"city": "Boston", "weight": 90}, {"city": "Washington", "weight": 80},
                {"city": "Atlanta", "weight": 70}, {"city": "Miami", "weight": 65},
                {"city": "Baltimore", "weight": 45}, {"city": "Charlotte", "weight": 40},
                {"city": "Orlando", "weight": 35}, {"city": "Tampa", "weight": 30},
                {"city": "Jacksonville", "weight": 40}
            ],
            "America/Chicago": [
                {"city": "Chicago", "weight": 200}, {"city": "Dallas", "weight": 120},
                {"city": "Houston", "weight": 110}, {"city": "Detroit", "weight": 70},
                {"city": "Minneapolis", "weight": 60}, {"city": "St. Louis", "weight": 45},
                {"city": "Kansas City", "weight": 40}, {"city": "Indianapolis", "weight": 35},
                {"city": "Milwaukee", "weight": 30}, {"city": "Columbus", "weight": 25}
            ],
            "America/Denver": [
                {"city": "Denver", "weight": 80}, {"city": "Phoenix", "weight": 70},
                {"city": "Las Vegas", "weight": 45}, {"city": "Salt Lake City", "weight": 35},
                {"city": "Albuquerque", "weight": 25}, {"city": "Boise", "weight": 15},
                {"city": "Cheyenne", "weight": 5}, {"city": "El Paso", "weight": 20}
            ],
            "America/Los_Angeles": [
                {"city": "Los Angeles", "weight": 300}, {"city": "San Francisco", "weight": 120},
                {"city": "Seattle", "weight": 80}, {"city": "San Diego", "weight": 70},
                {"city": "Portland", "weight": 45}, {"city": "Sacramento", "weight": 40},
                {"city": "San Jose", "weight": 35}, {"city": "Oakland", "weight": 25}
            ],
            "America/Phoenix": [
                {"city": "Phoenix", "weight": 90}, {"city": "Tucson", "weight": 25},
                {"city": "Mesa", "weight": 20}, {"city": "Scottsdale", "weight": 15},
                {"city": "Glendale", "weight": 10}, {"city": "Chandler", "weight": 10},
                {"city": "Gilbert", "weight": 10}, {"city": "Tempe", "weight": 8}
            ],
            "America/Boise": [
                {"city": "Boise", "weight": 50}, {"city": "Salt Lake City", "weight": 25},
                {"city": "Denver", "weight": 15}, {"city": "Las Vegas", "weight": 10}
            ],
            "America/Detroit": [
                {"city": "Detroit", "weight": 80}, {"city": "Cleveland", "weight": 35},
                {"city": "Columbus", "weight": 30}, {"city": "Indianapolis", "weight": 25}
            ],
            "America/Anchorage": [
                {"city": "Anchorage", "weight": 80}, {"city": "Fairbanks", "weight": 12},
                {"city": "Juneau", "weight": 5}, {"city": "Wasilla", "weight": 3}
            ],
            "America/Honolulu": [
                {"city": "Honolulu", "weight": 25}, {"city": "Hilo", "weight": 8},
                {"city": "Kailua", "weight": 4}, {"city": "Kaneohe", "weight": 3}
            ],
            "America/Indiana/Indianapolis": [
                {"city": "Indianapolis", "weight": 70}, {"city": "Fort Wayne", "weight": 15},
                {"city": "Evansville", "weight": 10}, {"city": "South Bend", "weight": 5}
            ],
            "America/Juneau": [
                {"city": "Juneau", "weight": 60}, {"city": "Ketchikan", "weight": 15},
                {"city": "Sitka", "weight": 10}, {"city": "Anchorage", "weight": 15}
            ],

            # United Kingdom Timezones
            "Europe/London": [
                {"city": "London", "weight": 400}, {"city": "Birmingham", "weight": 80},
                {"city": "Manchester", "weight": 70}, {"city": "Glasgow", "weight": 45},
                {"city": "Liverpool", "weight": 35}, {"city": "Leeds", "weight": 30},
                {"city": "Sheffield", "weight": 25}, {"city": "Edinburgh", "weight": 25},
                {"city": "Bristol", "weight": 20}, {"city": "Cardiff", "weight": 15}
            ],
            "Europe/Belfast": [
                {"city": "Belfast", "weight": 70}, {"city": "Derry", "weight": 15},
                {"city": "Lisburn", "weight": 10}, {"city": "Newry", "weight": 5}
            ],
            "Europe/Jersey": [
                {"city": "Saint Helier", "weight": 80}, {"city": "Saint Saviour", "weight": 10},
                {"city": "Saint Clement", "weight": 5}, {"city": "Grouville", "weight": 5}
            ],
            "Europe/Guernsey": [
                {"city": "Saint Peter Port", "weight": 75}, {"city": "Saint Sampson", "weight": 15},
                {"city": "Vale", "weight": 10}
            ],
            "Europe/Isle_of_Man": [
                {"city": "Douglas", "weight": 70}, {"city": "Ramsey", "weight": 15},
                {"city": "Peel", "weight": 10}, {"city": "Castletown", "weight": 5}
            ],

            # Canada Timezones
            "America/Toronto": [
                {"city": "Toronto", "weight": 300}, {"city": "Montreal", "weight": 120},
                {"city": "Ottawa", "weight": 70}, {"city": "Hamilton", "weight": 45},
                {"city": "London", "weight": 30}, {"city": "Quebec City", "weight": 25},
                {"city": "Windsor", "weight": 20}, {"city": "Kitchener", "weight": 18}
            ],
            "America/Vancouver": [
                {"city": "Vancouver", "weight": 150}, {"city": "Surrey", "weight": 60},
                {"city": "Burnaby", "weight": 45}, {"city": "Richmond", "weight": 35},
                {"city": "Victoria", "weight": 25}, {"city": "Coquitlam", "weight": 15},
                {"city": "Kelowna", "weight": 10}, {"city": "Abbotsford", "weight": 10}
            ],
            "America/Edmonton": [
                {"city": "Edmonton", "weight": 100}, {"city": "Calgary", "weight": 80},
                {"city": "Red Deer", "weight": 15}, {"city": "Lethbridge", "weight": 10},
                {"city": "Fort McMurray", "weight": 8}, {"city": "Medicine Hat", "weight": 7}
            ],
            "America/Winnipeg": [
                {"city": "Winnipeg", "weight": 120}, {"city": "Brandon", "weight": 20},
                {"city": "Thompson", "weight": 8}, {"city": "Portage la Prairie", "weight": 5}
            ],
            "America/Halifax": [
                {"city": "Halifax", "weight": 80}, {"city": "Dartmouth", "weight": 25},
                {"city": "Sydney", "weight": 12}, {"city": "Truro", "weight": 8}
            ],
            "America/St_Johns": [
                {"city": "St. John's", "weight": 60}, {"city": "Mount Pearl", "weight": 15},
                {"city": "Corner Brook", "weight": 10}, {"city": "Conception Bay South", "weight": 8}
            ],
            "America/Regina": [
                {"city": "Regina", "weight": 70}, {"city": "Saskatoon", "weight": 60},
                {"city": "Prince Albert", "weight": 12}, {"city": "Moose Jaw", "weight": 10}
            ],
            "America/Whitehorse": [
                {"city": "Whitehorse", "weight": 85}, {"city": "Dawson City", "weight": 8},
                {"city": "Watson Lake", "weight": 4}, {"city": "Haines Junction", "weight": 3}
            ],
            "America/Iqaluit": [
                {"city": "Iqaluit", "weight": 80}, {"city": "Arviat", "weight": 8},
                {"city": "Rankin Inlet", "weight": 7}, {"city": "Baker Lake", "weight": 5}
            ],

            # Australia Timezones
            "Australia/Sydney": [
                {"city": "Sydney", "weight": 300}, {"city": "Melbourne", "weight": 250},
                {"city": "Brisbane", "weight": 150}, {"city": "Perth", "weight": 120},
                {"city": "Adelaide", "weight": 80}, {"city": "Gold Coast", "weight": 40},
                {"city": "Newcastle", "weight": 35}, {"city": "Canberra", "weight": 25},
                {"city": "Wollongong", "weight": 20}, {"city": "Sunshine Coast", "weight": 15}
            ],
            "Australia/Melbourne": [
                {"city": "Melbourne", "weight": 350}, {"city": "Geelong", "weight": 45},
                {"city": "Ballarat", "weight": 25}, {"city": "Bendigo", "weight": 20},
                {"city": "Melton", "weight": 15}, {"city": "Mildura", "weight": 10}
            ],
            "Australia/Brisbane": [
                {"city": "Brisbane", "weight": 200}, {"city": "Gold Coast", "weight": 80},
                {"city": "Sunshine Coast", "weight": 45}, {"city": "Townsville", "weight": 35},
                {"city": "Cairns", "weight": 25}, {"city": "Toowoomba", "weight": 20}
            ],
            "Australia/Perth": [
                {"city": "Perth", "weight": 150}, {"city": "Rockingham", "weight": 35},
                {"city": "Mandurah", "weight": 25}, {"city": "Bunbury", "weight": 15},
                {"city": "Geraldton", "weight": 8}, {"city": "Kalgoorlie", "weight": 7}
            ],
            "Australia/Adelaide": [
                {"city": "Adelaide", "weight": 100}, {"city": "Mount Gambier", "weight": 15},
                {"city": "Whyalla", "weight": 10}, {"city": "Port Lincoln", "weight": 8},
                {"city": "Port Pirie", "weight": 6}, {"city": "Port Augusta", "weight": 5}
            ],
            "Australia/Darwin": [
                {"city": "Darwin", "weight": 70}, {"city": "Palmerston", "weight": 15},
                {"city": "Alice Springs", "weight": 12}, {"city": "Katherine", "weight": 8}
            ],
            "Australia/Hobart": [
                {"city": "Hobart", "weight": 60}, {"city": "Launceston", "weight": 25},
                {"city": "Devonport", "weight": 12}, {"city": "Burnie", "weight": 8}
            ],
            "Australia/Lord_Howe": [
                {"city": "Lord Howe Island", "weight": 95}, {"city": "Sydney", "weight": 5}
            ],

            # New Zealand Timezones
            "Pacific/Auckland": [
                {"city": "Auckland", "weight": 200}, {"city": "Wellington", "weight": 120},
                {"city": "Christchurch", "weight": 100}, {"city": "Hamilton", "weight": 45},
                {"city": "Tauranga", "weight": 35}, {"city": "Dunedin", "weight": 25},
                {"city": "Palmerston North", "weight": 20}, {"city": "Napier", "weight": 15}
            ],
            "Pacific/Chatham": [
                {"city": "Chatham Islands", "weight": 85}, {"city": "Wellington", "weight": 15}
            ],
            "Pacific/Wellington": [
                {"city": "Wellington", "weight": 150}, {"city": "Lower Hutt", "weight": 45},
                {"city": "Upper Hutt", "weight": 25}, {"city": "Porirua", "weight": 20},
                {"city": "Palmerston North", "weight": 18}, {"city": "Kapiti Coast", "weight": 12}
            ],
            "Pacific/Christchurch": [
                {"city": "Christchurch", "weight": 120}, {"city": "Timaru", "weight": 20},
                {"city": "Ashburton", "weight": 12}, {"city": "Oamaru", "weight": 8}
            ],
            "Pacific/Hamilton": [
                {"city": "Hamilton", "weight": 80}, {"city": "Cambridge", "weight": 15},
                {"city": "Te Awamutu", "weight": 10}, {"city": "Matamata", "weight": 5}
            ],
            "Pacific/Dunedin": [
                {"city": "Dunedin", "weight": 70}, {"city": "Mosgiel", "weight": 15},
                {"city": "Port Chalmers", "weight": 8}, {"city": "Oamaru", "weight": 7}
            ],

            # Ireland Timezones
            "Europe/Dublin": [
                {"city": "Dublin", "weight": 200}, {"city": "Cork", "weight": 45},
                {"city": "Limerick", "weight": 35}, {"city": "Galway", "weight": 30},
                {"city": "Waterford", "weight": 20}, {"city": "Drogheda", "weight": 15},
                {"city": "Dundalk", "weight": 12}, {"city": "Swords", "weight": 10}
            ],
            "Europe/Cork": [
                {"city": "Cork", "weight": 120}, {"city": "Cobh", "weight": 15},
                {"city": "Midleton", "weight": 12}, {"city": "Youghal", "weight": 8}
            ],
            "Europe/Galway": [
                {"city": "Galway", "weight": 80}, {"city": "Tuam", "weight": 12},
                {"city": "Ballinasloe", "weight": 10}, {"city": "Loughrea", "weight": 8}
            ],
            "Europe/Limerick": [
                {"city": "Limerick", "weight": 70}, {"city": "Ennis", "weight": 15},
                {"city": "Newcastle West", "weight": 10}, {"city": "Killarney", "weight": 8}
            ],
            "Europe/Waterford": [
                {"city": "Waterford", "weight": 60}, {"city": "Tramore", "weight": 12},
                {"city": "Dungarvan", "weight": 10}, {"city": "Kilkenny", "weight": 8}
            ]
        }
        
        # CRITICAL FIX: If no timezone provided, generate one first to ensure consistency
        if not timezone:
            timezone_variations = {
                "United States": [
                    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
                    "America/Phoenix", "America/Anchorage", "America/Honolulu", "America/Detroit",
                    "America/Indiana/Indianapolis", "America/Boise", "America/Juneau"
                ],
                "United Kingdom": ["Europe/London", "Europe/Belfast"],
                "Canada": ["America/Toronto", "America/Vancouver", "America/Edmonton"],
                "Australia": ["Australia/Sydney", "Australia/Melbourne", "Australia/Perth"],
            }
            country_timezones = timezone_variations.get(country, ["UTC"])
            timezone = random.choice(country_timezones)
        
        # Get weighted cities for the timezone
        if timezone in timezone_to_weighted_cities:
            weighted_cities = timezone_to_weighted_cities[timezone]
            cities = [wc["city"] for wc in weighted_cities]
            weights = [wc["weight"] for wc in weighted_cities]
            location_city = random.choices(cities, weights=weights, k=1)[0]
        else:
            # Fallback to major cities in the country
            fallback_cities = {
                "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
                "United Kingdom": ["London", "Birmingham", "Manchester"],
                "Canada": ["Toronto", "Vancouver", "Montreal"],
                "Australia": ["Sydney", "Melbourne", "Brisbane"]
            }
            location_city = random.choice(fallback_cities.get(country, ["Unknown"]))
        
        # Get IP range based on timezone region
        region = timezone_to_region.get(timezone)
        if not region or region not in ip_ranges:
            # Fallback based on country
            country_fallbacks = {
                "United States": "Northeast",
                "United Kingdom": "UK", 
                "Canada": "Eastern Canada",
                "Australia": "Eastern Australia",
            }
            region = country_fallbacks.get(country, "Northeast")
        
        country_ranges = ip_ranges.get(region, ip_ranges["Northeast"])
        
        # Select a random IP range and generate IP
        ip_range = random.choice(country_ranges)
        first_octet = ip_range["range"][0]
        second_octet = random.randint(ip_range["range"][1], ip_range["range"][3])
        third_octet = random.randint(0, 255)
        fourth_octet = random.randint(1, 254)
        
        ip_address = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
        location = f"{country}, {location_city}"
        
        return ip_address, location

    def validate_city_timezone_alignment(self, city, timezone):
        """Validate that a city actually uses the specified timezone"""
        city_timezone_exceptions = {
            # Cities that might be in unexpected timezones
            "Houston": "America/Chicago",  # Central Time
            "Dallas": "America/Chicago",   # Central Time  
            "Chicago": "America/Chicago",  # Central Time
            "Detroit": "America/Detroit",  # Eastern Time
            "Indianapolis": "America/Indiana/Indianapolis",  # Eastern Time
            "Phoenix": "America/Phoenix",  # Mountain Time (no DST)
            "Boise": "America/Boise",      # Mountain Time
        }
        
        # If city has a specific timezone requirement, use it
        if city in city_timezone_exceptions:
            return city_timezone_exceptions[city]
        
        return timezone  # Default to the original timezone

    def add_ip_addresses_section(self, responses, country, timezone=""):
        """Add IP addresses and locations section to responses"""
        responses.append("\"IP ADDRESSES AND LOCATIONS\"")
        
        # Generate 1-3 IP addresses
        num_ips = random.choices([1, 2, 3], weights=[70, 25, 5], k=1)[0]
        
        ip_lines = []
        for _ in range(num_ips):
            ip_address, location = self.generate_ip_and_location(country, timezone)
            ip_lines.append(f"{ip_address},\"{location}\"")
        
        responses.extend(ip_lines)

def generate_questionnaire(json_file_path):
    """
    Generate a questionnaire based on JSON data with percentage chances
    """
    try:
        #print(f"Loading JSON file: {json_file_path}")
        
        # Check if file exists
        if not os.path.exists(json_file_path):
            print(f"ERROR: File {json_file_path} not found!")
            print("Please make sure qs2.json is in the same folder as this script")
            return
        
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        #print(f"Successfully loaded JSON with {len(data)} questions")
        
        # Initialize data generator
        data_gen = DataGenerator()
        
        # Generate responses for each question
        responses = []
        responses.append("\"DESCRIPTION AND QUESTIONNAIRE\"")
        
        # Store answers to reuse for duplicate questions
        answer_cache = {}
        
        # Define the exact order and structure from your original example
        question_order = [
            "therapy_reason",
            "therapy_type", 
            "country",
            "gender_identity",
            "age",
            "sexual_orientation",
            "relationship_status",
            "religion_importance",
            "religion_identity",
            "christian_therapy",  # ← ADD THIS LINE
            "spiritual",
            "therapy_before",
            "therapy_motivation",
            "therapist_expectations",
            "communication_style",
            "session_style",
            "therapist_formality",
            "eating_habits",
            "sleep_habits",
            "physical_health",
            "medication",
            "alcohol_use",
            "intimacy_issues",
            "chronic_pain",
            "anxiety_experience",
            "employment",
            "physical_health",  # Duplicate
            "eating_habits",    # Duplicate
            "feeling_down",     # PHQ-9
            "depression_experience",
            "little_interest",  # PHQ-9
            "movement_changes", # PHQ-9
            "feeling_down",     # PHQ-9 duplicate
            "sleep_problems",   # PHQ-9
            "low_energy",       # PHQ-9
            "appetite_changes", # PHQ-9
            "self_esteem",      # PHQ-9
            "concentration",    # PHQ-9
            "suicidal_thoughts",# PHQ-9
            "difficulty_functioning", # PHQ-9
            "employment",       # Duplicate
            "intimacy_issues",  # Duplicate
            "alcohol_use",      # Duplicate
            "suicidal_thoughts_timing",
            "anxiety_experience", # Duplicate
            "medication",       # Duplicate
            "chronic_pain",     # Duplicate
            "sleep_habits",     # Duplicate
            "therapy_resources",
            "communication_preference"
        ]
        
        # Track the position of the religion question for later insertion
        religion_position = None
        
        # Process questions in exact order
        for i, question_key in enumerate(question_order):
            # Skip christian_therapy if religion is not Christianity
            if question_key == "christian_therapy":
                religion_identity = answer_cache.get("religion_identity", "")
                if religion_identity == "" or religion_identity is None:
                    continue
                elif religion_identity.lower() != "christianity":
                    continue
            
            if question_key in data:
                question_data = data[question_key]
                
                if "question" in question_data and "options" in question_data:
                    question_text = question_data["question"]
                    
                    # Use cached answer if this question was already answered
                    if question_key in answer_cache:
                        selected_answer = answer_cache[question_key]
                    else:
                        selected_answer = weighted_choice(question_data["options"])
                        # Special handling for age question - pick random number from range
                        if question_key == "age" and "-" in selected_answer:
                            selected_answer = get_age_from_range(selected_answer)
                        # Cache the answer for future use
                        answer_cache[question_key] = selected_answer
                    
                    # Format the response line
                    if question_text.endswith('?'):
                        response_line = f'"{question_text} {selected_answer}"'
                    else:
                        response_line = f'"{question_text}{selected_answer}"'
                    
                    responses.append(response_line)
                    
                    # Track position of religion identity question
                    if question_key == "religion_identity":
                        religion_position = len(responses) - 1  # Current position in responses list
                else:
                    print(f"  - SKIPPING: Missing 'question' or 'options' for {question_key}")
            else:
                print(f"  - WARNING: Question key '{question_key}' not found in JSON data")
        
        # Generate personal information using cached gender, age, and country
        gender_identity = answer_cache.get("gender_identity", "Male")
        age = answer_cache.get("age", "30")
        country = answer_cache.get("country", "United States")
            
        personal_info = data_gen.generate_personal_info(gender_identity, age, country)
        personal_info_line = f'"{personal_info["email"]}","{personal_info["first_name"]}","{personal_info["middle_name"]}","{personal_info["last_name"]}","{personal_info["nick_name"]}","{personal_info["gender"]}","{personal_info["age"]}","{personal_info["country"]}",{personal_info["state"] or ""},{personal_info["city"] or ""},{personal_info["address"] or ""},{personal_info["zip"] or ""},{personal_info["phone"] or ""},{personal_info["mobile"] or ""},{personal_info["phone_country_code"] or ""},"{personal_info["timezone"]}",{personal_info["customer_key"] or ""}'
        
        # Add the additional sections
        responses.append("")
        data_gen.add_emergency_information(responses, personal_info)
        responses.append("")
        responses.append("\"PERSONAL INFORMATION\"")
        responses.append("email,first_name,middle_name,last_name,nick_name,gender,age,country,state,city,address,zip,phone,mobile,phone_country_code,timezone,customer_key")
        responses.append(personal_info_line)
        responses.append("")
        data_gen.add_ip_addresses_section(responses, country, personal_info.get("timezone", ""))
        responses.append("")
        responses.append("\"MISCELLANEOUS DATA\"")
        responses.append('"Account id","Internal id used to identify account data"')
        responses.append('"Client id","Internal id used to identify client data"')
        responses.append('"User Agent","Identifies the member\'s browser and operating system"')
        responses.append('"Customer key","Alpha-numeric value used in executing billing operations"')
        
        # Generate filename and save in same folder as script
        filename = generate_random_file_name() + ".csv"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'items4/' + filename)
        
        # Save to CSV - write each response as a single line without extra quotes
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            for response in responses:
                csvfile.write(response + '\n')
        
        print(f"\n✅ SUCCESS: Questionnaire saved as: {file_path}")
        
        # Show final output
        #print("\n📋 Generated responses:")
        #for response in responses:
            #print(response)
            
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON format in {json_file_path}")
        print(f"Error details: {e}")
        print("\nPlease check that your JSON file is properly formatted")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"Error type: {type(e).__name__}")

# Run the script
if __name__ == "__main__":
    json_file_path = "qs2.json"
    print("🚀 Starting questionnaire generator...")
    print("=" * 50)
    n = 100000
    for i in range(n):
        print(f"\n📝 Generating questionnaire {i+1} of {n}...")
        generate_questionnaire(json_file_path)
    
    print("=" * 50)
    print("Script finished! Press Enter to close...")
    input()  # This will wait for user input before closing