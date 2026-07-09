# Blog Application

## Overview
This project is a secure blog application that allows users to create, manage, and share blog posts securely. It is designed to provide a user-friendly platform for writers to express their thoughts and connect with readers. The application is built using HTML, CSS, Bootstrap, Python, Django, and SQLite, ensuring a dynamic and engaging user experience.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation Guide](#installation-guide)
- [Usage Instructions](#usage-instructions)
- [Contributing Guidelines](#contributing-guidelines)
- [License](#license)

## Features
- **User Registration and Authentication:** Users can create accounts, log in, and securely manage their blog posts and comments.
- **Blog Post Creation and Management:** Writers can easily create, edit, and delete their blog posts, with the option to add images and format text.
- **Commenting System:** Readers can post comments on blog posts, fostering discussions and engagement.
- **User Profiles:** Users can view their profiles, including their blog posts, comments, and personal information.
- **Search Functionality:** Users can search for specific blog posts or topics, making it easier to find content of interest.
- **Password Reset Email Notifications:** Users receive email notifications for the Password reset link.
- **Social Media Integration:** Users can share their blog posts on social media platforms, expanding their reach and engagement.
- **Responsive Design:** The application is designed to be responsive, ensuring a seamless experience on various devices, including mobile and desktop.

## Technologies Used
- **Front End:** HTML, CSS, Bootstrap, JavaScript
- **Back End:** Python, Django
- **Database:** SQLite
- **Testing:** Unit tests using Django's testing framework

## Installation Guide
To install and set up the Blog Application, follow these steps:

1. Clone the repository: `git clone https://github.com/joekariuki3/mysite_blog_django.git`
2. Navigate to the project directory: `cd mysite_blog_django.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Set up the database:
   - Migrate the database: `python manage.py migrate`
   - Create a superuser: `python manage.py createsuperuser`
7. Create a `.env` file in the project root directory with the following variables:
   ```
   DATABASE_URL=sqlite:///db.sqlite3
   ENVIRONMENT='development'
   User_Email="your_email@example.com"
   User_Password="your_password_here"
   ```
   Replace `"your_email@example.com"` with your actual email address and `"your_password_here"` with your desired password.
8. Run the development server: `python manage.py runserver`
9. Access the application in your web browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage Instructions
### For Writers/Bloggers:
1. Register and create an account by clicking on the "Sign Up" button.
2. Log in to your account using your credentials.
3. To create a new blog post, click on the "New Post" button and fill in the title, content, and optional image.
4. Manage your blog posts by editing or deleting them as needed.
5. Engage with your readers by responding to comments on your posts.
6. Share your blog posts on social media platforms to reach a wider audience.
### For Readers:
1. Explore the blog posts by scrolling through the homepage or searching.
2. Read the blog posts that interest you and engage with the content by leaving comments.
3. Follow your favourite writers to stay updated with their latest posts.
4. Share the blog posts on social media to spread the word.

## Contributing Guidelines
Contributions are welcome! If you have suggestions, improvements, or bug fixes, please follow these steps:

1. Fork the repository on GitHub.
2. Create a branch for your changes: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add your commit message here'`.
4. Push your changes to your branch: `git push origin feature/your-feature`.
5. Submit a pull request, and clearly describe your changes.

## License
This project is licensed under the MIT License. If you would like more information, please refer to the LICENSE file in the repository.

Feel free to reach out to @joekariuki3 project owner for any queries or suggestions. Enjoy using and contributing to the Blog Application!
