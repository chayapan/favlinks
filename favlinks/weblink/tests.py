from io import StringIO
from django.core.management import call_command
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from weblink.models import URL, Category, Tag, Link

from django.contrib.auth import authenticate, login, alogin, logout

class UserAccountTestCase(TestCase):
    """
    - username/email must be unique
    - password cannot be weak password
    - user signup via web form
    - user signup via API
    - user login via web form
    - user login via API
    """
    def setUp(self):
        user001 = User.objects.create_user(  username="johnw",
                                        email="john.wick@example.com",
                                        password="changeme",
                                        first_name="John",
                                        last_name="Wick")
        username = "john"
        first_name = "John"
        last_name = "Doe"
        email = "john.doe@example.com"
        user002 = User.objects.create(  username=username, 
                                        email=email, 
                                        first_name=first_name, 
                                        last_name=last_name  )
    
    def test_account_signup_(self):
        with self.assertRaises(User.DoesNotExist):
            user001 = User.objects.get(username="alice")
        
        with self.assertRaises(User.MultipleObjectsReturned):
            user001 = User.objects.get(first_name="John")
        
        c = Client()
        response = c.get('/accounts/login')
        self.assertEqual(response.status_code, 200, 'Login page should be available.')
    
        response = c.get('/accounts/signup')
        self.assertEqual(response.status_code, 200, 'Signup page should be available.')
    
    def test_user_signin_signout(self):
        """create user, signin, signout."""
        user003 = User.objects.create_user("test1","test1@example.com","simplePassword")
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200, 'Landing page should be available.')
        

    def tearDown(self) -> None:
        return super().tearDown()


class ApplicationModelClassesTest(TestCase):
    def test_user_model(self):
        g  = Group.objects.create(name='FreeTier')
        u = User.objects.create(username='user-1')
        self.assertEquals(g.id, 1)
        self.assertEquals(u.id, 1)

    def test_weblink_models(self):
        """
        This test cases examine URL object and relationships: 
            URL-category URL-tags User-URL."""
        u1 = User.objects.create(username='user-1')
        self.assertEquals(u1.id, 1)
        url_0 = 'https://www.example.com'
        url1 = URL.objects.create(raw_url=url_0)
        cat1 = Category.objects.create(name='TEST-LINK-1')
        # The link object associates a User with his favorite URLs.
        link1 = Link.objects.create(url_text=url_0, category=cat1, user=u1, url=url1)
        # Tags can be added to the link instance
        tags = []
        tag_list = ['a','b','c','d']
        for t in tag_list:
            # add tag keyword to the link
            tag = link1.add_tag(t) # the method returns Tag object
            tags.append(tag)
        self.assertEquals(len(tags), 4, "Create four tags for testing.")
        tagged = [t.value for t in url1.tags.all()]
        self.assertTrue(set(tag_list).issubset(tagged), "Tags are added, so they have subset relationship.")

    def test_tag_feature(self):
        """Tagging function. User can tag URL with given tag. Tags are list of strings."""
        URL
        Tag
    def test_category_feature(self):
        """Category feature. URL belongs to a category. When user creates a URL (make a favorite) he has to define which category the URL belongs to."""
        Category
        URL

class CategoryModelTest(TestCase):
    def test_create_category_object(self):
        cat1 = 'A'
        cat2 = 'B'
        cat3 = 'C'
        cat4 = 'D'
        a = Category.objects.create(name=cat1)
        b = Category.objects.create(name=cat2)
        c = Category.objects.create(name=cat3)
        d = Category.objects.create(name=cat4)
        d.parent = c 
        d.save()
        self.assertEquals(d.parent, c, "Test parent-child relationship in category tree.")


class TagModelTest(TestCase):
    def test_create_category_object(self):
        tag_list = ['a','b','c','d']
        tags = []
        for t in tag_list:
            tag = Tag.objects.create(value=t)
            tags.append(tag)
        self.assertEquals(len(tags), 4, "Create four tags for testing.")


class AccountRegistrationCommandTest(TestCase):
    """Create account and test log-in.
    manage.py register EMAIL --password secr3tVry

    Testing for command line.
    https://docs.djangoproject.com/en/5.0/topics/testing/tools/#topics-testing-management-commands
    """
    def test_command_output(self):
        out = StringIO()
        call_command("register", "list-all", stdout=out)
        self.assertIn('Manage User Accounts', out.getvalue())

class MakeFavLinkCommandTest(TestCase):
    """Test the making a favorite link function with CLI.

    manage.py link make-favorite EMAIL URL CATEGORY

    Testing for command line.
    https://docs.djangoproject.com/en/5.0/topics/testing/tools/#topics-testing-management-commands
    """
    def test_command_output(self):
        out = StringIO()
        call_command("link", "list", stdout=out)
        self.assertIn('=PK=\t=FAV-LINK=', out.getvalue())
