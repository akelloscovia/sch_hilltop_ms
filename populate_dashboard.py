#!/usr/bin/env python3
"""
Fill in all dashboard content for the school website
"""
import requests
import json

BASE_URL = "http://localhost:5010/api/v1"

# Home Page Content
home_data = {
    "hero_title": "Hilltop Junior School Kasangati",
    "hero_subtitle": "Nurturing Excellence & Character Development",
    "about_title": "Welcome to Hilltop Junior School",
    "about_text": "Hilltop Junior School is a warm and vibrant learning community offering Daycare, Kindergarten, and Primary education. We provide a safe, friendly, and inclusive environment where every child thrives academically, socially, and personally.",
    "about_link": "/about",
    "core_values": [
        {"title": "Community", "description": "We build connections between students, staff and families for mutual support."},
        {"title": "Respect", "description": "We value diversity, kindness and dignity for all."},
        {"title": "Excellence", "description": "We strive for high standards in learning and behavior."},
        {"title": "Curiosity", "description": "We encourage exploration, creativity and love of learning."}
    ]
}

# About Page Content
about_data = {
    "vision": "To nurture confident, creative, and responsible learners who will contribute positively to society.",
    "mission": "To provide accessible quality education in a safe, supportive, and inclusive environment.",
    "director": "Mr. John Smith",
    "head_teacher": "Mrs. Sarah Johnson",
    "deputy_head_teacher": "Mr. David Ochieng",
    "achievements": "Award-winning school with excellent UCCE exam results. Recognized for innovative teaching methods and holistic child development."
}

# Contact Info
contact_data = {
    "address": "Kasangati, Wakiso District, Uganda",
    "phone_number": "+256 771 234 567",
    "email": "info@hilltopjunior.ug",
    "working_hours": "Monday - Friday: 7:00 AM - 5:00 PM",
    "additional_notes": "Office hours: 8:00 AM - 4:00 PM. For emergencies, call the duty officer."
}

# Footer Info (same as contact for now)
footer_data = {
    "address": "Kasangati, Wakiso District, Uganda",
    "phone_number": "+256 771 234 567",
    "email": "info@hilltopjunior.ug",
    "working_hours": "Monday - Friday: 7:00 AM - 5:00 PM",
    "additional_notes": "P.O. Box 12345, Kampala"
}

def update_home():
    print("📝 Updating Home Page...")
    try:
        response = requests.put(f"{BASE_URL}/home", json=home_data)
        if response.status_code in [200, 201]:
            print("✅ Home page updated successfully")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating home: {e}")
        return False

def update_about():
    print("📝 Updating About Page...")
    try:
        response = requests.put(f"{BASE_URL}/about", json=about_data)
        if response.status_code in [200, 201]:
            print("✅ About page updated successfully")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating about: {e}")
        return False

def update_contact():
    print("📝 Updating Contact Info...")
    try:
        # First try to get existing contact
        get_response = requests.get(f"{BASE_URL}/contact_info")
        if get_response.status_code == 200:
            contacts = get_response.json()
            if contacts and len(contacts) > 0:
                # Update existing contact
                contact_id = contacts[0]['id']
                response = requests.put(f"{BASE_URL}/contact_info/{contact_id}", json=contact_data)
            else:
                # Create new contact
                response = requests.post(f"{BASE_URL}/contact_info", json=contact_data)
        else:
            # Create new contact
            response = requests.post(f"{BASE_URL}/contact_info", json=contact_data)
        
        if response.status_code in [200, 201]:
            print("✅ Contact info updated successfully")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating contact: {e}")
        return False

def update_footer():
    print("📝 Updating Footer...")
    try:
        # First try to get existing footer
        get_response = requests.get(f"{BASE_URL}/footer")
        if get_response.status_code == 200:
            footers = get_response.json()
            if footers and len(footers) > 0:
                # Update existing footer
                footer_id = footers[0]['id']
                response = requests.put(f"{BASE_URL}/footer/{footer_id}", json=footer_data)
            else:
                # Create new footer
                response = requests.post(f"{BASE_URL}/footer", json=footer_data)
        else:
            # Create new footer
            response = requests.post(f"{BASE_URL}/footer", json=footer_data)
        
        if response.status_code in [200, 201]:
            print("✅ Footer updated successfully")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating footer: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Dashboard Content Population...\n")
    
    results = {
        "Home": update_home(),
        "About": update_about(),
        "Contact": update_contact(),
        "Footer": update_footer()
    }
    
    print("\n" + "="*50)
    print("📊 Summary:")
    for section, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {section}: {'Updated' if success else 'Failed'}")
    print("="*50)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n📈 Results: {passed}/{total} sections updated successfully")
