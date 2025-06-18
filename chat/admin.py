from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model"""
    list_display = ('sender', 'receiver', 'short_message', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('sender__email', 'receiver__email', 'message_text')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    
    def short_message(self, obj):
        """Display a shortened version of the message text"""
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    short_message.short_description = 'Message'

admin.site.register(Message, MessageAdmin)
