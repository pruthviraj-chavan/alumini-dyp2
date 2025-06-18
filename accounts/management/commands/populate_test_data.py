from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post
from chat.models import Message
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with test data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(email='admin@example.com').exists():
            admin = User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='ADMIN',
                branch='CSE',
                year=2023,
                is_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin.email}'))
        
        # Create student users
        student_data = [
            {
                'email': 'student1@example.com',
                'password': 'student123',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
                'branch': 'CSE',
                'year': 2023,
                'bio': 'Final year Computer Science student interested in AI and machine learning.',
                'is_verified': True
            },
            {
                'email': 'student2@example.com',
                'password': 'student123',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'branch': 'IT',
                'year': 2024,
                'bio': 'Third year IT student passionate about web development and cybersecurity.',
                'is_verified': True
            },
            {
                'email': 'student3@example.com',
                'password': 'student123',
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'branch': 'ECE',
                'year': 2023,
                'bio': 'Electronics student with interest in IoT and embedded systems.',
                'is_verified': False
            }
        ]
        
        students = []
        for data in student_data:
            if not User.objects.filter(email=data['email']).exists():
                student = User.objects.create_user(
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    role='STUDENT',
                    branch=data['branch'],
                    year=data['year'],
                    bio=data['bio'],
                    is_verified=data['is_verified']
                )
                students.append(student)
                self.stdout.write(self.style.SUCCESS(f'Created student: {student.email}'))
        
        # Create alumni users
        alumni_data = [
            {
                'email': 'alumni1@example.com',
                'password': 'alumni123',
                'first_name': 'Vikram',
                'last_name': 'Singh',
                'branch': 'CSE',
                'year': 2018,
                'bio': 'Software Engineer at Google. Working on cloud infrastructure.',
                'phone': '+91 9876543210',
                'is_verified': True
            },
            {
                'email': 'alumni2@example.com',
                'password': 'alumni123',
                'first_name': 'Neha',
                'last_name': 'Gupta',
                'branch': 'IT',
                'year': 2019,
                'bio': 'Product Manager at Amazon. Graduated in 2019 with honors.',
                'phone': '+91 9876543211',
                'is_verified': True
            },
            {
                'email': 'alumni3@example.com',
                'password': 'alumni123',
                'first_name': 'Rajesh',
                'last_name': 'Khanna',
                'branch': 'ME',
                'year': 2020,
                'bio': 'Mechanical Engineer at Tata Motors. Specializing in automotive design.',
                'phone': '+91 9876543212',
                'is_verified': False
            }
        ]
        
        alumni = []
        for data in alumni_data:
            if not User.objects.filter(email=data['email']).exists():
                alum = User.objects.create_user(
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    role='ALUMNI',
                    branch=data['branch'],
                    year=data['year'],
                    bio=data['bio'],
                    phone=data.get('phone', ''),
                    is_verified=data['is_verified']
                )
                alumni.append(alum)
                self.stdout.write(self.style.SUCCESS(f'Created alumni: {alum.email}'))
        
        # Create posts
        achievement_posts = [
            {
                'title': 'Secured Internship at Microsoft',
                'content': 'I am excited to share that I have secured a summer internship at Microsoft. Looking forward to working with the Azure team and learning cloud technologies.',
                'category': 'ACHIEVEMENT'
            },
            {
                'title': 'Won First Prize in Hackathon',
                'content': 'Our team won the first prize in the national level hackathon organized by TechCrunch. We built an AI-powered solution for healthcare.',
                'category': 'ACHIEVEMENT'
            },
            {
                'title': 'Published Research Paper',
                'content': 'My research paper on "Efficient Algorithms for Big Data Processing" has been accepted in the International Conference on Data Science.',
                'category': 'ACHIEVEMENT'
            }
        ]
        
        job_posts = [
            {
                'title': 'Software Engineer Opening at Google',
                'content': 'Google is hiring Software Engineers for their Bangalore office. Requirements: B.Tech in CS/IT, 0-2 years experience, strong in algorithms and data structures. Apply with your resume at careers.google.com.',
                'category': 'JOB'
            },
            {
                'title': 'Data Scientist Position at Amazon',
                'content': 'Amazon is looking for Data Scientists to join their Machine Learning team. Requirements: Masters/PhD in CS/Statistics, experience with Python, ML libraries. Email your resume to hiring@amazon.com.',
                'category': 'JOB'
            },
            {
                'title': 'Frontend Developer Internship',
                'content': 'Our startup is offering a 6-month internship for Frontend Developers. Tech stack: React, Redux, TypeScript. Stipend: Rs. 25,000 per month. Send your portfolio to jobs@startup.com.',
                'category': 'JOB'
            }
        ]
        
        # Assign posts to users
        all_users = students + alumni
        if all_users:
            # Create achievement posts
            for post_data in achievement_posts:
                user = random.choice(all_users)
                post = Post.objects.create(
                    user=user,
                    title=post_data['title'],
                    content=post_data['content'],
                    category=post_data['category'],
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                self.stdout.write(self.style.SUCCESS(f'Created achievement post: {post.title} by {user.email}'))
            
            # Create job posts (only by alumni)
            if alumni:
                for post_data in job_posts:
                    user = random.choice(alumni)
                    post = Post.objects.create(
                        user=user,
                        title=post_data['title'],
                        content=post_data['content'],
                        category=post_data['category'],
                        created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created job post: {post.title} by {user.email}'))
        
        # Create some messages between users
        if students and alumni:
            for student in students:
                if student.is_verified:
                    for alum in alumni:
                        if alum.is_verified:
                            # Student to Alumni
                            Message.objects.create(
                                sender=student,
                                receiver=alum,
                                message_text=f"Hello {alum.first_name}, I am interested in learning more about your career path. Could you share some advice?",
                                timestamp=datetime.now() - timedelta(days=random.randint(1, 10), hours=random.randint(1, 23))
                            )
                            
                            # Alumni to Student
                            Message.objects.create(
                                sender=alum,
                                receiver=student,
                                message_text=f"Hi {student.first_name}, I'd be happy to help. What specific area are you interested in?",
                                timestamp=datetime.now() - timedelta(days=random.randint(0, 5), hours=random.randint(1, 23))
                            )
                            
                            self.stdout.write(self.style.SUCCESS(f'Created messages between {student.email} and {alum.email}'))
        
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
