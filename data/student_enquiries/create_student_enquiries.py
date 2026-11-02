import csv
from pathlib import Path

rows =[]

def add_example(label, topic, example):
    for text in example:
        rows.append(
            {
                "text": text,
                "label": label,
                "source_topic": topic
            }
        )

# Enrolment Enquiries
add_example("enrolment", "unit enrolment", [
    "How do I enrol in my units for next semester?",
    "Where can I add units to my enrolment?",
    "I need to enrol in subjects for the upcoming semester.",
    "What is the process for enrolling in a unit?",
    "Can someone tell me how to register for my units?"
])

add_example("enrolment", "choosing units", [
    "How do I know which units to choose for my degree?",
    "Where can I find the units I need to study?",
    "I am not sure which subjects to select for my course.",
    "How can I decide what units to take next semester?",
    "Which units am I supposed to choose for my degree?"
])

add_example("enrolment", "unit withdrawal", [
    "How can I withdraw from a unit I am enrolled in?",
    "I want to drop a subject I am currently enrolled in, what is the process?",
    "Where do I go to remove a unit from my enrolment?",
    "Can I stop studying one of my units this semester?",
    "What do I need to do if I want to leave a unit?"
])

add_example("enrolment", "withdrawal after census date", [
    "Can I withdraw from a unit after the census date?",
    "I missed the census date, can I still drop a subject?",
    "What happens if I want to withdraw from a unit after the census date?",
    "Is late withdrawal from a unit still possible?",
    "I need to leave a unit even though the census date has passed, what are my options?"
])

add_example("enrolment", "course withdrawal", [
    "How do I withdraw completely from my course?",
    "I want to stop studying my degree. What should I do?",
    "Where can I submit a request to withdraw from my course?",
    "Can I discontinue my course before I finish it?",
    "What is the process if I no longer want to continue my degree?"
])

add_example("enrolment", "study load", [
    "How many units can I take in a semester?",
    "What is considered a full-time study load?",
    "Can I study fewer units this semester?",
    "How many subjects do I need to take to remain full-time?",
    "I am unsure how many units I should enrol in."
])

add_example("enrolment", "unit prerequisites", [
    "How can I check the prerequisites for a unit?",
    "Why can't I enrol in a unit that has a prerequisite?",
    "Do I need to complete another subject before taking this unit?",
    "Where can I see the prerequisites a course requires?",
    "I want to enrol in a subject but I am not sure if I meet the requirements?"
])

add_example("enrolment", "unit waiver", [
    "Can I request a waiver to enrol in this unit?",
    "How do I apply for a unit prerequisite waiver?",
    "I don't meet the listed requirement. Can I still request permission to enrol?",
    "Where can I submit a unit waiver request?",
    "Can the prerequisite for a subject be waived?"
])

add_example("enrolment", "credit overload", [
    "Can I enrol in more units than the normal study load?",
    "How do I request permission to take extra subjects?",
    "I want to take more units this semester. Is that possible?",
    "Where can I apply for a credit overload?",
    "Am I allowed to study more than the standard number of credit units?"
])

add_example("enrolment", "class registration", [
    "How do I register for my tutorials?",
    "Where can I choose my class times?",
    "Where can I register for lectures and tutorials?",
    "I enrolled in the unit but haven't selected my class times yet. How do I do that?",
    "How can I change the class I registered for?"
])

# fees enquiries
add_example("fees","checking outstanding fees", [
    "How can I check if I have any outstanding fees?",
    "Where can I see how much I owe in fees?",
    "I want to check whether there are unpaid charges on my account.",
    "How do I find my current outstanding fees?",
    "Can I see online if I have any fees that need to be paid?"
])

add_example("fees","fee payment methods", [
    "What payment methods can I use to pay my university fees?",
    "How can I pay my tuition fees?",
    "Can I pay my university fees online?",
    "What options are available for paying my fees?",
    "Where do I go to make a fee payment?"
])

add_example("fees","fee payment due date", [
    "Where are my university fees due dates listed?",
    "How can I find the deadline for paying my tuition fees?",
    "What date do I need to pay my fees by?",
    "I am not sure when my fees are due.",
    "Where can I check the due date for my university fees?"
])

add_example("fees","student fee invoice", [
    "where can I find my student fee invoice?",
    "How do I download an invoice for my university fees?",
    "I need a copy of my fee invoice. Where can I get it?",
    "Can I view my tuition fee invoice online?",
    "Where is my university fee statement or invoice available?"
])

add_example("fees","international fee payment", [
    "How can an international student pay their tuition fees?",
    "What are the payment options for international student fees?",
    "Where should I pay my international tuition fees?",
    "Can international student pay their fees online?",
    "I need to pay my tuition fees as an international student. How do I do that?"
])

add_example("fees","fee refund after withdrawal", [
    "Can I get my fees refunded after I withdraw from a unit?",
    "What happens to my tuition fees if I withdraw from a subject?",
    "Am I eligible for a tuition refund after dropping a unit?",
    "How do I request a fee refund after withdrawing from a course?",
    "Will my unit fees be returned if I withdraw?"
])

add_example("fees","HECS-HELP debt remission", [
    "Can my HECS-HELP debt be remitted if I withdraw from a unit?",
    "How do I apply to have HECS-HELP debt remitted?",
    "Is it possible to reverse HECS-HELP debt for a withdrawn unit?",
    "What happens to my HECS debt if I withdraw under special circumstances?",
    "I withdrew from a unit and want to know if my HECS-HELP debt can be cancelled."
])

add_example("fees","FEE-HELP debt remission", [
    "Can I have my FEE-HELP debt removed after withdrawing from a unit?",
    "How do I request remission of a FEE-HELP debt?",
    "what happens to my FEE-HELP debt if I withdrew due to special circumstances?",
    "Can FEE-HELP charges for a withdrawn unit be reversed?",
    "I need to know whether my FEE-HELP debt can be cancelled."
])

add_example("fees","statement of outstanding charges", [
    "Where can I get a statement showing my outstanding charges?",
    "How do I view a statement of the fees I still owe?",
    "I need a document showing the unpaid charges on my student account.",
    "Can I download a statement of my outstanding university fees?",
    "Where can I find a summary of the charges remaining on my account?"
])

add_example("fees","fee liability after withdrawal", [
    "Will I still have to pay for a unit if I withdraw from it?",
    "What happens to my fees if I drop a unit?",
    "Do I still owe tuition fees after withdrawing from a subject?",
    "If I leave a unit, will I remain liable for its fees?",
    "How does withdrawing from a unit affect the fees I have to pay?"
])

# assessment enquiries
add_example("assessment","special consideration", [
    "How do I apply for special consideration?",
    "Can I request special consideration if something affected my assessment?",
    "Where do I submit a special consideration application?",
    "What should I do if unexpected circumstances impacted my assessment?",
    "I was unable to complete my assessment due to unforeseen events. How can I apply for special consideration?"
])

add_example("assessment","assessment extension", [
    "How can I request an extension for my assessment?",
    "Can I get more time to complete my assignment?",
    "I don't think I can finish my assessment on time. What should I do?",
    "Where can I apply for an extension on my assessment?",
    "What is the process for requesting an assessment extension?"
])

add_example("assessment","special consideration evidence", [
    "What evidence do I need to provide for special consideration application?",
    "Do I need supporting documents when applying for special consideration?",
    "What documents should I provide with my special consideration request?",
    "Will I need evidence to support my special consideration application?",
    "What kind of documentation is accepted for special consideration requests?"
])

add_example("assessment","special consideration deadline", [
    "When is the deadline to apply for special consideration?",
    "How long do I have to submit a special consideration request?",
    "Can I apply for special consideration after the assessment deadline?",
    "How soon after an affected assessment should I apply for special consideration?",
    "I need to know when my special consideration application is due."
])

add_example("assessment","assessment results", [
    "Where can I check my assessment results?",
    "How do I find out my grades for my assessments?",
    "When will my final assessment results be released?",
    "Where are my university grades published?",
    "How can I view the results from this semester?"
])

add_example("assessment","incomplete grade", [
    "What does an incomplete grade mean?",
    "Why does my result show as incomplete grade?",
    "I received an incomplete grade for my unit. What does that mean?",
    "What should I do if my grade is listed as incomplete?",
    "Why hasn't a final grade been given for my subject?"
])

add_example("assessment","supplementary exam results", [
    "When will I receive the results for my supplementary exam?",
    "Where can I see my supplementary assessment results?",
    "How do I check the grade from my supplementary exam?",
    "When are supplementary exam results released?",
    "I completed a supplementary exam. Where will the result appear?"
])

add_example("assessment","grade appeal", [
    "How can I appeal my final grade?",
    "What should I do if I think my grade is incorrect?",
    "Can I request a review of my assessment grade?",
    "Where do I submit a grade appeal?",
    "I disagree with my final grade. Is there a process to challenge it?"
])

add_example("assessment","grading system", [
    "What do the different university grades mean?",
    "How does the university grading system work?",
    "What mark do I need for each grade?",
    "Where can I find an explanation of the grading scale?",
    "How are marks converted into final grades?"
])

add_example("assessment","assessment submission through iLearn", [
    "How do I submit my assignment through iLearn?",
    "Where in iLearn should I upload my assessment?",
    "I need to submit an assignment online. How do I do it?",
    "How can I check whether my assignment was submitted on iLearn?",
    "Where can I upload my assessment for my unit?"
])

# campus services enquiries
add_example("campus_services","campus card", [
    "How do I apply for a university campus card?",
    "Where can I collect my student ID card?",
    "I am a new student and need a campus card. What is the process?",
    "What is the procedure to get my university ID card?",
    "Can I request a replacement for my lost campus card?"
])

add_example("campus_services","campus identification", [
    "What identification do I need to carry on campus?",
    "Can I use my campus card as student identification?",
    "Where can I obtain proof of my student identity?",
    "Do I need a student ID card to access campus facilities?",
    "How can I show that I am a current university student on campus?"
])

add_example("campus_services","building access with campus card", [
    "Can I use my campus card to access university buildings?",
    "How do I get access to restricted study areas?",
    "My campus card is not opening the building entrance. What should I do?",
    "Where can I request building access for my campus card?",
    "Do I need permission to enter certain campus building?"
])

add_example("campus_services", "library borrowing with campus card", [
    "Can I borrow library books using my campus card?",
    "How do I check out books from the university library?",
    "Do I need my student card to borrow library materials?",
    "Where can I get help with borrowing books?",
    "My campus card is not working when I borrow library books."
])

add_example("campus_services", "printing services", [
    "Where can I print documents on campus?",
    "Are printing facilities available for students?",
    "How do I use the university printing service?",
    "I need to print my assignment before class.",
    "Where can I find a printer in the university?"
])

add_example("campus_services", "computer labs", [
    "Where are the student computer labs located?",
    "Can I use university computers between classes?",
    "Are there computer labs available for students?",
    "How can I find a computer workstation on campus?",
    "Which campus facilities provide computers for students?"
])

add_example("campus_services", "IT Service Desk", [
    "Where is the university IT Service Desk located?",
    "How can I contact the campus IT help desk?",
    "Is there a service desk where students can get technology assistance?",
    "What are the contact details for the IT Service Desk?",
    "Can I visit the IT help desk for in-person assistance?"
])

add_example("campus_services", "TechBar", [
    "Where can I find the university TechBar?",
    "Can I visit TechBar for help with my laptop?",
    "What assistance is available at the campus TechBar?",
    "How do I get face-to-face support at TechBar?",
    "Is TechBar available to help students with their devices?"
])

add_example("campus_services", "student support services", [
    "Where can I find student support services on campus?",
    "How do I contact the university student support team?",
    "What support services are available to students?",
    "Is there a student help centre I can visit?",
    "Where should I go for general student assistance?"
])

add_example("campus_services", "campus facilities access", [
    "How can students access campus facilities?",
    "Are university study spaces available outside class hours?",
    "Where can I find information about campus facility access?",
    "Do students need permission to use certain university facilities?",
    "How do I find out which campus spaces I can use?"
])

# IT support enquiries

add_example("it_support", "iLearn login", [
    "How do I log in to iLearn?",
    "Where can I access my iLearn account?",
    "What credentials should I use to sign in to iLearn?",
    "I am a new student and need to log in to iLearn.",
    "How can I open my iLearn dashboard?"
])

add_example("it_support", "iLearn access problems", [
    "Why am I unable to access iLearn?",
    "My iLearn account is showing a login error.",
    "What should I do if iLearn is not loading?",
    "I keep getting an error when opening my iLearn units.",
    "How can I fix an issue accessing the iLearn website?"
])

add_example("it_support", "student password", [
    "How do I reset my university account password?",
    "I forgot the password for my student account.",
    "Where can I change my university login password?",
    "My student password has expired. What should I do?",
    "How can I recover access to my account after forgetting my password?"
])

add_example("it_support", "first-time system login", [
    "How do I activate my university account for the first time?",
    "I am a new student and cannot access the university systems.",
    "What do I need to do before my first student portal login?",
    "Where can I find instructions for setting up my student account?",
    "How do I sign in to the university systems as a new student?"
])

add_example("it_support", "multi-factor authentication", [
    "How do I set up multi-factor authentication for my account?",
    "Why do I need an authentication code when signing in?",
    "Where can I register my phone for university MFA?",
    "How do I enable two-step verification for my student login?",
    "What is the process for configuring multi-factor authentication?"
])

add_example("it_support", "MFA problems", [
    "I am not receiving the authentication code on my phone.",
    "What should I do if my MFA verification keeps failing?",
    "I changed my phone and cannot approve my university login.",
    "How can I regain access if my authenticator app is not working?",
    "My university account is asking for MFA but I cannot verify my identity."
])

add_example("it_support", "campus Wi-Fi", [
    "How do I connect my laptop to campus Wi-Fi?",
    "Why is the university wireless network not connecting?",
    "What network should students use for internet access on campus?",
    "My phone keeps disconnecting from the campus Wi-Fi.",
    "How can I troubleshoot the university Wi-Fi connection?"
])

add_example("it_support", "student email access", [
    "How do I access my university student email?",
    "Why can't I sign in to my student email account?",
    "Where can I open my university email inbox?",
    "My student email is not syncing on my phone.",
    "How can I fix problems receiving emails on my university account?"
])

add_example("it_support", "eStudent access", [
    "How do I log in to the eStudent portal?",
    "Why is my eStudent account not opening?",
    "I keep getting an error when accessing eStudent.",
    "What should I do if the student portal is unavailable?",
    "How can I resolve a login problem with eStudent?"
])

add_example("it_support", "OneHelp technical support", [
    "How do I report a technical problem through OneHelp?",
    "Where can I submit an IT support request?",
    "Can I create a help ticket for a university system error?",
    "How do I contact technical support about my account?",
    "Where can I track a request I submitted for IT assistance?"
])

# Save the raw dataset
for i, row in enumerate(rows, start=1):
    row["id"] = i

output_file = (
    Path(__file__).resolve().parent
    / "raw_student_enquiries.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["id", "text", "label", "source_topic"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Raw dataset saved to {output_file}")
print(f"Total enquiries: {len(rows)}")
