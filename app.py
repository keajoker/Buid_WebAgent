import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from textblob import TextBlob
import re

# Function to correct spelling and handle missing spaces
def preprocess_input(question):
     #Correct spelling mistakes
    corrected_question = str(TextBlob(question).correct())

    # Handle missing spaces (e.g., "whatisyourname" -> "what is your name")
    # Using a simple dictionary-based approach for common merged words
    common_phrases = {
        "whatis": "what is",
        "howare": "how are",
        "buid": "BUiD",
        "contactus": "contact us",
        "libraryservices": "library services"
    }
    for merged, fixed in common_phrases.items():
        corrected_question = re.sub(merged, fixed, corrected_question)

    #  Extract keywords and map synonyms
    synonyms_map = {
        "faculty": "engineering",
        "program": "programmes",
        "degree": "programmes",
        "help": "support",
        "fee": "tuition fees",
        "cost": "tuition fees",
        "scholarship": "scholarships",
        "admission": "admission requirements"
    }
    words = corrected_question.split()
    normalized_words = [synonyms_map.get(word, word) for word in words]

    # Join the words back into a single string
    normalized_question = " ".join(normalized_words)

    return normalized_question


# Removes common keywords so the bot can process the question with ease
def extract_keywords(question):
    words = re.findall(r'\b\w+\b', question.lower())
    common_words = {'the', 'is', 'in', 'at', 'which', 'on', 'and', 'a', 'an', 'of', 'to', 'how', 'what', 'why', 'where'}
    keywords = [word for word in words if word not in common_words]
    return keywords

# All possible questions that can be asked
def answer_question(question, all_paragraphs):
    greetings = [
        "Hello there! How can I assist you today?",
        "Hi! What can I assist you with?",
        "Good day! How may I help you?"
    ]

    goodbyes = [
        "Goodbye!",
        "Farewell!",
        "Take care!"
    ]

    engineering_answers = [
        ("BUiD's Faculty of Engineering and IT offers a variety of programmes including Bachelor's, Master's, "
         "and Doctoral degrees in fields such as Artificial Intelligence, Cybersecurity, and Electro-Mechanical Engineering. "
         "These programmes are designed to equip students with the knowledge and skills needed to excel in their careers. "
         "You can find more details on their website under the 'Faculty of Engineering and IT' section."),
        ("The Faculty of Engineering and IT at BUiD provides comprehensive education in areas like AI, Cybersecurity, and Electro-Mechanical Engineering "
         "with programmes at the Bachelor's, Master's, and Doctoral levels. Visit the BUiD website for more info under 'Faculty of Engineering and IT'."),
        ("Explore BUiD's Engineering and IT programmes, including degrees in AI, Cybersecurity, and more. They offer Bachelor's, Master's, and Doctoral degrees. "
         "Check the 'Faculty of Engineering and IT' section on their website for details.")
    ]

    contact_us_answers = [
        ("To contact BUiD, you can visit the 'Contact Us' section on their website. "
         "Here are the main contact details:\n"
         "Address: BUiD, Block 11, Dubai International Academic City (DIAC), Dubai, UAE\n"
         "Phone: +971 4 279 1400\n"
         "Email: info@buid.ac.ae\n"
         "You can also find a contact form on their website for specific inquiries."),
        ("For contacting BUiD, head to the 'Contact Us' page on their website. "
         "Main details are:\n"
         "Address: BUiD, Block 11, DIAC, Dubai, UAE\n"
         "Phone: +971 4 279 1400\n"
         "Email: info@buid.ac.ae\n"
         "A contact form is also available on the site."),
        ("Reach out to BUiD via the 'Contact Us' section on their site. Here’s how:\n"
         "Address: BUiD, Block 11, Dubai International Academic City, Dubai, UAE\n"
         "Phone: +971 4 279 1400\n"
         "Email: info@buid.ac.ae\n"
         "You can also fill out a contact form online.")
    ]

    library_services_answers = [
        ("The BUiD Library offers a wide range of services to support the academic and research needs of students and faculty. "
         "These services include access to an extensive collection of books, journals, and online resources, research assistance, and study spaces. "
         "You can learn more about the library services and access the online catalog on the 'Library Services' section of the BUiD website or contact them via email at library@buid.ac.ae."),
        ("BUiD Library provides extensive support for academic and research needs, including a vast collection of books, journals, and online resources, along with research help and study spaces. "
         "For more info, visit the 'Library Services' section on the BUiD website or email library@buid.ac.ae."),
        ("Offering a wealth of academic support, the BUiD Library features a large collection of books, journals, and online resources, research aid, and study areas. "
         "Find out more in the 'Library Services' section of the BUiD website or contact them at library@buid.ac.ae.")
    ]

    research_guides_answers = [
        ("Research guides at BUiD are designed to assist students in their academic research projects. "
         "These guides provide resources, methodologies, and tips for conducting effective research. "
         "You can find research guides for various disciplines on the BUiD website under the 'Research Guides' section."),
        ("BUiD's research guides support students in their academic research projects by offering resources, methodologies, and tips for effective research. "
         "Visit the 'Research Guides' section on the BUiD website for more information."),
        ("Explore the research guides at BUiD to assist in your academic research projects. They provide valuable resources, methodologies, and tips for effective research. "
         "Check the 'Research Guides' section on the BUiD website.")
    ]

    scholarships_answers = [
        ("BUiD offers a range of scholarships to support students in their studies. These scholarships are awarded based on academic merit, financial need, and other criteria. "
         "To apply for scholarships or learn more about the available opportunities, you can visit the 'Scholarships' section on the BUiD website or email scholarships@buid.ac.ae."),
        ("Various scholarships are available at BUiD to support students based on academic merit, financial need, and other criteria. "
         "For more information and to apply, visit the 'Scholarships' section on the BUiD website or contact scholarships@buid.ac.ae."),
        ("BUiD offers scholarships to support students' studies, awarded based on criteria like academic merit and financial need. "
         "Find out more about available opportunities on the 'Scholarships' section of the BUiD website or email scholarships@buid.ac.ae.")
    ]

    academic_staff_answers = [
        ("BUiD's academic staff consists of experienced professors and researchers who are experts in their fields. "
         "They are committed to providing high-quality education and conducting impactful research. "
         "You can learn more about the academic staff, including their qualifications and research interests, on the 'Academic Staff' section of the BUiD website."),
        ("The academic staff at BUiD includes experienced professors and researchers who excel in their fields. "
         "They offer high-quality education and conduct significant research. "
         "More details about their qualifications and research interests are available in the 'Academic Staff' section of the BUiD website."),
        ("Experienced professors and researchers make up the academic staff at BUiD, providing high-quality education and impactful research. "
         "Learn more about their qualifications and interests on the 'Academic Staff' section of the BUiD website.")
    ]

    student_services_answers = [
        ("BUiD's Student Services department provides a range of support services to enhance the student experience. "
         "These services include academic advising, counseling, career services, and extracurricular activities. "
         "For more information or assistance, you can contact Student Services via email at masters@buid.ac.ae for Masters students or undergrad@buid.ac.ae for undergraduate students."),
        ("Student Services at BUiD offers various support services to improve the student experience, including academic advising, counseling, career services, and extracurricular activities. "
         "Contact them via email at masters@buid.ac.ae for Masters students or undergrad@buid.ac.ae for undergraduate students for more assistance."),
        ("Enhance your student experience with the support services provided by BUiD's Student Services, including academic advising, counseling, career services, and extracurricular activities. "
         "For more details, email masters@buid.ac.ae for Masters students or undergrad@buid.ac.ae for undergraduate students.")
    ]

    it_support_answers = [
        ("BUiD's IT Services department provides technical support and resources to ensure that students and staff can effectively use the university's IT systems. "
         "For assistance with technical issues, you can contact IT Services via email at itservices@buid.ac.ae."),
        ("Get technical support and resources from BUiD's IT Services to use the university's IT systems efficiently. "
         "Contact IT Services via email at itservices@buid.ac.ae for assistance with technical issues."),
        ("BUiD's IT Services offers technical support and resources to help students and staff effectively use the IT systems. "
         "Reach out to IT Services via email at itservices@buid.ac.ae for help with any technical problems.")
    ]

    best_doctor_answers = [
        "The best doctor is Dr. Hend Elmohandes.",
        "Dr. Hend Elmohandes is the best doctor.",
        "According to many, Dr. Hend Elmohandes is the best doctor."
    ]
    
    programmes_answers = [
        ("BUiD offers a variety of programmes at the undergraduate, postgraduate, and doctoral levels. "
         "These programmes cover fields such as Business, Engineering, Computer Science, and Education. "
         "Each programme is designed to provide students with the knowledge and skills needed to succeed in their careers. "
         "You can find more information about the programmes offered by BUiD on their website under the 'Programmes' section."),
        ("Explore the wide range of programmes at BUiD, including undergraduate, postgraduate, and doctoral levels in fields like Business, Engineering, Computer Science, and Education. "
         "Each programme equips students with essential skills for their careers. Check the 'Programmes' section on the BUiD website for more details."),
        ("BUiD provides various programmes at different levels—undergraduate, postgraduate, and doctoral—in areas such as Business, Engineering, Computer Science, and Education. "
         "These programmes are tailored to help students thrive in their careers. For more info, visit the 'Programmes' section of the BUiD website.")
    ]

    admission_requirements_answers = [
        ("The admission requirements for BUiD vary depending on the programme you are applying for. Generally, they require academic transcripts, English language proficiency test scores, "
         "a statement of purpose, and letters of recommendation. Specific requirements can be found on the 'Admissions' section of the BUiD website."),
        ("BUiD's admission requirements differ by programme, typically including academic transcripts, English proficiency test scores, "
         "a statement of purpose, and recommendation letters. Detailed requirements are available on the 'Admissions' section of the BUiD website."),
        ("For admission to BUiD, requirements include academic transcripts, English language test scores, a statement of purpose, and recommendation letters, varying by programme. "
         "Visit the 'Admissions' section on the BUiD website for specific details.")
    ]



    campus_facilities_answers = [
        ("BUiD's campus offers a range of facilities to support students' academic and extracurricular activities. Facilities include modern classrooms, a library, computer labs, and recreational areas. "
         "More information about campus facilities can be found on the 'Campus Facilities' section of the BUiD website."),
        ("Explore BUiD's campus facilities, which support both academic and extracurricular activities, including modern classrooms, a library, computer labs, and recreational areas. "
         "Details are available on the 'Campus Facilities' section of the BUiD website."),
        ("The campus at BUiD provides facilities such as modern classrooms, a library, computer labs, and recreational areas to support student activities. "
         "Learn more in the 'Campus Facilities' section of the BUiD website.")
    ]

    alumni_network_answers = [
        ("BUiD has a vibrant alumni network that offers opportunities for networking, professional development, and career advancement. "
         "Alumni can stay connected with the university through various events and activities. More details can be found on the 'Alumni Network' section of the BUiD website."),
        ("Join BUiD's active alumni network for networking, professional growth, and career opportunities. Stay connected through events and activities. "
         "Visit the 'Alumni Network' section of the BUiD website for more information."),
        ("BUiD's alumni network provides networking, professional development, and career advancement opportunities. Alumni stay engaged through diverse events and activities. "
         "Check the 'Alumni Network' section on the BUiD website for details.")
    ]

    research_opportunities_answers = [
        ("BUiD offers numerous research opportunities for students and faculty. These include funded research projects, collaborative research with industry partners, and access to research facilities. "
         "More information can be found on the 'Research Opportunities' section of the BUiD website."),
        ("Discover research opportunities at BUiD, including funded projects, industry collaborations, and access to research facilities. "
         "Visit the 'Research Opportunities' section of the BUiD website for more information."),
        ("Engage in various research opportunities at BUiD, from funded projects to collaborations with industry partners and research facility access. "
         "Find more details in the 'Research Opportunities' section on the BUiD website.")
    ]
    bachelor_answers = [
    ("BUiD offers a range of Bachelor's programs in fields such as Engineering, Business, and Computer Science. "
     "These programs are designed to provide a solid foundation in the chosen field and prepare students for professional careers. "
     "More information can be found on the 'Undergraduate Programs' section of the BUiD website."),
    ("Explore BUiD's Bachelor's programs in Engineering, Business, and Computer Science. These programs aim to give students a strong foundation for their professional careers. "
     "Visit the 'Undergraduate Programs' section of the BUiD website for more details."),
    ("BUiD provides various Bachelor's programs in fields like Engineering, Business, and Computer Science, aimed at equipping students with the necessary skills for their careers. "
     "Check out the 'Undergraduate Programs' section on the BUiD website.")
    ]

    masters_answers = [
    ("BUiD's Master's programs offer advanced education in various disciplines including Engineering, Business Administration, and Information Technology. "
    "These programs aim to enhance professional skills and knowledge. "
    "Details about the courses, admission requirements, and application process can be found in the 'Postgraduate Programs' section on the BUiD website."),
    ("For advanced education, BUiD provides Master's programs in Engineering, Business Administration, and IT. "
    "These programs are designed to enhance professional skills and knowledge. "
    "Find more information on the 'Postgraduate Programs' section of the BUiD website."),
    ("Master's programs at BUiD cover various fields such as Engineering, Business Administration, and IT, aiming to boost your professional skills. "
    "You can find more details on the 'Postgraduate Programs' section of the BUiD website.")
    ]

    phd_answer = [
    ("BUiD offers PhD programs in several fields such as Engineering, Business, and Education. "
     "These doctoral programs are research-intensive and designed for students looking to contribute original knowledge to their field of study. "
     "You can find more information about the PhD programs, including research areas and supervisors, on the 'Doctoral Programs' section of the BUiD website."),
    ("PhD programs at BUiD span across various fields like Engineering, Business, and Education. "
     "These research-focused programs are meant for students who aim to contribute original knowledge to their fields. "
     "Check out the 'Doctoral Programs' section on the BUiD website for more details."),
    ("Explore PhD programs at BUiD in fields like Engineering, Business, and Education. "
     "These programs focus on original research and contribution to knowledge in your field. "
     "More details can be found in the 'Doctoral Programs' section of the BUiD website.")
    ]


    application_process_answers = [
    ("The application process at BUiD involves submitting an online application form along with the required documents such as transcripts, proof of English proficiency, and a personal statement. "
     "You can find detailed information about the application process on the 'Admissions' section of the BUiD website."),
    ("To apply to BUiD, you need to fill out an online application form and submit necessary documents including transcripts and a personal statement. "
     "Visit the 'Admissions' section on the BUiD website for more details about the application process."),
    ("BUiD's application process requires an online application form, transcripts, proof of English proficiency, and a personal statement. "
     "Check the 'Admissions' section of the BUiD website for comprehensive details.")
    ]

    financial_aid_answers = [
    ("BUiD offers various financial aid options including scholarships and bursaries to help students finance their education. "
     "Details about financial aid can be found on the 'Financial Aid' section of the BUiD website."),
    ("To support students, BUiD provides scholarships and bursaries. More information about financial aid options is available in the 'Financial Aid' section of the BUiD website."),
    ("Explore BUiD's financial aid options such as scholarships and bursaries on the 'Financial Aid' section of the BUiD website to help fund your education.")
    ]

    course_schedule_answers = [
    ("Course schedules at BUiD are available through the student portal. You can view your class timings, assignments, and exam dates by logging into the portal. "
     "If you need assistance, please contact the academic office."),
    ("To view your course schedule, log into the BUiD student portal where you can find details about class timings, assignments, and exams. "
     "For further assistance, contact the academic office."),
    ("BUiD's course schedules can be accessed through the student portal, which provides information on class timings, assignments, and exam dates. "
     "For more help, reach out to the academic office.")
    ]

    internships_answers = [
    ("BUiD offers internship opportunities to students in various programs to gain practical experience in their field of study. "
     "Internship placements are coordinated through the career services office. More details can be found on the BUiD website."),
    ("To gain hands-on experience, BUiD provides internship opportunities for students across different programs. "
     "For more information, visit the career services office or check the BUiD website."),
    ("Explore internship opportunities at BUiD to gain practical experience in your field. For placement details, contact the career services office or visit the BUiD website.")
    ]

    career_services_answers = [
    ("BUiD's career services office offers support such as resume writing workshops, job search assistance, and career counseling. "
     "Visit the 'Career Services' section of the BUiD website for more information."),
    ("To help students with their career goals, BUiD's career services provides workshops, job search assistance, and counseling. "
     "More details can be found on the 'Career Services' section of the BUiD website."),
    ("BUiD's career services office supports students with resume writing, job searches, and career counseling. "
     "Visit the 'Career Services' section of the BUiD website for more details.")
    ]

    library_hours_answers = [
    ("The BUiD Library is open from 8 AM to 10 PM on weekdays and 10 AM to 6 PM on weekends. "
     "For more details, visit the 'Library Hours' section on the BUiD website."),
    ("BUiD Library operates from 8 AM to 10 PM during weekdays and 10 AM to 6 PM on weekends. "
     "Check the 'Library Hours' section of the BUiD website for more information."),
    ("Library hours at BUiD are 8 AM to 10 PM on weekdays and 10 AM to 6 PM on weekends. "
     "For more details, visit the 'Library Hours' section of the BUiD website.")
    ]

    faculties_answers = [
    ("BUiD has several faculties including Engineering, Business, Education, and IT. "
     "Each faculty offers specialized programs and research opportunities. More information can be found on the 'Faculties' section of the BUiD website."),
    ("Explore BUiD's faculties such as Engineering, Business, Education, and IT, which offer specialized programs and research opportunities. "
     "Visit the 'Faculties' section of the BUiD website for more details."),
    ("BUiD's faculties include Engineering, Business, Education, and IT, each offering specialized programs. "
     "Check out the 'Faculties' section on the BUiD website for more information.")
    ]
    
    academic_calendar_answers = [
    ("BUiD's academic calendar outlines the important dates and deadlines for the academic year, including start and end dates for terms, exam periods, and holidays. "
     "You can find the detailed academic calendar on the 'Academic Calendar' section of the BUiD website."),
    ("The academic calendar at BUiD provides crucial information on term dates, exam schedules, and holidays. "
     "For more details, visit the 'Academic Calendar' section on the BUiD website."),
    ("BUiD's academic calendar is your guide to the key dates and deadlines throughout the academic year, including term start and end dates, exams, and holidays. "
     "More information is available in the 'Academic Calendar' section of the BUiD website.")
    ]

    graduation_answers = [
    ("Graduation ceremonies at BUiD celebrate the achievements of students completing their programs. "
     "Details about graduation dates, requirements, and procedures can be found in the 'Graduation' section of the BUiD website."),
    ("BUiD holds graduation ceremonies to honor students who have completed their degrees. "
     "For more information on graduation dates and requirements, visit the 'Graduation' section on the BUiD website."),
    ("The graduation process at BUiD includes ceremonies to celebrate students' accomplishments. "
     "You can find more details about graduation requirements and schedules in the 'Graduation' section of the BUiD website.")
    ]

    events_answers = [
    ("BUiD hosts a variety of events throughout the year, including academic seminars, cultural activities, and networking opportunities. "
     "Details about upcoming events can be found in the 'Events' section of the BUiD website."),
    ("From academic seminars to cultural activities, BUiD organizes numerous events for students and faculty. "
     "Check the 'Events' section on the BUiD website for a schedule of upcoming events."),
    ("Stay updated on BUiD's events, including seminars, workshops, and cultural activities, by visiting the 'Events' section of the BUiD website.")
]    

    clubs_societies_answers = [
    ("BUiD offers various clubs and societies that provide opportunities for students to engage in extracurricular activities and connect with peers. "
     "You can learn more about the different clubs and societies available on the 'Student Clubs' section of the BUiD website."),
    ("Engage in extracurricular activities at BUiD by joining one of the many student clubs and societies. "
     "More information can be found in the 'Student Clubs' section on the BUiD website."),
    ("BUiD's student clubs and societies offer a range of activities and opportunities to connect with fellow students. "
     "Visit the 'Student Clubs' section of the BUiD website for more details.")
    ]

    study_abroad_answers = [
    ("BUiD provides study abroad and exchange programs for students to gain international experience. "
     "Details about these opportunities can be found in the 'Study Abroad' section of the BUiD website."),
    ("Explore BUiD's study abroad and exchange programs, which offer students the chance to study at partner institutions worldwide. "
     "More information is available in the 'Study Abroad' section of the BUiD website."),
    ("Gain international exposure through BUiD's study abroad and exchange programs. "
     "Visit the 'Study Abroad' section on the BUiD website for details about these opportunities.")
    ]

    health_services_answers = [
    ("BUiD provides health services to support the well-being of students and staff. "
     "More information about available health services can be found in the 'Health Services' section of the BUiD website."),
    ("Access health services at BUiD to support your physical and mental well-being. "
     "Details about these services are available in the 'Health Services' section of the BUiD website."),
    ("BUiD's health services offer a range of support for students and staff. "
     "Find out more about available services in the 'Health Services' section of the BUiD website.")
    ]


    campus_safety_answers = [
    ("BUiD prioritizes campus safety to ensure a secure environment for students and staff. "
     "More information about campus safety measures can be found in the 'Campus Safety' section of the BUiD website."),
    ("Stay informed about campus safety protocols and measures implemented at BUiD. "
     "Details are available in the 'Campus Safety' section on the BUiD website."),
    ("BUiD's campus safety initiatives are designed to protect students and staff. "
     "Find more information in the 'Campus Safety' section of the BUiD website.")
    ]


    student_portal_answers = [
    ("The student portal at BUiD provides access to important academic and administrative resources. "
     "You can log in to the student portal via the BUiD website."),
    ("Access the BUiD student portal for academic and administrative resources. "
     "Log in via the BUiD website."),
    ("The BUiD student portal is your gateway to essential academic and administrative services. "
     "Visit the BUiD website to log in.")
    ]

    tuition_fees_answers = [
    ("The tuition fees at BUiD range from AED 56,000 to AED 85,000 per year, depending on the degree and program. "
     "These fees may be reduced if you receive a scholarship. For more detailed information on the fee structure and specific programs, you can visit the "
     "[BUiD Fees page](https://www.buid.ac.ae/programme/fees/)."),
    ("BUiD's tuition fees vary between AED 56,000 and AED 85,000 per year, based on the degree and program. "
     "Scholarships can help reduce these fees. Additional details on fees for various programs can be found on the "
     "[BUiD Fees page](https://www.buid.ac.ae/programme/fees/)."),
    ("The tuition fees for programs at BUiD range from AED 56,000 to AED 85,000 annually, depending on the specific degree and program. "
     "Receiving a scholarship can lower these fees. You can find more comprehensive information about the fee structure on the "
     "[BUiD Fees page](https://www.buid.ac.ae/programme/fees/).")
    ]


    

    # ... Add more categories of responses as needed ...
    
    
    if question.lower() in ['hi', 'hello', 'good morning', 'good afternoon', 'good evening', 'morning', 'good day', 'hey', 'hey there', 'hi there', 'howdy', 'greetings', 'sup', 'what\'s up', 'yo', 'hiya', 'how\'s it going', 'how\'s everything', 'how are you', 'what\'s new', 'nice to see you', 'long time no see', 'good to see you', 'hello there', 'what\'s happening', 'hiii', 'helloooo', 'heyyy', 'hiiiiii', 'heyyy there', 'hiii there', 'yoo', 'hi hi', 'heeey', 'hello hello', 'hiyaaa']:
        return random.choice(greetings)

    
    elif question.lower() in ['exit', 'bye', 'quit']:
        return random.choice(goodbyes)
    
    elif any(keyword in question.lower() for keyword in ['engineering', 'engineer', 'computer']):
        return random.choice(engineering_answers)
    
    elif "contact us" in question.lower() or "contact" in question.lower():
        return random.choice(contact_us_answers)
    elif "library services" in question.lower():
        return random.choice(library_services_answers)
    elif "research guides" in question.lower():
        return random.choice(research_guides_answers)
    elif "scholarships" in question.lower():
        return random.choice(scholarships_answers)
    elif "academic staff" in question.lower():
        return random.choice(academic_staff_answers)
    elif "student services" in question.lower():
        return random.choice(student_services_answers)
    elif "IT support" in question.lower():
        return random.choice(it_support_answers)
    elif "programmes" in question.lower():
        return random.choice(programmes_answers)
    elif "admission requirements" in question.lower():
        return random.choice(admission_requirements_answers)
    elif "campus facilities" in question.lower():
        return random.choice(campus_facilities_answers)
    elif "alumni network" in question.lower():
        return random.choice(alumni_network_answers)
    elif "research opportunities" in question.lower():
        return random.choice(research_opportunities_answers)
    elif "bachelor programs" in question.lower() or "undergraduate" in question.lower():
        return random.choice(bachelor_answers)
    elif "master programs" in question.lower() or "postgraduate" in question.lower():
        return random.choice(masters_answers)
    elif "phd programs" in question.lower() or "doctoral" in question.lower() or "phd" in question.lower():
        return random.choice(phd_answer)
    elif "access blackboard" in question.lower() or "blackboard login" in question.lower() or "blackboard" in question.lower(): 
        return ("Blackboard is the online learning management system used by BUiD. To access Blackboard, you need to use your student login credentials provided by the university. " 
            "You can log in to Blackboard via the BUiD website under the 'Student Services' section or directly at [Blackboard Login](https://blackboard.buid.ac.ae). " 
            "If you face any issues, you can contact IT support at itservices@buid.ac.ae.")
    elif "application" in question.lower() or "apply" in question.lower():
                return random.choice(application_process_answers)
    elif "financial aid" in question.lower() or "aid" in question.lower():
                return random.choice(financial_aid_answers)
    elif "course schedule" in question.lower() or "class schedule" in question.lower() or "class timing" in question.lower() or "class time" in question.lower():
                return random.choice(course_schedule_answers)
    elif "internships" in question.lower() or "internship opportunities" in question.lower():
                return random.choice(internships_answers)
    elif "career services" in question.lower() or "career support" in question.lower():
                return random.choice(career_services_answers)
    elif "library hours" in question.lower() or "library timing" in question.lower():
                return random.choice(library_hours_answers)
    elif "faculties" in question.lower() or "faculty" in question.lower():
                return random.choice(faculties_answers)
    elif "academic calendar" in question.lower() or "calendar" in question.lower():
                return random.choice(academic_calendar_answers)
    elif "graduation" in question.lower() or "graduate" in question.lower():
                return random.choice(graduation_answers)
    elif "events" in question.lower() or "event" in question.lower():
                return random.choice(events_answers)
    elif "clubs and societies" in question.lower() or "student clubs" in question.lower() or "clubs" in question.lower():
                return random.choice(clubs_societies_answers)
    elif "study abroad" in question.lower() or "exchange programs" in question.lower():
                return random.choice(study_abroad_answers)
    elif "health services" in question.lower() or "health center" in question.lower() or "health" in question.lower():
                return random.choice(health_services_answers)
    elif "student portal" in question.lower():
                return random.choice(student_portal_answers)
    elif "best doctor" in question.lower() or "best lecturer" in question.lower() or "best teacher" in question.lower() or "best professor" in question.lower() or "best" in question.lower() or "goat" in question.lower():
                return random.choice(best_doctor_answers)
    elif "campus safety" in question.lower() or "security" in question.lower() or "safe" in question.lower() or "secure" in question.lower():
                return random.choice(campus_safety_answers)
    elif "fees" in question.lower() or "tuition fees" in question.lower() or "price" in question.lower() or "fee" in question.lower() or "cost" in question.lower():
                return random.choice(tuition_fees_answers)
    
    else:
        # Attempt to auto-correct the question
        corrected_question = str(TextBlob(question).correct())
        print(f"Corrected Question: {corrected_question}")
        
        # Try to get an answer for the corrected question
        second_try_answer = ""
        
        
        if corrected_question.lower() in ['hi', 'hello', 'good morning', 'good afternoon', 'good evening', 'morning', 'good day', 'hey', 'hey there', 'hi there', 'howdy', 'greetings', 'sup', 'what\'s up', 'yo', 'hiya', 'how\'s it going', 'how\'s everything', 'how are you', 'what\'s new', 'nice to see you', 'long time no see', 'good to see you', 'hello there', 'what\'s happening', 'hiii', 'helloooo', 'heyyy', 'hiiiiii', 'heyyy there', 'hiii there', 'yoo', 'hi hi', 'heeey', 'hello hello', 'hiyaaa']:
            second_try_answer = random.choice(greetings)

    
        elif corrected_question.lower() in ['exit', 'bye', 'quit']:
            second_try_answer = random.choice(goodbyes)
    
        elif any(keyword in corrected_question.lower() for keyword in ['engineering', 'engineer', 'computer']):
            second_try_answer = random.choice(engineering_answers)
    
        elif "contact us" in corrected_question.lower() or "contact" in corrected_question.lower():
            second_try_answer = random.choice(contact_us_answers)
        elif "library services" in corrected_question.lower():
            second_try_answer = random.choice(library_services_answers)
        elif "research guides" in corrected_question.lower():
            second_try_answer = random.choice(research_guides_answers)
        elif "scholarships" in corrected_question.lower():
            second_try_answer = random.choice(scholarships_answers)
        elif "academic staff" in corrected_question.lower():
            second_try_answer = random.choice(academic_staff_answers)
        elif "student services" in corrected_question.lower():
            second_try_answer = random.choice(student_services_answers)
        elif "IT support" in corrected_question.lower():
            second_try_answer = random.choice(it_support_answers)
        elif "programmes" in corrected_question.lower():
            second_try_answer = random.choice(programmes_answers)
        elif "admission requirements" in corrected_question.lower():
            second_try_answer = random.choice(admission_requirements_answers)
        elif "campus facilities" in corrected_question.lower():
            second_try_answer = random.choice(campus_facilities_answers)
        elif "alumni network" in corrected_question.lower():
            second_try_answer = random.choice(alumni_network_answers)
        elif "research opportunities" in corrected_question.lower():
            second_try_answer = random.choice(research_opportunities_answers)
        elif "bachelor programs" in corrected_question.lower() or "undergraduate" in corrected_question.lower():
            second_try_answer = random.choice(bachelor_answers)
        elif "master programs" in corrected_question.lower() or "postgraduate" in corrected_question.lower():
            second_try_answer = random.choice(masters_answers)
        elif "phd programs" in corrected_question.lower() or "doctoral" in corrected_question.lower() or "phd" in corrected_question.lower():
            second_try_answer = random.choice(phd_answer)
        elif "access blackboard" in corrected_question.lower() or "blackboard login" in corrected_question.lower() or "blackboard" in corrected_question.lower(): 
            second_try_answer = ("Blackboard is the online learning management system used by BUiD. To access Blackboard, you need to use your student login credentials provided by the university. " 
            "You can log in to Blackboard via the BUiD website under the 'Student Services' section or directly at [Blackboard Login](https://blackboard.buid.ac.ae). " 
            "If you face any issues, you can contact IT support at itservices@buid.ac.ae.")
        elif "application" in corrected_question.lower() or "apply" in corrected_question.lower():
                second_try_answer = random.choice(application_process_answers)
        elif "financial aid" in corrected_question.lower() or "aid" in corrected_question.lower():
                second_try_answer = random.choice(financial_aid_answers)
        elif "course schedule" in corrected_question.lower() or "class schedule" in corrected_question.lower() or "class timing" in corrected_question.lower() or "class time" in corrected_question.lower():
                second_try_answer = random.choice(course_schedule_answers)
        elif "internships" in corrected_question.lower() or "internship opportunities" in corrected_question.lower():
                second_try_answer = random.choice(internships_answers)
        elif "career services" in corrected_question.lower() or "career support" in corrected_question.lower():
                second_try_answer = random.choice(career_services_answers)
        elif "library hours" in corrected_question.lower() or "library timing" in corrected_question.lower():
                second_try_answer = random.choice(library_hours_answers)
        elif "faculties" in corrected_question.lower() or "faculty" in corrected_question.lower():
                second_try_answer = random.choice(faculties_answers)
        elif "academic calendar" in corrected_question.lower() or "calendar" in corrected_question.lower():
                second_try_answer = random.choice(academic_calendar_answers)
        elif "graduation" in corrected_question.lower() or "graduate" in corrected_question.lower():
                second_try_answer = random.choice(graduation_answers)
        elif "events" in corrected_question.lower() or "event" in corrected_question.lower():
                second_try_answer = random.choice(events_answers)
        elif "clubs and societies" in corrected_question.lower() or "student clubs" in corrected_question.lower() or "clubs" in corrected_question.lower():
                second_try_answer = random.choice(clubs_societies_answers)
        elif "study abroad" in corrected_question.lower() or "exchange programs" in corrected_question.lower():
                second_try_answer = random.choice(study_abroad_answers)
        elif "health services" in corrected_question.lower() or "health center" in corrected_question.lower() or "health" in corrected_question.lower():
                second_try_answer = random.choice(health_services_answers)
        elif "student portal" in corrected_question.lower():
                second_try_answer = random.choice(student_portal_answers)
        elif "best doctor" in corrected_question.lower() or "best lecturer" in corrected_question.lower() or "best teacher" in corrected_question.lower() or "best professor" in corrected_question.lower() or "best" in corrected_question.lower() or "goat" in corrected_question.lower():
                second_try_answer = random.choice(best_doctor_answers)
        elif "campus safety" in corrected_question.lower() or "security" in corrected_question.lower() or "safe" in corrected_question.lower() or "secure" in corrected_question.lower():
                second_try_answer = random.choice(campus_safety_answers)
        elif "fees" in corrected_question.lower() or "tuition fees" in corrected_question.lower() or "price" in corrected_question.lower():
                second_try_answer = random.choice(tuition_fees_answers)
        else:
            second_try_answer = "Sorry, I couldn't understand your question. Can you please provide more details or try rephrasing it?"

        return second_try_answer


#You can add possible questions with answers if needed

#Allows the connection between the backend and frontend through local host
class MyServer(BaseHTTPRequestHandler):
    all_paragraphs = None

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        question = data.get("question", "")
        answer = answer_question(question, MyServer.all_paragraphs)
        response = {"answer": answer}
        self._set_response()
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))



#Creates the port were the the code will run on
def run(server_class=HTTPServer, handler_class=MyServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

#Runs the python code on the port given
if __name__ == '__main__':
    run()