from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            first_name='Student',
            last_name='Test',
            role='STUDENT',
            branch='CSE',
            year=2023,
            is_verified=True
        )
        
        self.alumni = User.objects.create_user(
            email='alumni@example.com',
            password='testpass123',
            first_name='Alumni',
            last_name='Test',
            role='ALUMNI',
            branch='CSE',
            year=2018,
            is_verified=True
        )
    
    def test_message_creation(self):
        """Test that a message can be created"""
        message = Message.objects.create(
            sender=self.student,
            receiver=self.alumni,
            message_text='Hello, this is a test message',
        )
        self.assertEqual(message.message_text, 'Hello, this is a test message')
        self.assertEqual(message.sender, self.student)
        self.assertEqual(message.receiver, self.alumni)
        self.assertFalse(message.is_read)
        
    def test_message_read_status(self):
        """Test that a message can be marked as read"""
        message = Message.objects.create(
            sender=self.student,
            receiver=self.alumni,
            message_text='Hello, this is a test message',
        )
        self.assertFalse(message.is_read)
        
        # Mark message as read
        message.is_read = True
        message.save()
        
        # Refresh from database
        message.refresh_from_db()
        self.assertTrue(message.is_read)

class ChatViewTests(TestCase):
    def setUp(self):
        # Create test users
        self.student = User.objects.create_user(
            email='student@example.com',
            password='testpass123',
            first_name='Student',
            last_name='Test',
            role='STUDENT',
            branch='CSE',
            year=2023,
            is_verified=True
        )
        
        self.alumni = User.objects.create_user(
            email='alumni@example.com',
            password='testpass123',
            first_name='Alumni',
            last_name='Test',
            role='ALUMNI',
            branch='CSE',
            year=2018,
            is_verified=True
        )
        
        self.unverified_student = User.objects.create_user(
            email='unverified@example.com',
            password='testpass123',
            first_name='Unverified',
            last_name='Student',
            role='STUDENT',
            branch='CSE',
            year=2023,
            is_verified=False
        )
        
        # Create test messages
        Message.objects.create(
            sender=self.student,
            receiver=self.alumni,
            message_text='Hello from student',
        )
        
        Message.objects.create(
            sender=self.alumni,
            receiver=self.student,
            message_text='Hello from alumni',
        )
        
        # Create client
        self.client = Client()
    
    def test_inbox_view_authenticated(self):
        """Test that authenticated users can access inbox"""
        # Login
        self.client.login(email='student@example.com', password='testpass123')
        
        # Access inbox
        response = self.client.get(reverse('inbox'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/inbox.html')
        self.assertIn('chat_partners', response.context)
        self.assertEqual(len(response.context['chat_partners']), 1)
        
    def test_inbox_view_unauthenticated(self):
        """Test that unauthenticated users cannot access inbox"""
        # Access inbox without login
        response = self.client.get(reverse('inbox'))
        
        # Check redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('inbox')}")
    
    def test_chat_with_user_view(self):
        """Test that users can access chat with another user"""
        # Login
        self.client.login(email='student@example.com', password='testpass123')
        
        # Access chat with alumni
        response = self.client.get(reverse('chat_with_user', args=[self.alumni.id]))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat.html')
        self.assertIn('chat_partner', response.context)
        self.assertIn('messages', response.context)
        self.assertIn('form', response.context)
        
    def test_start_new_chat_view(self):
        """Test that users can access the start new chat page"""
        # Login
        self.client.login(email='student@example.com', password='testpass123')
        
        # Access start new chat page
        response = self.client.get(reverse('start_new_chat'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/new_chat.html')
        self.assertIn('available_users', response.context)
        
    def test_unverified_user_restrictions(self):
        """Test that unverified users cannot start chats"""
        # Login as unverified user
        self.client.login(email='unverified@example.com', password='testpass123')
        
        # Try to access start new chat page
        response = self.client.get(reverse('start_new_chat'))
        
        # Should redirect to home with a message
        self.assertRedirects(response, reverse('home'))
