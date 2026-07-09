from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    text = models.TextField()
    image = models.ImageField(upload_to='images', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    edited_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """
        Publishes the post by setting the published_date field to the current datetime and saving the post object.

        Parameters:
            self (Post): The post object to be published.

        Returns:
            None
        """
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        """
        Returns the approved comments related to this post.
        """
        return self.comments.filter(approved=True)

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representing the title of the object.
        :rtype: str
        """
        return self.title


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approve_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        """
        Sets the 'approved' field of the Comment object to True and updates the 'approve_date' field with the current datetime.
        Saves the changes to the database.

        Parameters:
            self (Comment): The Comment object to be approved.

        Returns:
            None
        """
        self.approved = True
        self.approve_date = timezone.now()
        self.save()

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representing the text of the object.
        :rtype: str
        """
        return self.text
