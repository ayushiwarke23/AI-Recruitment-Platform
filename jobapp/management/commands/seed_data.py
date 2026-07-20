from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth.models import User
from jobapp.models import Company, UserRole, RecruiterProfile, CandidateProfile, Education, Skill, Certification, Offer, Interview, Experience, Project, Job, Application,Notification, SavedJob
from django.core.files import File
from datetime import timedelta, time
from django.utils import timezone


class Command(BaseCommand):
    help = "Generate fake data"
    
    def handle(self, *args, **kwargs):
        COMPANIES = [
        "Google",
        "Microsoft",
        "Amazon",
        "Adobe",
        "Oracle",
        "Capgemini",
        "Infosys",
        "TCS",
        "Wipro",
        "NVIDIA",
        "Vector Consulting",
        "Cognizant"
    ]

        self.fake = Faker()
        for company_name in COMPANIES:
            username = company_name.lower().replace(" ","_")

            user = User.objects.create_user(username = username, 
                    email=f"{username}@company.com", 
                    password = "SeedData@123"
            )
            
            UserRole.objects.create(
                user=user,
                role = "company"
            )

            company = Company.objects.create(
                user=user, 
                company_name = company_name,
                website = f"https://www.{username}.com",
                email = f"{username}@company.com",
                phone = self.fake.phone_number()[:10],
                description = self.fake.text(max_nb_chars=400),
                industry = "Information Technology",
                headquarters = random.choice(
                    [
                        "Pune","Banglore","Hyderabad","Delhi","Mumbai","USA","London","Australia","Sydney","France","Kolkata"
                    ]
                ),
                founded_year = random.randint(1975,2022),
                company_size = random.choice(
                ["201-500",

                "501-1000",

                "1001-5000",

                "5001-10000"]
                ),
                linkedin=f"https://linkedin.com/company/{username}"
            )
            with open("seed_assets/companylogo.png", "rb") as logo:
                company.company_logo.save(
                    "companylogo.png",
                    File(logo),
                    save=True)
        companies = list(Company.objects.all())
        for i in range(20):

            first_name = self.fake.first_name()
            last_name = self.fake.last_name()

            username = (
                first_name.lower()
                + "."
                + last_name.lower()
                + str(i)
            )

            user = User.objects.create_user(
            username=username,
            email=f"{username}@gmail.com",
            password="SeedData@123")

            UserRole.objects.create(
            user=user,
            role="recruiter"
            )
            
            recruiter = RecruiterProfile.objects.create(

            user=user,
            
            company=random.choice(companies),

            full_name=f"{first_name} {last_name}",

            phone=self.fake.numerify("##########"),

            email=f"{username}@gmail.com",

            designation=random.choice([
                "HR Executive",
                "Senior Recruiter",
                "Talent Acquisition Specialist",
                "HR Manager",
                "Project Head",
                "National Manager",
            ]),

            department="Human Resources",

            experience_years=random.randint(1,12),

            office_location=random.choice([
                "Pune","Banglore","Hyderabad","Delhi","Mumbai","USA","London","Australia","Sydney","France","Kolkata"
            ]),

            bio=self.fake.text(max_nb_chars=150),

            linkedin=f"https://linkedin.com/in/{username}"

        )
            with open("seed_assets/recruiterprofile.png", "rb") as image:

                recruiter.profile_picture.save(
            "recruiterprofile.png",
            File(image),
            save=True
        )
            
        candidate_images = [
        "seed_assets/candidate1.png",
        "seed_assets/candidate2.png",
        "seed_assets/candidate3.png",
        "seed_assets/candidate4.png",]

        for i in range(100):

            first_name = self.fake.first_name()
            last_name = self.fake.last_name()

            username = (
            first_name.lower()
            + "."
            + last_name.lower()
            + str(i))

            user = User.objects.create_user(
            username=username,
            email=f"{username}@gmail.com",
            password="SeedData@123"
        )

            UserRole.objects.create(
            user=user,
            role="candidate"
        )

            candidate = CandidateProfile.objects.create(
            user=user,
            full_name=f"{first_name} {last_name}",
            phone=self.fake.numerify("##########"),
            date_of_birth=self.fake.date_between(
                start_date="-35y",
                end_date="-20y"
            ),
            gender=random.choice([
                "male",
                "female"
            ]),
            bio=self.fake.text(max_nb_chars=150),
            github=f"https://github.com/{username}",
            linkedin=f"https://linkedin.com/in/{username}"
        )

            image_path = random.choice(candidate_images)

            with open(image_path, "rb") as image:

                candidate.profile_picture.save(
                f"{username}.png",
                File(image),
                save=True
            )

        self.create_skills()

        self.create_education()

        self.create_experience()

        self.create_projects()

        self.create_certifications()

        self.create_jobs()

        self.create_applications()

        self.create_saved_jobs()

        self.create_interviews()

        self.create_offers()

        self.create_notifications()
        self.stdout.write(
            self.style.SUCCESS(
                "Seed command working!"
            )
        ) 

    LOCATIONS = [
        "Pune",
        "Bangalore",
        "Hyderabad",
        "Mumbai",
        "Delhi",
        "Chennai",
        "Kolkata",
        "Remote"
    ]

    JOB_TYPES = [
        "full_time",
        "part_time",
        "contract",
        "internship",
        "temporary"
    ]

    WORKPLACE_TYPES = [
        "onsite",
        "hybrid",
        "remote"
    ]

    APPLICATION_STATUS = [
        "Applied",
        "Under Review",
        "Shortlisted",
        "Interview Scheduled",
        "Selected",
        "Rejected"
    ]


    def create_jobs(self):

        print("Creating Jobs...")

        recruiters = RecruiterProfile.objects.select_related("company")

        for recruiter in recruiters:

            for i in range(random.randint(6,10)):

                Job.objects.create(

                    recruiter=recruiter,

                    company=recruiter.company,

                    title=random.choice(self.JOB_TITLES),

                    description=self.fake.text(500),

                    skills_required=", ".join(
                        random.sample(self.SKILLS, random.randint(4,8))
                    ),

                    location=random.choice(self.LOCATIONS),

                    job_type=random.choice(self.JOB_TYPES),

                    workplace_type=random.choice(self.WORKPLACE_TYPES),

                    experience_required=random.randint(0,8),

                    salary_min=random.randint(300000,1200000),

                    salary_max=random.randint(1200001,2500000),

                    vacancies=random.randint(1,15),

                    application_deadline=timezone.now().date()+timedelta(days=random.randint(20,120)),

                    is_active=True

                )

    def create_applications(self):

        print("Creating Applications...")

        candidates=list(CandidateProfile.objects.all())

        jobs=list(Job.objects.all())

        for candidate in candidates:

            applied=random.sample(
                jobs,
                random.randint(3,8)
            )

            for job in applied:

                Application.objects.create(

                    candidate=candidate,

                    job=job,

                    cover_letter=self.fake.text(250),

                    status=random.choice(
                        self.APPLICATION_STATUS
                    ),

                    resume="application_resume/default_resume.pdf"

                )
    def create_saved_jobs(self):

        print("Creating Saved Jobs...")

        candidates=list(CandidateProfile.objects.all())

        jobs=list(Job.objects.all())

        for candidate in candidates:

            for job in random.sample(
                jobs,
                random.randint(2,6)
            ):

                SavedJob.objects.get_or_create(

                    candidate=candidate,

                    job=job

                )
    from datetime import time

    def create_interviews(self):

        print("Creating Interviews...")

        applications=Application.objects.filter(

            status="Interview Scheduled"

        )

        for application in applications:

            Interview.objects.create(

                application=application,

                interview_date=self.fake.date_between(

                    start_date="today",

                    end_date="+30d"

                ),

                interview_time=time(

                    hour=random.randint(9,17),

                    minute=random.choice([0,30])

                ),

                mode=random.choice([

                    "Online",

                    "Offline"

                ]),

                meeting_link="https://meet.google.com/demo",

                office_address=application.job.company.headquarters,

                interviewer_name=random.choice([

                    "Rahul Sharma",

                    "Priya Singh",

                    "Neha Patil",

                    "Ankit Verma"

                ]),

                instructions=self.fake.text(150)

            )

    def create_offers(self):

        print("Creating Offers...")

        applications=Application.objects.filter(

            status="Selected"

        )

        for application in applications:

            Offer.objects.create(

                application=application,

                offer_letter="offer_letters/default_offer.pdf",

                other_info=self.fake.text(200),

                status=random.choice([

                    "Accepted",

                    "Rejected"

                ]),

                hr_contact="hr@company.com"

            )
    def create_notifications(self):


        for user in User.objects.all():

            for i in range(random.randint(2,8)):

                Notification.objects.create(

                    user=user,

                    title=random.choice([

                        "Application Updated",

                        "Interview Scheduled",

                        "Offer Received",

                        "Profile Viewed",

                        "New Job Posted"

                    ]),

                    message=self.fake.text(120)

                )
    SKILLS = [
"Python","Java","C","C++","C#","JavaScript","TypeScript",
"React","Angular","Vue","Node.js","Express","Django","Flask",
"FastAPI","Spring Boot","HTML","CSS","Bootstrap","Tailwind",
"PostgreSQL","MySQL","MongoDB","Redis","SQLite",
"Docker","Kubernetes","AWS","Azure","GCP",
"Git","GitHub","Linux",
"Machine Learning","Deep Learning","TensorFlow",
"PyTorch","OpenCV","NLP",
"REST API","GraphQL"
]

    COLLEGES = [
"IIT Bombay",
"IIT Delhi",
"IIT Madras",
"IIT Kanpur",
"NIT Trichy",
"NIT Surathkal",
"VIT Vellore",
"MIT WPU",
"COEP Pune",
"PCCOE Pune",
"PES University",
"SRM University",
"BITS Pilani",
"Manipal University"
]

    DEGREES = [
"B.Tech",
"B.E.",
"M.Tech",
"MCA",
"BCA"
]

    FIELDS = [
"Computer Science",
"Information Technology",
"Artificial Intelligence",
"Data Science",
"Electronics",
"Mechanical"
]

    CERTIFICATIONS = [
"AWS Cloud Practitioner",
"AWS Solutions Architect",
"Microsoft Azure Fundamentals",
"Google Associate Cloud Engineer",
"Oracle Java",
"Cisco CCNA",
"RedHat RHCSA",
"TensorFlow Developer",
"Meta Backend Developer",
"IBM Data Science"
]

    PROJECTS = [
"AI Recruitment Platform",
"Hospital Management System",
"Smart Attendance",
"Online Banking",
"E-Commerce Website",
"Chat Application",
"Inventory Management",
"Movie Recommendation System",
"Weather Forecast App",
"Face Recognition System"
]

    JOB_TITLES = [
"Software Engineer",
"Backend Developer",
"Python Developer",
"Full Stack Developer",
"AI Engineer",
"ML Engineer",
"Data Analyst",
"Cloud Engineer",
"DevOps Engineer",
"Software Developer",
"AIML Engineer",
"AWS Engineer",
"Associate Software Engineer",
"Django Developer",
"Database Administrator",
]
    def create_skills(self):

        print("Creating Skills...")

        for candidate in CandidateProfile.objects.all():

            skills = random.sample(
                self.SKILLS,
                random.randint(5,10)
            )

            for skill in skills:

                Skill.objects.create(

                    candidate=candidate,

                    skill_name=skill

                )

        print("Skills Created")

    def create_education(self):

        print("Creating Education...")

        for candidate in CandidateProfile.objects.all():

            Education.objects.create(

                candidate=candidate,

                college_name=random.choice(self.COLLEGES),

                degree=random.choice(self.DEGREES),

                field_of_study=random.choice(self.FIELDS),

                start_year=random.randint(2015,2022),

                end_year=random.randint(2023,2026),

                grade=round(random.uniform(6.5,9.9),2),

                currently_studying=False

            )

        print("Education Created")
    def create_experience(self):

        print("Creating Experience...")

        companies=list(Company.objects.all())

        for candidate in CandidateProfile.objects.all():

            if random.choice([True,False]):

                Experience.objects.create(

                    candidate=candidate,

                    company=random.choice(companies),

                    job_title=random.choice(self.JOB_TITLES),

                    start_date=self.fake.date_between(
                        start_date="-5y",
                        end_date="-2y"
                    ),

                    end_date=self.fake.date_between(
                        start_date="-2y",
                        end_date="today"
                    ),

                    currently_working=False,

                    job_description=self.fake.text(200)

                )
    def create_projects(self):

        print("Creating Projects...")

        for candidate in CandidateProfile.objects.all():

            for i in range(random.randint(1,3)):

                Project.objects.create(

                    candidate=candidate,

                    project_title=random.choice(self.PROJECTS),

                    project_description=self.fake.text(300),

                    links=f"https://github.com/{candidate.user.username}",

                    technologies_used=", ".join(

                        random.sample(

                            self.SKILLS,

                            random.randint(3,6)

                        )

                    )

                )

    def create_certifications(self):

        print("Creating Certifications...")

        for candidate in CandidateProfile.objects.all():

            for i in range(random.randint(0,3)):

                Certification.objects.create(

                    candidate=candidate,

                    certification_name=random.choice(
                        self.CERTIFICATIONS
                    ),

                    issuing_organization=random.choice([
                        "AWS",
                        "Google",
                        "Microsoft",
                        "Oracle",
                        "Cisco",
                        "Coursera",
                        "Udemy"
                    ]),

                    issue_date=self.fake.date_between(
                        start_date="-5y",
                        end_date="today"
                    ),

                    credential_id=self.fake.uuid4(),

                    credential_url="https://coursera.org"

                )